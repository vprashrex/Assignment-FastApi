from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.router import blog
from fastapi.requests import Request

def init():
    VERSION = "0.1"

    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  
        allow_credentials=True,
        allow_methods=["*"],  
        allow_headers=["*"],  
    )

    app.get("/")
    async def root(request:Request):
        return {"status":"Server is Running"}
    
    app.include_router(blog.router)

app = init()