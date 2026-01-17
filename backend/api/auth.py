from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from model import UserSignup, UserLogin, Token, UserResponse
from core.security import verify_password, get_password_hash, create_access_token, decode_token
from database import users_collection
from datetime import datetime
import uuid

router = APIRouter()
security = HTTPBearer()

@router.post("/signup", response_model=Token)
async def signup(user_data: UserSignup):
    
    existing_user = users_collection.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    user_id = str(uuid.uuid4())
    hashed_password = get_password_hash(user_data.password)
    
    new_user = {
        "_id": user_id,
        "email": user_data.email,
        "name": user_data.name,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow()
    }
    
    users_collection.insert_one(new_user)
    
    # Create token
    access_token = create_access_token(data={"sub": user_id})
    
    return {
        "token": access_token,
        "user": {
            "id": user_id,
            "email": user_data.email,
            "name": user_data.name
        }
    }

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    user = users_collection.find_one({"email": credentials.email})
    
    if not user or not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user["_id"]})
    
    return {
        "token": access_token,
        "user": {
            "id": user["_id"],
            "email": user["email"],
            "name": user["name"]
        }
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("sub")
    user = users_collection.find_one({"_id": user_id})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user["_id"],
        "email": user["email"],
        "name": user["name"]
    }