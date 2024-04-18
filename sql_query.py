
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


    """Ввод и проверка пин-кода"""
    @staticmethod
    def input_code(number_card):
        pin_code = input("Введите пин-код карты: ")
        with sqlite3.connect("atm.db") as db:
            cur = db.cursor()
            cur.execute(f"""SELECT Pin_code FROM Users_data WHERE Number_card = {number_card}""")
            result_code = cur.fetchone()
            input_pin = result_code[0]
            try:
                if input_pin == int(pin_code):
                    print("Введён верный пин-код")
                    return True
                else:
                    print("Введён некорректный пин-код")
                    return False
            except:
                print("Введён некорректный пин-код")
                return False


    """Вывод на экран баланса карты"""
    @staticmethod
    def info_balance(number_card):
        with sqlite3.connect("atm.db") as db:
            cur = db.cursor()
            cur.execute(f"""SELECT Balance FROM Users_data WHERE Number_card = {number_card}""")
            result_info_balance = cur.fetchone()
            balance_cart = result_info_balance[0]
            print(f"Баланс карты: {balance_cart}")


    """Снятие денег с карты"""
    @staticmethod
    def withdraw_money(number_card):
        amount = input("Введите сумму, которую хотите снять: ")
        with sqlite3.connect("atm.db") as db:
            cur = db.cursor()
            cur.execute(f"""SELECT Balance FROM Users_data WHERE Number_card = {number_card}""")
            result_info_balance = cur.fetchone()
            balance_cart = result_info_balance[0]
            try:
                if int(amount) > balance_cart:
                    print("На карте недостаточно денег")
                    return False
                else:
                    cur.execute(f"""UPDATE Users_data SET Balance = Balance - {amount} WHERE Number_card = {number_card}""")
                    db.commit()
                    SQL_atm.info_balance(number_card)
                    return True
            except:
                print("Попытка выполнить некорректное действие")
                return False


    """Внесение денег на баланс карты"""
    @staticmethod
    def depositing_money(number_card):
        with sqlite3.connect("atm.db") as db:
            try:
                recipient_card = input("Введите номер карты, на которую хотите внести деньги: ")
                if not recipient_card.isdigit():
                    print("Некорректный номер карты. Номер карты должен содержать только цифры.")
                    return False

                amount = int(input("Введите сумму, которую хотите внести: "))
                if amount <= 0:
                    print("Сумма внесения должна быть положительным числом.")
                    return False

                cur = db.cursor()
                cur.execute(f"""SELECT Number_card FROM Users_data WHERE Number_card = {recipient_card}""")
                result_card = cur.fetchone()
                if result_card is None:
                    print("Введенный номер карты не существует.")
                    return False

                cur.execute(f"""UPDATE Users_data SET Balance = Balance + {amount} WHERE Number_card = {number_card}""")
                db.commit()
                SQL_atm.info_balance(number_card)
                return True
            except ValueError:
                print("Некорректная сумма внесения. Введите число.")
                return False
            except sqlite3.Error:
                print("Произошла ошибка при выполнении запроса. Введите корректный запрос.")
                return False


    """Выбор операции по карте"""
    @staticmethod
    def input_operation(number_card):
        while True:
            operation = input("Введите операцию, которую хотите совершить: \n"
                              "1. Узнать баланс\n"
                              "2. Снять деньги\n"
                              "3. Внести деньги\n"
                              "4. Перевести денежные средства\n"
                              "5. Завершить работу\n")
            if operation == "1":
                SQL_atm.info_balance(number_card)

            elif operation == "2":
                SQL_atm.withdraw_money(number_card)

            elif operation == "3":
                SQL_atm.depositing_money(number_card)

            elif operation == "4":
                recipient_card = input("Введите номер карты, на которую хотите перевести деньги: ")
                if not recipient_card.isdigit():
                    print("Некорректный номер карты. Номер карты должен содержать только цифры.")
                    continue
                SQL_atm.transfer_money(number_card, recipient_card)

            elif operation == "5":
                print("Всего доброго.")
                return False
            else:
                print("Данная операция недоступна")

    """Перевод денег между картами"""
    @staticmethod
    def transfer_money(sender_card, recipient_card):
        try:
            amount = int(input("Введите сумму, которую хотите перевести: "))
            if amount <= 0:
                print("Сумма перевода должна быть положительным числом.")
                return False

            with sqlite3.connect("atm.db") as db:
                cur = db.cursor()
                # Проверяю достаточность средств на счете отправителя
                cur.execute(f"""SELECT Balance FROM Users_data WHERE Number_card = {sender_card}""")
                sender_balance = cur.fetchone()[0]
                if sender_balance < amount:
                    print("На вашем счете недостаточно средств для перевода.")
                    return False
                # Обновляю балансы обеих карт
                cur.execute(f"""UPDATE Users_data SET Balance = Balance - {amount} WHERE Number_card = {sender_card}""")
                cur.execute(
                    f"""UPDATE Users_data SET Balance = Balance + {amount} WHERE Number_card = {recipient_card}""")
                db.commit()
                print("Перевод выполнен успешно.")
                return True
        except ValueError:
            print("Некорректная сумма перевода. Введите число.")
            return False
        except sqlite3.Error as e:
            print("Произошла ошибка при выполнении перевода:", e)
            return False
