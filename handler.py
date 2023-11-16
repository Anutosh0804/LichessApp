from fastapi import HTTPException
from queries import *

class Handler:
    def __init__(self, db):
        self.db = db
    
    def get_top_player(self):
        response = list()
        try:
            top_player_response = self.db.execute_query(GET_TOP_PLAYERS)
            if top_player_response:
                for player in top_player_response:
                    username = player[0]
                    current_rating = player[1]
                    response.append(
                        {
                            "username": username,
                            "current_rating": current_rating
                        }
                    )
            return response

        except HTTPException as err:
            raise HTTPException(status_code=err.status_code, detail=str(err.detail)) from err
        
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    def get_player_rating_history(self, username):
        response = list()
        try:
            history_player_response = self.db.execute_query(GET_PLAYER_HISTORY % username)
            if history_player_response:
                history_player_response = history_player_response[0]
                username = history_player_response[0]
                history_rating = history_player_response[-1]
                response.append(
                    {
                        "username": username,
                        "history_rating": history_rating
                    }
                )
            return response
        
        except HTTPException as err:
            raise HTTPException(status_code=err.status_code, detail=str(err.detail)) from err
        
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err
    
    def get_rating_history_csv(self):
        response = list()
        try:
            player_response = self.db.execute_query(GET_TOP_PLAYERS)
            if player_response:
                for player in player_response:
                    username = player[0]
                    oldest_rating = player[2]
                    history_rating = player[3]
                    response.append({"username": username,"oldest_rating": oldest_rating,"history_rating": history_rating})
            return response
       
        except HTTPException as err:
            raise HTTPException(status_code=err.status_code, detail=str(err.detail)) from err
        
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err
