from fastapi import APIRouter

integrationRouter = APIRouter(prefix="/user")

@integrationRouter.post("/telegram/generateToken")
async def generateToken():
    pass

@integrationRouter.put("/telegram/linkAccount")
async def linkTelegramAccount():
    pass