from fastapi import APIRouter

holidayRouter = APIRouter(prefix="/holiday")

@holidayRouter.get("/existing")
async def getHolidays():
    pass

@holidayRouter.post("/add")
async def addHolidays():
    pass

@holidayRouter.put("/update")
async def updateHolidays():
    pass