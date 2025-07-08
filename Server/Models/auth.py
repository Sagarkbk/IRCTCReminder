from pydantic import BaseModel

class GoogleAuth(BaseModel):
    idToken: str
    clientId: str