from fastapi import FastAPI
from Routes.users import usersRouter
from Routes.telegram import telegramRouter

app = FastAPI()

@app.get("/")
def root():
    return "Root App"

app.include_router(usersRouter)
app.include_router(telegramRouter)