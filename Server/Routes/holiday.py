from fastapi import APIRouter, Response, status
from Services.holidayService import get_existing_holidays, add_holidays, update_holidays
from Models.holiday import HolidayBody, HolidayResponse
from typing import List

holidayRouter = APIRouter(prefix="/holiday")

@holidayRouter.get("/existing", response_model=List[HolidayResponse])
async def getHolidays(body, response: Response):
    try:
        user_id = body['user_id']
        holidays = await get_existing_holidays(user_id)
        response.status_code = status.HTTP_200_OK
        return {"message": "Here are your current holidays", "data": holidays}
    except Exception as e:
        raise

@holidayRouter.post("/add")
async def addHolidays(body: HolidayBody, response: Response):
    try:
        user_id = body['user_id']
        holidays = await add_holidays(user_id)
        response.status_code = status.HTTP_200_OK
        return {"message": "Here are your holidays", "data": holidays}
    except Exception as e:
        raise

@holidayRouter.put("/update")
async def updateHolidays(body: HolidayBody, response: Response):
    try:
        user_id = body['user_id']
        holidays = await update_holidays(user_id)
        response.status_code = status.HTTP_200_OK
        return {"message": "Here are your updated holidays", "data": holidays}
    except Exception as e:
        raise