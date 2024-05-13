from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime
import uuid

router = APIRouter()

# 사용자 정보 모델
class User(BaseModel):
    name: str
    school: str


# 로그 모델
class Log(BaseModel):
    log_type: str
    log_data: Dict


# 사용자 정보 저장소
users = {}

# 로그 저장소
logs = []


@router.post("/user", response_model=User)
def create_user(user: User):
    user_id = str(uuid.uuid4())
    users[user_id] = user
    return {"user_id": user_id, **user.dict()}


@router.post("/users/{user_id}/logs", response_model=Log)
def create_log(user_id: str, log: Log):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    log_id = str(uuid.uuid4())
    log_entry = {
        "log_id": log_id,
        "user_id": user_id,
        "log_type": log.log_type,
        "log_data": log.log_data,
        "timestamp": datetime.now().isoformat()
    }
    logs.append(log_entry)
    return log_entry


@router.get("/users/{user_id}/logs", response_model=List[Log])
def get_user_logs(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    user_logs = [log for log in logs if log["user_id"] == user_id]
    return user_logs