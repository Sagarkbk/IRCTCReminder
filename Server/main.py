from fastapi import FastAPI
from Routes.auth import authRouter
from Routes.user import userRouter
from Routes.holiday import holidayRouter
from Routes.integration import integrationRouter

app = FastAPI()

app.include_router(authRouter, prefix="/api")
app.include_router(userRouter, prefix="/api")
app.include_router(holidayRouter, prefix="/api")
app.include_router(integrationRouter, prefix="/api")