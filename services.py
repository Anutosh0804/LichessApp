import traceback
from fastapi import APIRouter, HTTPException, Header, status, Body
from starlette.responses import JSONResponse, Response

router = APIRouter()


@router.get("/top-players")
def get_top_player():
    print("Top Player Fetched")


@router.get("/player/{username}/rating-history")
def get_player_rating_history(username):
    print(f"Rating History Fetched for {username}")


@router.get("/players/rating-history-csv")
def get_rating_history_csv():
    print("Generated Rating History CSV")
