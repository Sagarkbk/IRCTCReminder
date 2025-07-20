from fastapi import APIRouter, status, Depends, HTTPException
from Services.journeyService import get_existing_journeys, add_journey, update_journey, delete_journey_by_id
from Middlewares.middlewares import authMiddleware
from fastapi_limiter.depends import RateLimiter
from Services.redisService import get_redis
from redis.asyncio import Redis

journeyRouter = APIRouter(prefix="/journey")

@journeyRouter.get("/existing", status_code = status.HTTP_200_OK, dependencies=[Depends(RateLimiter(times=60, seconds=60))])
async def getJourneys(user_id: int =  Depends(authMiddleware), rds: Redis = Depends(get_redis)):
    try:
        holidays = await get_existing_journeys(user_id, rds)
        return {"holidays": holidays}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

@journeyRouter.post("/add", status_code = status.HTTP_200_OK, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def addJourney(body, user_id: int =  Depends(authMiddleware), rds: Redis = Depends(get_redis)):
    try:
        if (not body.journey_name) or body.journey_name is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Journey Name is required")
        
        if (not body.journey_date) or body.journey_date is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Journey Date is required")
        
        if (body.remind_on_release_day is None) or (body.remind_on_day_before is None):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Reminder preferences for release day and day before release are required")
        
        holidays = await add_journey(body, user_id, rds)
        return {"holidays": holidays}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

@journeyRouter.put("/update", status_code = status.HTTP_200_OK, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def updateJourney(body, journey_id, user_id: int =  Depends(authMiddleware), rds: Redis = Depends(get_redis)):
    try:
        if (not body.journey_name) or body.journey_name is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Journey Name is required")
        
        if (not body.journey_date) or body.journey_date is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Journey Date is required")
        
        if (body.remind_on_release_day is None) or (body.remind_on_day_before is None):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Reminder preferences for release day and day before release are required")
                
        holidays = await update_journey(body, user_id, journey_id, rds)
        return {"holidays": holidays}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
    
@journeyRouter.delete("/delete", status_code=status.HTTP_200_OK, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def deleteJourney(journey_id, user_id: int =  Depends(authMiddleware), rds: Redis = Depends(get_redis)):
    try:
        holidays = await delete_journey_by_id(user_id, journey_id, rds)
        return {"holidays": holidays}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)