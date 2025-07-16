from fastapi import APIRouter, status, Depends, HTTPException
from Services.journeyService import get_existing_journeys, add_journeys, update_journeys
from Middlewares.middlewares import authMiddleware

journeyRouter = APIRouter(prefix="/journey")

@journeyRouter.get("/existing", status_code = status.HTTP_200_OK)
async def getHolidays(user_id: int =  Depends(authMiddleware)):
    try:
        holidays = await get_existing_journeys(user_id)
        return {"holidays": holidays}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

@journeyRouter.post("/add", status_code = status.HTTP_200_OK)
async def addHolidays(body, user_id: int =  Depends(authMiddleware)):
    try:
        if not(len(body.holiday_name)==len(body.holiday_date)==len(body.category)==
            len(body.day_before_sent)==len(body.release_day_sent)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Number of records not matching")
        holidays = await add_journeys(body, user_id)
        return {"holidays": holidays}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

@journeyRouter.put("/update", status_code = status.HTTP_200_OK)
async def updateHolidays(body, user_id: int =  Depends(authMiddleware)):
    try:
        if not(len(body.holiday_name)==len(body.holiday_date)==len(body.category)==
            len(body.day_before_sent)==len(body.release_day_sent)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Number of records not matching")
        holidays = await update_journeys(body, user_id)
        return {"holidays": holidays}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)