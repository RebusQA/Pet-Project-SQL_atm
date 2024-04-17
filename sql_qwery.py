
import sqlite3

class SQL_atm:

    """Создание таблицы User_data"""
    @staticmethod
    def create_table():
        with sqlite3.connect("atm.db") as db:
            cur = db.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS User_data(
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Number_card INTEGER NOT NULL,
            Pin_code INTEGER NOT NULL,
            Balance INTEGER NOT NULL);            
            """)
            print("Создание таблицы User_data")
