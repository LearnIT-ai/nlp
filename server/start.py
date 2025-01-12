from dotenv import load_dotenv
import os
import subprocess


if __name__ == '__main__':
        load_dotenv()
        port = os.getenv("GATEWAY_PORT")
        host = os.getenv("GATEWAY_HOST")
        from server import FastServer
        server = FastServer()
        module_name = "server:app"  
        workers = 1
        uvicorn_command = [
        "uvicorn",
        module_name,
        "--host", host,
        "--port", str(port),
        "--workers", str(workers),
    ]
        subprocess.run(uvicorn_command)