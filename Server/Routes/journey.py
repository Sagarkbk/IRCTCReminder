from fastapi import APIRouter, status, Depends, HTTPException
from Services.journeyService import get_existing_journeys, add_journey, update_journey, delete_journey_by_id
from Middlewares.middlewares import authMiddleware

journeyRouter = APIRouter(prefix="/holiday")

@journeyRouter.get("/existing", status_code = status.HTTP_200_OK)
async def getJourneys(user_id: int =  Depends(authMiddleware)):
    try:
        holidays = await get_existing_journeys(user_id)
        return {"holidays": holidays}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

@journeyRouter.post("/add", status_code = status.HTTP_200_OK)
async def addJourney(body, user_id: int =  Depends(authMiddleware)):
    try:
        if (not body.journey_name) or body.journey_name is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Journey Name is required")
        
        if (not body.journey_date) or body.journey_date is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Journey Date is required")
        
        if (body.remind_on_release_day is None) or (body.remind_on_day_before is None):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Reminder preferences for release day and day before release are required")
        
        holidays = await add_journey(body, user_id)
        return {"holidays": holidays}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

@journeyRouter.put("/update", status_code = status.HTTP_200_OK)
async def updateJourney(body, journey_id, user_id: int =  Depends(authMiddleware)):
    try:
        if (not body.journey_name) or body.journey_name is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Journey Name is required")
        
        if (not body.journey_date) or body.journey_date is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Journey Date is required")
        
        if (body.remind_on_release_day is None) or (body.remind_on_day_before is None):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Reminder preferences for release day and day before release are required")
                
        holidays = await update_journey(body, user_id, journey_id)
        return {"holidays": holidays}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
    
@journeyRouter.delete("/delete", status_code=status.HTTP_200_OK)
async def deleteJourney(journey_id, user_id: int =  Depends(authMiddleware)):
    try:
        holidays = await delete_journey_by_id(user_id, journey_id)
        return {"holidays": holidays}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)