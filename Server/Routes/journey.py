from fastapi import APIRouter, status, Depends, HTTPException
from Services.journeyService import get_existing_journeys, add_journey, update_journey, delete_journey_by_id, get_journey_stats
from Middlewares.middlewares import authMiddleware
from fastapi_limiter.depends import RateLimiter
from Services.redisService import get_redis
from redis.asyncio import Redis
from Models.journeyModel import JourneyInput

journeyRouter = APIRouter(prefix="/journey")

@journeyRouter.get("/existing", status_code = status.HTTP_200_OK, dependencies=[Depends(RateLimiter(times=60, seconds=60))])
async def getJourneys(user_id: int =  Depends(authMiddleware), rds: Redis = Depends(get_redis)):
    try:
        journeys = await get_existing_journeys(user_id, rds)
        return {"data": journeys}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@journeyRouter.post("/add", status_code = status.HTTP_200_OK, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def addJourney(body: JourneyInput, user_id: int =  Depends(authMiddleware), rds: Redis = Depends(get_redis)):
    try:        
        journey = await add_journey(body, user_id, rds)
        return {"data": journey}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@journeyRouter.put("/update", status_code = status.HTTP_200_OK, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def updateJourney(body: JourneyInput, journey_id: int, user_id: int =  Depends(authMiddleware), rds: Redis = Depends(get_redis)):
    try:
        journey = await update_journey(body, user_id, journey_id, rds)
        return {"data": journey}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
@journeyRouter.delete("/delete", status_code=status.HTTP_200_OK, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def deleteJourney(journey_id: int, user_id: int =  Depends(authMiddleware), rds: Redis = Depends(get_redis)):
    try:
        journeys = await delete_journey_by_id(user_id, journey_id, rds)
        return {"data": journeys}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
@journeyRouter.get("/journeyStats", status_code = status.HTTP_200_OK, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def journeyStats(user_id: int = Depends(authMiddleware)):
    try:
        stats = await get_journey_stats(user_id)
        return {"data" : stats}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")