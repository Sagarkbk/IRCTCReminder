from fastapi import APIRouter, Depends
from redis.asyncio import Redis
from Services.redisService import get_redis

healthRouter = APIRouter(prefix="/health")

@healthRouter.get("/app")
async def ping():
    return {"status" : "ok", "ping" : "pong"}

@healthRouter.get("/redis")
async def redisPing(rds: Redis = Depends(get_redis)):
    try:
        pong = await rds.ping()
        return {"status" : "healthy", "redis" : "connected", "ping" : pong}
    except Exception as e:
        return {"status" : "degraded", "redis" : f"Error: {e}"}