
from sql_qwery import SQL_atm


class ATM():

    def atm_logic(self):

        SQL_atm.create_table()
        # SQL_atm.insert_users((7777, 3333, 10000))
        """Проверяю что метод ввода карты работает"""
        number_card = input("Введите номер карты: ")

        while True:
            if SQL_atm.input_card(number_card):
                print("7777")
            else:
                break

start = ATM()
start.atm_logic()
