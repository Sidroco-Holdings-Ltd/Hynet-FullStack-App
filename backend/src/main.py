import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import example_router
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

api_title = os.getenv("API_TITLE", "Hynet REST API")
app = FastAPI(title=api_title)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(example_router)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn_host = os.getenv("UVICORN_HOST", "0.0.0.0")
    uvicorn_port = int(os.getenv("UVICORN_PORT", 8000))

    uvicorn.run(app, host=uvicorn_host, port=uvicorn_port) 
