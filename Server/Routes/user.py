from fastapi import APIRouter

userRouter = APIRouter(prefix="/user")

@userRouter.get("/profile")
async def getProfile():
    pass

@userRouter.put("/preferences")
async def updateProfile():
    pass