import traceback
from fastapi import APIRouter, HTTPException, Header, status, Body
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse, Response
from starlette.requests import Request

from handler import Handler

router = APIRouter()

@router.get("/top-players")
def get_top_player(request: Request):
    try:
        response = Handler(db=request.state.db_session).get_top_player()
        return JSONResponse(status_code=200, content=jsonable_encoder(response))
    except HTTPException as err:
        return err

@router.get("/player/{username}/rating-history")
def get_player_rating_history(request: Request, username):
    try:
        response = Handler(db=request.state.db_session).get_player_rating_history(username)
        return JSONResponse(status_code=200, content=jsonable_encoder(response))
    except HTTPException as err:
        return err


@router.get("/players/rating-history-csv")
def get_rating_history_csv(request: Request):
    try:
        response = Handler(db=request.state.db_session).get_rating_history_csv()
        return JSONResponse(status_code=200, content=jsonable_encoder(response))
    except HTTPException as err:
        return err
