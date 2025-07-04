from fastapi import Response, status, Request, HTTPException
from Database.connection import db

async def user_verification(request: Request, response: Response):
    if request.url.path.endswith("/users/addUser"):
        return
    
    google_id = request.path_params.get("google_id")

    if not google_id and request.method in ["POST", "PUT", "PATCH"]:
        try:
            body = await request.json()
            google_id = body.get("google_id")
        except:
            pass
    
    if not google_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Provide google_id")
    
    await db.connect()
    try:
        user = await db.fetchone("SELECT * FROM users WHERE google_id = $1", google_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        request.state.user = user
    except Exception as e:
        print(f"Exception in middleware: {e}")
        raise
