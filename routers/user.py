from fastapi import APIRouter
from models.user import *

user_router = APIRouter(prefix="/users", tags=["user"])