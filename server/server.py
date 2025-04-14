from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routeRegistrator import RouteRegistrator

class FastServer:
    
    def create_app(self):
        app = FastAPI(title="Gateway API")

        allowed_origins = ["http://127.0.0.1:5050"]
        app.add_middleware(
            CORSMiddleware,
            allow_origins=allowed_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @app.exception_handler(404)
        async def not_found_handler(request: Request, exc: HTTPException):
            return JSONResponse(status_code=404, content={"error": "404. Request not exists"})
        
        @app.exception_handler(502)
        async def server_not_started(request: Request, exc: HTTPException):
            return JSONResponse(status_code=502, content={"-_-": "Something went wrong. Respawn timer activated!"})
        
        @app.exception_handler(500)
        async def internal_server_error(request: Request, exc: HTTPException):
            return JSONResponse(status_code=500, content={"error": "Internal Server Error"})
        
        @app.middleware("http")
        async def custom_cors_middleware(request: Request, call_next):
            response = await call_next(request)
            origin = request.headers.get("origin")
            if origin in allowed_origins:
                response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, DELETE, PUT'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            return response
        
        registrator = RouteRegistrator(app)
        app = registrator.register_all()
        
        return app
    
app = FastServer().create_app()  
