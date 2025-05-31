import os
from fastapi.responses import FileResponse
from fastapi import APIRouter, Request, HTTPException, Query
default_router = APIRouter(prefix="/default")




@default_router.get("/get_silabus")
async def get_user_avatar(request: Request, filename:str=Query(alias="filename")):
    if not filename:
        raise HTTPException(detail="Filename can not be empty.",status_code=400)

    user_server_path = f"static/simple_silabus_generated/{filename}"
    if not os.path.exists(user_server_path) or not os.path.isfile(user_server_path):
        raise HTTPException(detail="File not founded.",status_code=400)
    else:
        server_path = user_server_path

    return FileResponse(path=server_path, filename=filename)