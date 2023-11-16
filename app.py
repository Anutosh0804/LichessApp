import uvicorn
from fastapi import FastAPI, status, HTTPException, Depends
# from services import router as services_router
from starlette.requests import Request
from starlette.middleware.cors import CORSMiddleware
import time
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
# from models import UserOut, UserAuth, TokenSchema
from replit import db
from auth import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password
)
from uuid import uuid4

from db_utility import DBUtility
import services
from queries import *
from deps import get_current_user

app = FastAPI()

api_dependencies = [Depends(get_current_user)]
app.include_router(services.router, dependencies=api_dependencies)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def read_root():
    return "Welcome to Lichess App"

@app.get("/health")
def get_health():
    return {"message": "OK"}

@app.middleware("http")
async def authorization(request: Request, call_next):
    start_time = time.time()
    endpoint = request.url.path
    if endpoint not in ['/', '/docs', '/favicon.ico', '/openapi.json']:
        db_session = DBUtility()
        request.state.db_session = db_session
    response = await call_next(request)
    end_time = time.time()
    process_time = end_time - start_time
    response.headers["X-Start-Time"] = str(start_time)
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-End-Time"] = str(end_time)
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Strict-Transport-Security'] = 'max-age=63072000; includeSubDomains; preload'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['Cache-Control'] = 'no-cache, no-store'
    response.headers['Pragma'] = 'no-cache'
    response.headers['server'] = 'XXXXX'
    return response


# @app.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # user = db.get(form_data.username, None)
    db_session = DBUtility()
    user = db_session.execute_query(GET_USERNAME % form_data.username)
    if len(user) == 0: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user[0][1]
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return {
        "access_token": create_access_token(user[0][0]),
        "refresh_token": create_refresh_token(user[0][0]),
    }


@app.post("/signup")
async def signup(username, password):
    # user = db.get(form_data.username, None)
    db_session = DBUtility()
    user = db_session.execute_query(GET_USERNAME % username)
    if len(user) == 0: 
        hashed_password = get_hashed_password(password)
        db_session.execute_insert(INSERT_USER_DETAILS % (username, hashed_password))
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    return {
        "message": "Create User Successfully"
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8081)
