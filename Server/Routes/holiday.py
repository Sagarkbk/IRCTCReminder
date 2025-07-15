from fastapi import APIRouter, status, Depends, HTTPException
from Services.holidayService import get_existing_holidays, add_holidays, update_holidays
from Models.holiday import HolidayBody
from Middlewares.middlewares import authMiddleware

holidayRouter = APIRouter(prefix="/holiday")

@holidayRouter.get("/existing", status_code = status.HTTP_200_OK)
async def getHolidays(user_id: int =  Depends(authMiddleware)):
    try:
        holidays = await get_existing_holidays(user_id)
        return {"holidays": holidays}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

@holidayRouter.post("/add", status_code = status.HTTP_200_OK)
async def addHolidays(body: HolidayBody, user_id: int =  Depends(authMiddleware)):
    try:
        if not(len(body.holiday_name)==len(body.holiday_date)==len(body.category)==
            len(body.day_before_sent)==len(body.release_day_sent)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Number of records not matching")
        holidays = await add_holidays(body, user_id)
        return {"holidays": holidays}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

@holidayRouter.put("/update", status_code = status.HTTP_200_OK)
async def updateHolidays(body: HolidayBody, user_id: int =  Depends(authMiddleware)):
    try:
        if not(len(body.holiday_name)==len(body.holiday_date)==len(body.category)==
            len(body.day_before_sent)==len(body.release_day_sent)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Number of records not matching")
        holidays = await update_holidays(body, user_id)
        return {"holidays": holidays}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)