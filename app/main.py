from fastapi import FastAPI
from dotenv import load_dotenv

from sqlmodel import SQLModel
from contextlib import asynccontextmanager

from app.db.session import engine
from app.api.routers import users, auth, transactions, categories



# import os

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code here
    SQLModel.metadata.create_all(engine)
    yield
    # Shutdown code here
    
    
app = FastAPI(title="Minty API", lifespan=lifespan)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(categories.router)



@app.get("/health")
def health():
    return {"ok": True}


    



