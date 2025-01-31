from uuid import UUID
from typing import Dict, Any
from sqlalchemy import text
from Database.Connection import DBConnection
from RedisCache.Redis import RedisCacheAsync
from Exception.Exception import Unauthorized
from Helpers.Message import UNAUTHORIZATED
from Helpers.Code import DB_ERROR_0006

class TokenValidate:

    def __init__(self):
        self.db = DBConnection()
        self.redis = RedisCacheAsync()

    async def validate(self, token_id: UUID, user_id: UUID) -> Dict[str, Any]:
        session = self.db.get_session()
        await self.redis.connect()
        exist_token = await self.redis.exists(token_id)
        if exist_token:
            data_byte = await self.redis.get_str(token_id)
            return data_byte.decode('utf-8')
        
        with session:
            query = text('''
                EXEC SECURITY.sps_ValidateUserToken  
                @i_idToken = :token_id,
                @i_idUser = :user_id
            ''')
            result = session.execute(query, {'token_id': token_id, 'user_id': user_id})
            row = result.scalar()
            if not row:
                raise Unauthorized(error=UNAUTHORIZATED, status_code=DB_ERROR_0006)
            
        await self.redis.set_str(token_id, row, ttl=1800)
        await self.redis.close()
        return row

