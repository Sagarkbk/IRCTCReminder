import jwt
from fastapi import Header, HTTPException, status, Depends
import os
from Services.userService import get_user_by_id
from Services.redisService import get_redis
from redis.asyncio import Redis

async def authMiddleware(authorization = Header(...), rds: Redis = Depends(get_redis)):
    try:
        JWT_SECRET = os.getenv("JWT_SECRET")
        
        if not JWT_SECRET:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                detail="JWT_SECRET is not available in Environment Variables")
        
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(
                                status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail="Unauthorized User"
                            )
    
        jwt_token = authorization.split(" ")[1]

        payload = jwt.decode(jwt_token, JWT_SECRET, algorithms="HS256")

        user_id = payload['user_id']
        user = await get_user_by_id(user_id, rds)
        if not user:
            raise HTTPException(
                                status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Not a registered user"
                            )

        return user['id']

    except (jwt.PyJWTError, KeyError):
        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Unauthorized User"
                        )