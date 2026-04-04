from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.auth_routes import router as auth_router
from src.api.user_routes import router as user_router
from src.api.task_routes import router as task_router, simple_router as simple_task_router
from src.api.chat import router as chat_router
from contextlib import asynccontextmanager
from src.database import engine
from src.models.user import User
from src.models.task import Task
from src.models.conversation import Conversation, Message
from sqlmodel import SQLModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    SQLModel.metadata.create_all(bind=engine)
    yield
    # Cleanup on shutdown if needed
    pass

app = FastAPI(
    title="Multi-User Todo API",
    description="API for the multi-user todo web application with JWT authentication",
    version="0.1.0",
    lifespan=lifespan
)

# Add CORS middleware BEFORE including routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers (routers have their own prefixes defined)
app.include_router(auth_router)  # /auth/*
app.include_router(user_router)  # /users/*
app.include_router(task_router)  # /tasks/*
app.include_router(simple_task_router)  # /tasks-simple/*
app.include_router(chat_router)  # /api/* (AI chat endpoints)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Multi-User Todo API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}