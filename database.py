from peewee import Model, ForeignKeyField, CharField, PostgresqlDatabase, FloatField, DateTimeField
import csv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table

from datetime import datetime

db = PostgresqlDatabase('finance', user='postgres', password='12345678', host='127.0.0.1')


class Account(Model):
    name = CharField()
    balance = FloatField()

    class Meta:
        database = db


class Transaction(Model):
    account = ForeignKeyField(Account, backref='transactions')
    amount = FloatField()
    description = CharField()
    date = DateTimeField(default=datetime.now())

    class Meta:
        database = db


def main():
    db.connect()
    db.create_tables([Account, Transaction])

    # Account.create(name='Talant', balance=1000.0)
    #
    # Account.create(name='Bahtyar', balance=100.0)
    #
    # Account.create(name='Nazgul', balance=34)
    #
    # Account.create(name='Dastan', balance=1000.0)
    #
    # Account.create(name='Anya', balance=1000.0)

    def main_menu():
        while True:
            print("Главное меню:")
            print("1. Добавить транзакцию")
            print("2. Просмотреть общий баланс")
            print("3. Получить отчет")
            print("4. Выйти")

            choice = input("Выберите действие (1/2/3/4): ")

            if choice == '1':
                add_transaction_menu()
            elif choice == '2':
                view_balance()
            elif choice == '3':
                generate_report()

            elif choice == '4':
                print("Выход из приложения.")
                break
            else:
                print("Неверный выбор. Пожалуйста, выберите 1, 2 или 3.")

    def add_transaction_menu():
        while True:
            print("Добавление транзакции:")
            print("1. Доход")
            print("2. Расход")
            print("3. Назад")

            choice = input("Выберите тип транзакции (1/2/3): ")

            if choice == '1':
                add_income()
            elif choice == '2':
                add_expense()
            elif choice == '3':
                break
            else:
                print("Неверный выбор. Пожалуйста, выберите 1, 2 или 3.")

    def add_income():
        account_name = input("Введите имя счета: ")
        amount = float(input("Введите сумму дохода: "))
        description = input("Введите описание дохода: ")

        try:
            account = Account.get(Account.name == account_name)
            Transaction.create(account=account, amount=amount, description=description,
                               date=datetime.now())
            account.balance += amount
            account.save()
            print("Доход успешно добавлен.")
        except Account.DoesNotExist:
            print("Счет не найден. Пожалуйста, убедитесь, что счет с таким именем существует.")

    def add_expense():
        account_name = input("Введите имя счета: ")
        amount = float(input("Введите сумму расхода: "))
        description = input("Введите описание расхода: ")

        try:
            account = Account.get(Account.name == account_name)
            Transaction.create(account=account, amount=-amount, description=description,
                               date=datetime.now())
            account.balance -= amount
            account.save()
            print("Расход успешно добавлен.")
        except Account.DoesNotExist:
            print("Счет не найден. Пожалуйста, убедитесь, что счет с таким именем существует.")

    def view_balance():
        account_name = input("Введите имя счета: ")
        print()

        try:
            account = Account.get(Account.name == account_name)
            print(f"Баланс счета {account.name}: {account.balance}")
        except Account.DoesNotExist:
            print("Счет не найден. Пожалуйста, убедитесь, что счет с таким именем существует.")

    def generate_report():

        account_name = input("Введите имя счета: ")
        format_choice = input("Выберите формат отчета (csv или pdf) : ")
        filename = input("Введите имя файла для сохранения отчета: ")

        try:

            account = Account.get(Account.name == account_name)

            if format_choice == "csv":
                transactions = Transaction.select().where(Transaction.account == account)
                report_data = [["Дата", "Описание", "Сумма"]]

                for transaction in transactions:
                    report_data.append([transaction.date, transaction.description, transaction.amount])

                with open(filename, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(report_data)

                print(f"CSV-отчет сохранен в файл: {filename}")

            elif format_choice == "pdf":
                transactions = Transaction.select().where(Transaction.account == account)
                data = [["Дата", "Описание", "Сумма"]]

                for transaction in transactions:
                    data.append([str(transaction.date), transaction.description, str(transaction.amount)])

                doc = SimpleDocTemplate(filename, pagesize=letter)
                table = Table(data)

                doc.build([table])

                print(f"PDF-отчет сохранен в файл: {filename}")

            else:

                print("Неподдерживаемый формат отчета.")
        except Account.DoesNotExist:
            print("Счет не найден. Пожалуйста, убедитесь, что счет с таким именем существует.")

    if __name__ == "__main__":
        main_menu()


if __name__ == '__main__':
    main()
