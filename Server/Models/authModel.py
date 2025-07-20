from pydantic import BaseModel, field_validator

class GoogleAuth(BaseModel):
    idToken : str
    clientId: str