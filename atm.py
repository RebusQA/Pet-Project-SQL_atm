
from sql_qwery import SQL_atm


class ATM():

    def atm_logic(self):

        SQL_atm.create_table()
        # SQL_atm.insert_users((7777, 3333, 10000))

start = ATM()
start.atm_logic()
