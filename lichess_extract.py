import berserk
import requests
from datetime import datetime, date as today_date
import psycopg2
import json

API_TOKEN = "lip_9OlTGSB82eqAHUzGEOO3"

create_table_query = """
CREATE TABLE IF NOT EXISTS user_details (
  username VARCHAR(255),
  current_rating INT,
  oldest_rating INT,
  rating_history JSONB
);
"""

delete_user_data = """
DELETE FROM user_details;
"""

insert_user_data = """
INSERT INTO 
    user_details (username, current_rating, oldest_rating, rating_history)
VALUES
    (%s,  %s::int, %s::int, %s);
"""

headers = {
    'Authorization': f'Bearer {API_TOKEN}',
}


class LichessExtract:
    def __init__(self):
        self.session = berserk.TokenSession(API_TOKEN)
        self.client = berserk.Client(session=self.session)

        #TODO: create connection
        self. conn = psycopg2.connect(
                            database="lichess_db",
                            host="localhost",
                            user="postgres",
                            password="admin",
                            port="5433")
        self.cursor = self.conn.cursor()

    def get_top_n_players(self, player_count=50, perf_type='classical'):
        top_player_list = list()
        player_list_result = requests.get(
            f'https://lichess.org/api/player/top/{player_count}/{perf_type}', headers=headers)
        player_list = player_list_result.json()["users"]

        for player in player_list:
            username = player["username"]
            curr_rating = player["perfs"]["classical"]["rating"]
            top_player_list.append(
                {"username": username, "current_rating": curr_rating})

        return top_player_list

    def get_n_day_player_history(self, username, perf_type='Classical'):
        rating_history = list()

        player_rating_history_result = requests.get(
            f'https://lichess.org/api/user/{username}/rating-history', headers=headers
        )

        player_rating_history = player_rating_history_result.json()

        player_rating_list = [
            d for d in player_rating_history if d['name'] == perf_type]
        player_rating_list = player_rating_list[0]['points']

        player_rating_list = player_rating_list[::-1]
        player_rating_list = player_rating_list[:30]

        date_today = today_date.today()
        date_min = 31
        oldest_rating = player_rating_list[0][-1]
        for rating in player_rating_list:
            date = rating[:-1]
            date = [str(x) for x in date]
            date = '/'.join(date)
            try:
                date = datetime.strptime(date, '%Y/%m/%d').date()
                date_diff = (date_today - date).days
                date_rating = rating[-1]
                if date_diff < date_min:
                    date_min = date_diff
                    oldest_rating = date_rating
                rating_history.append(
                    {'date': date.strftime("%Y/%m/%d"), 'rating': date_rating})
            except:
                pass
        return rating_history, oldest_rating

    def create_tables(self):
        print("Starting to Create Table using query: \n", create_table_query)
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def insert_data_into_db(self, top_player_list):
        self.cursor.execute(delete_user_data)
        for player in top_player_list:
            username = player['username']
            current_rating = int(player['current_rating'])
            oldest_rating = int(player['oldest_rating'])
            rating_history = player['rating_history']
            self.cursor.execute(insert_user_data, (username, current_rating, oldest_rating, json.dumps(rating_history)))
        self.conn.commit()

    def run(self):
        print("Getting Top Player Lists")
        top_player_list = self.get_top_n_players()
        for player in top_player_list:
            username = player['username']
            print(f"Getting History For User: {username}")
            rating_history, oldest_rating = self.get_n_day_player_history(username)
            player['oldest_rating'] = oldest_rating
            player['rating_history'] = rating_history
        self.create_tables()
        print("Inserting Data into DB")
        self.insert_data_into_db(top_player_list)

if __name__ == '__main__':
    LichessExtract().run()
