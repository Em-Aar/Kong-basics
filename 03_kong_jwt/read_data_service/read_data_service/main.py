from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel
from jose import jwt
import httpx


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("read data services started")
    yield

app = FastAPI(lifespan=lifespan, title="read data services")


class TokenData(SQLModel):
    iss: str


# SECRET_KEY = "DPZau2JXU0OnZXMYKjgOOAQbXgGRNknZ"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 2


def get_secret_from_kong(consumer_id: str) -> str:
    with httpx.Client() as client:
        print(f'consumer_id: {consumer_id}')
        url = f"http://kong:8001/consumers/{consumer_id}/jwt"
        response = client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code,
                                detail="Failed to fetch secret from Kong")
        kong_data = response.json()
        print(f'Kong Data: {kong_data}')
        if not kong_data['data'][0]["secret"]:
            raise HTTPException(
                status_code=404, detail="No JWT credentials found for the specified consumer")

        secret = kong_data['data'][0]["secret"]
        print(f'Secret: {secret}')
        return secret


def create_jwt_token(data: dict, secret: str):
    to_encode = data.copy()
    expire = datetime.utcnow() + \
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Limit expiration time to 2038-01-19 03:14:07 UTC
    expire = min(expire, datetime(2038, 1, 19, 3, 14, 7))
    to_encode.update({"exp": expire})
    headers = {
        "typ": "JWT",
        "alg": ALGORITHM
    }
    encoded_jwt = jwt.encode(to_encode, secret,
                             algorithm=ALGORITHM, headers=headers)
    return encoded_jwt


@app.post("/generate-token/")
async def generate_token(data: TokenData, consumer_id: str):
    secret = get_secret_from_kong(consumer_id)
    payload = {"iss": data.iss}
    token = create_jwt_token(payload, secret)
    return {"token": token}
