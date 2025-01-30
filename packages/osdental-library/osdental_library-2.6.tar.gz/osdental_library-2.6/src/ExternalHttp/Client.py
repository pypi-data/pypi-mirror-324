import os
import json
import asyncio
import httpx
from datetime import datetime
from typing import Dict, Any
from dotenv import load_dotenv
from ServicesBus.TaskQueue import task_queue
from Exception.Exception import HttpClientException
from Helpers.Message import HTTP_FAILED
from Helpers.Constant import STATUS_ERROR

load_dotenv()

class APIClient(httpx.AsyncClient):

    async def rest_request(self, method:str, url:str, *args, **kwargs):
        try:
            asyncio.create_task(self.send_request_to_service_bus(endpoint=url, body=kwargs.get('body')))
            response = await self.request(method, url, *args, **kwargs)
            response.raise_for_status()
            asyncio.create_task(self.send_response_to_service_bus(response))
            return response.json()
        
        except httpx.RequestError as e:
            raise HttpClientException(message=HTTP_FAILED, error=str(e), status_code=STATUS_ERROR)


    async def graph_request(self, url:str, consult:str, variables:Dict[str, Any]):
        try:
            asyncio.create_task(self.send_request_to_service_bus(endpoint=url, body=variables))
            response = await self.post(url, json={'query': consult, 'variables': variables})
            response.raise_for_status()
            asyncio.create_task(self.send_response_to_service_bus(response))
            return response.json()
        
        except httpx.RequestError as e:
            raise HttpClientException(message=HTTP_FAILED, error=str(e), status_code=STATUS_ERROR)
    
        
    async def send_request_to_service_bus(self, endpoint: str, body: Dict[str, Any]) -> None:
        """
        Send a message to the Service Bus with details about the request made:

        :param endpoint: (str): URL of the endpoint to which the request will be made.
        :param body: (Dict[str, Any]): Body of the request (usually in JSON format).
        """
        headers = self.request.headers
        message_json = {
            'idMessageLog': headers.get('Idmessagelog'),
            'type': 'REQUEST',
            'environment': os.getenv('ENVIRONMENT'),
            'dateExecution': datetime.now(self.local_tz).strftime('%Y-%m-%d %H:%M:%S'),
            'header': json.dumps(dict(headers)),
            'microServiceUrl': endpoint,
            'microServiceName': os.getenv('MICROSERVICE_NAME'),
            'microServiceVersion': os.getenv('MICROSERVICE_VERSION'),
            'serviceName': body.get('operationName') if body else None,
            'machineNameUser': headers.get('Machinenameuser'),
            'ipUser': headers.get('Ipuser'),
            'userName': headers.get('Username'),
            'localitation': headers.get('Localitation'),
            'httpMethod': 'POST',
            'httpResponseCode': '*',
            'messageIn': json.dumps(body) if body else None,
            'messageOut': '*',
            'errorProducer': '*',
            'auditLog': 'MESSAGE_LOG_EXTERNAL'
        }
        asyncio.create_task(task_queue.enqueue(message_json))


    async def send_response_to_service_bus(self, response: httpx.Response) -> None:
        """
        Send a message to the Service Bus with details about the response received:

        :param response: (Response): Response object received from the endpoint.
        """
        message_json = {
            'idMessageLog': self.request.headers.get('Idmessagelog'),
            'type': 'RESPONSE',
            'dateExecution': datetime.now(self.local_tz).strftime('%Y-%m-%d %H:%M:%S'),
            'httpResponseCode': str(response.status_code),
            'messageOut': json.dumps(response.json()),
            'auditLog': 'MESSAGE_LOG_EXTERNAL'
        }
        asyncio.create_task(task_queue.enqueue(message_json))