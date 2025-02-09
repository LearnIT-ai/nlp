from fastapi import APIRouter, Request, UploadFile, File
from fastapi.responses import JSONResponse
from AI_contorller import AiController
ai_access = APIRouter(prefix="/ai_chat")

@ai_access.post("/send_message")
async def create_chat(request: Request):
    body = await request.json()
    user_message = body.get("user_message")

    response = AiController.general_chat(user_message)

    return JSONResponse(content={"response": response}, status_code=200)

@ai_access.post("/check_homework_file")
async def check_homework_file(file: UploadFile = File(alias="homework")):
    
    response = AiController.check_homework_file(file)

    return JSONResponse(content={"response": response}, status_code=200)

@ai_access.post("/check_homework_text")
async def check_homework_text(request: Request):
    body = await request.json()
    task,answer = body.get("task"), body.get("answer")

    response = AiController.check_homework_text(task,answer)

    return JSONResponse(content={"response": response}, status_code=200)