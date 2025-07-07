from pydantic import BaseModel

class GoogleAuth:
    idToken: str;
    clientId: str;