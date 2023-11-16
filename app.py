import uvicorn
from fastapi import FastAPI
from services import router as services_router

app = FastAPI()

app.include_router(services_router)


@app.get("/")
def main_page():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)
