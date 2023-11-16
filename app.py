import uvicorn
from fastapi import FastAPI
# from services import router as services_router
from starlette.requests import Request
from starlette.middleware.cors import CORSMiddleware
import time

from db_utility import DBUtility
import services

app = FastAPI()

app.include_router(services.router)

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
    return {"Hello": "World"}

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


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8081)
