import json
import os
from datetime import datetime

class FinanceManager:
    def __init__(self, user):
        self.user = user
        self.transactions = user['data']['transactions']
        self.categories = {
            "Доходы": ["Зарплата", "Инвестиции", "Другое"],
            "Расходы": ["Еда", "Транспорт", "Жилье", "Развлечения", "Другое"]
        }

    def save_data(self):
        # Данные сохраняются через UserManager
        pass

    def add_transaction(self):
        print("\n=== Добавление транзакции ===")
        print("1. Доход")
        print("2. Расход")
        type_choice = input("Выберите тип транзакции: ")
        
        if type_choice not in ["1", "2"]:
            print("Неверный выбор")
            return
            
        transaction_type = "Доходы" if type_choice == "1" else "Расходы"
        
        print(f"\nДоступные категории {transaction_type}:")
        for i, category in enumerate(self.categories[transaction_type], 1):
            print(f"{i}. {category}")
            
        category_choice = input("Выберите категорию: ")
        try:
            category_index = int(category_choice) - 1
            if 0 <= category_index < len(self.categories[transaction_type]):
                category = self.categories[transaction_type][category_index]
            else:
                print("Неверный выбор категории")
                return
        except ValueError:
            print("Неверный ввод")
            return
            
        amount = float(input("Введите сумму: "))
        description = input("Введите описание: ")
        date = input("Введите дату (YYYY-MM-DD) [по умолчанию сегодня]: ") or datetime.now().strftime("%Y-%m-%d")
        
        transaction = {
            "type": transaction_type,
            "category": category,
            "amount": amount,
            "description": description,
            "date": date
        }
        
        self.transactions.append(transaction)
        print("Транзакция успешно добавлена")

    def view_history(self):
        if not self.transactions:
            print("Нет транзакций")
            return
            
        print("\n=== История транзакций ===")
        for item in self.transactions:
            print(f"[{item['date']}] {item['type'].capitalize()}: {item['amount']} - {item['category']} ({item['description']})")

    def menu(self):
        while True:
            print("\n=== Меню финансов ===")
            print("1. Добавить доход")
            print("2. Добавить расход")
            print("3. Просмотреть историю")
            print("0. Назад")
            choice = input("Выберите действие: ")

            if choice == "1":
                self.add_transaction()
            elif choice == "2":
                self.add_transaction()
            elif choice == "3":
                self.view_history()
            elif choice == "0":
                break
            else:
                print("Неверный выбор")
