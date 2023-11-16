import psycopg2

class DBUtility:
    def __init__(self):
        self.db_init_flag = 0
        self.db = self.init_db()
    
    def init_db(self):
        db_connection = psycopg2.connect(
                            database="lichess_db",
                            host="localhost",
                            user="postgres",
                            password="admin",
                            port="5433")
        print("Connection Established Successfully")
        self.db_init_flag = 1
        return db_connection
    
    def close_db(self):
        if self.db_init_flag == 1:
            self.db_init_flag = 0
            self.db.close()
            del self.db
    
    def execute_query(self, query):
        if self.db_init_flag == 0:
            self.init_db()
        cursor = self.db.cursor()

        cursor.execute(query)
        self.db.commit()
        result = cursor.fetchall()
        return result
