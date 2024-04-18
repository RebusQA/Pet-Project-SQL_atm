
from sql_query import SQL_atm


class ATM():

    def atm_logic(self):

        SQL_atm.create_table()
        # SQL_atm.insert_users((7777, 3333, 10000))
        """Проверяю что метод ввода карты работает"""
        number_cart = input("Введите номер карты: ")

        while True:
            if SQL_atm.input_card(number_cart):

                if SQL_atm.input_code(number_cart):
                    SQL_atm.info_balance(number_cart)
                    # SQL_atm.withdraw_money(number_cart)
                    SQL_atm.depositing_money(number_cart)
                    break
                else:
                    break
            else:
                break

start = ATM()
start.atm_logic()
