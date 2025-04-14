from fastapi import APIRouter, Request, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse
from AI_controller import AiController

ai_access = APIRouter(prefix="/ai_chat")

@ai_access.post("/send_message")
async def create_chat(request: Request):
    body = await request.json()
    user_message = body.get("user_message")

    response = AiController().general_chat(user_message)

    return JSONResponse(content={"response": response}, status_code=200)

@ai_access.post("/check_homework_file")
async def check_homework_file(file: UploadFile = File(alias="homework")):
    
    response = AiController().check_homework_file(file)

    return JSONResponse(content={"response": response}, status_code=200)

@ai_access.post("/check_homework_text")
async def check_homework_text(request: Request):
    body = await request.json()
    task,answer = body.get("task"), body.get("answer")

    response = AiController().check_homework_text(task,answer)

    return JSONResponse(content={"response": response}, status_code=200)

@ai_access.post("/get_homework_feedback")
async def get_homework_feedback(request: Request):
    body = await request.json()
    task,answer = body.get("task"), body.get("answer")

    response = AiController().get_homework_feedback(task,answer)

    return JSONResponse(content={"response": response}, status_code=200)


@ai_access.post("/get_texts_similarity")
async def check_homework_text(request: Request):
    body = await request.json()
    user_answer,model_answer = body.get("user_answer"), body.get("model_answer")

    response = AiController.get_texts_similarity(user_answer, model_answer)

    return JSONResponse(content={"response": response}, status_code=200)

@ai_access.post("/get_files_similarity")
async def check_homework_text(user_file: UploadFile = File(alias="user_file"), model_file: UploadFile = File(alias="model_file")):
    response = AiController.get_files_similarity(user_file, model_file)

    return JSONResponse(content={"response": response}, status_code=200)

@ai_access.post("/answer_by_file")
async def answer_by_file(file: UploadFile = File(alias="file"),question: str = Query(alias="question")):
    print(question)
    if not question or question is None:
        raise HTTPException(detail="Error: Question is required.",status_code=400)
    
    if not isinstance(question, str):
        raise HTTPException(detail="Error: Question must be a string.",status_code=400)

    response = AiController().answer_by_file(file,question)

    return JSONResponse(content={"response": response}, status_code=200)