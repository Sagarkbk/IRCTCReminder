from pydantic import BaseModel, field_validator

class GoogleAuth(BaseModel):
    authCode : str
    clientId: str