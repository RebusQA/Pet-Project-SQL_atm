
import sqlite3

class SQL_atm:

    """Создание таблицы Users_data"""
    @staticmethod
    def create_table():
        with sqlite3.connect("atm.db") as db:
            cur = db.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS Users_data(
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Number_card INTEGER NOT NULL,
            Pin_code INTEGER NOT NULL,
            Balance INTEGER NOT NULL);            
            """)
            print("Создание таблицы Users_data")


    """Создание нового пользователя"""
    @staticmethod
    def insert_users(data_users):
        with sqlite3.connect("atm.db") as db:
            cur = db.cursor()
            cur.execute("""INSERT INTO Users_data (Number_card, Pin_code, Balance) VALUES(?, ?,  ?);""", data_users)
            print("Создание нового пользователя")


    """Ввод и проверка карты"""
    @staticmethod
    def input_card(number_card):
        try:
            with sqlite3.connect("atm.db") as db:
                cur = db.cursor()
                cur.execute(f"""SELECT Number_card FROM Users_data WHERE Number_card = {number_card}""")
                result_card = cur.fetchone()

                """Логика проверки номера карты"""
                if result_card is None:
                    print("Введён неизвестный номер карты")
                    return False
                else:
                    print(f"Введён номер карты: {number_card}")
                    return True
        except:
            print("Введён неизвестный номер карты")
