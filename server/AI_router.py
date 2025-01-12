from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse
from AI_contorller import AiController

ai_access = APIRouter(prefix="/ai_chat")

@ai_access.post("/send_message")
async def create_chat(request: Request):
    body = await request.json()
    
    user_message = body.get("user_message")

    response = AiController.main_flan_t5(user_message)
    return JSONResponse(content ={"response": response},status_code=200)