from fastapi import Request, Response, status
from Database.connection import db

async def user_auth_middleware(request: Request, response: Response):
    try:
        google_id_param = request.path_params.get("google_id")
        google_id_body = None
        body = None
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.json()
                google_id_body = body.get("google_id")
            except:
                pass
        google_id_body = None
        if body:
            google_id_body = body.get("google_id")
        google_id = google_id_param or google_id_body
        await db.connect()
        existing_user_query = """
                            SELECT * FROM users WHERE google_id = $1
                            """
        existing_user = await db.fetchone(existing_user_query, google_id)
        if not existing_user:
            return None
        return existing_user
    except Exception as e:
        print(f"Exception in middleware function: {e}")
        raise