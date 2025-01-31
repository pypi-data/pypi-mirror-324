from uuid import UUID
from typing import Dict, Any
from sqlalchemy import text
from Database.Connection import DBConnection
from RedisCache.Redis import RedisCacheAsync
from Exception.Exception import Unauthorized, RedisException
from Helpers.Message import UNAUTHORIZATED, REDIS_FAILED
from Helpers.Code import DB_ERROR_0006, DB_ERROR_SERVER

class TokenValidate:

    def __init__(self):
        self.db = DBConnection()
        self.redis = RedisCacheAsync()

    async def validate(self, token_id: UUID, user_id: UUID) -> Dict[str, Any]:
        try:
            await self.redis.connect()
            exist_token = await self.redis.exists(token_id)
            if exist_token:
                return await self.redis.get_dict(token_id)

            session = self.db.get_session()
            with session:
                query = text('''
                    EXEC SECURITY.sps_ValidateUserToken  
                    @i_idToken = :token_id,
                    @i_idUser = :user_id
                ''')
                result = session.execute(query, {'token_id': token_id, 'user_id': user_id})
                row = {'isAuth': bool(result.scalar())} 
                if not row:
                    raise Unauthorized(error=UNAUTHORIZATED, status_code=DB_ERROR_0006)

            await self.redis.set_dict(token_id, row, ttl=1800)
            return row

        except Exception as e:
            raise RedisException(message=REDIS_FAILED, error=str(e), status_code=DB_ERROR_SERVER)

        finally:
            await self.redis.close()
