import hashlib
from datetime import datetime
from random import random

from fastapi import HTTPException, FastAPI
from jwt import jwt

from file.main import SECRET_KEY, User, Token, users_db

app = FastAPI()

@app.post("/signup")
async def signup(user: User):
    hashed_password = hashlib.sha256(user.password.encode()).hexdigest()


    users_db[user.email] = {
        "email": user.email,
        "password": hashed_password,
        "subscription_type": "Free",
        "wallet_balance": 0
    }

    return {"message": "User registered successfully"}


@app.post("/signin", response_model=Token)
async def signin(user: User):
    stored_user = users_db.get(user.email)
    if not stored_user:
        raise HTTPException(status_code=404, detail="User not found")

    hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
    if hashed_password != stored_user['password']:
        raise HTTPException(status_code=400, detail="Incorrect password")


    token = jwt.encode(
        {"email": user.email, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        SECRET_KEY,
        algorithm="HS256"
    )

    return {"token": token}


@app.post("/generate-otp")
async def generate_otp(user: User):
    otp = random.randint(1000, 9999)
    print(f"Generated OTP: {otp}")
    return {"message": "OTP sent", "otp": otp}


