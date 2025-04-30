import json
import os
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt

class Analytics:
    def __init__(self, user):
        self.user = user
        self.transactions = user['data']['transactions']
        self.goals = user['data']['goals']

    def get_category_stats(self):
        print("\n=== Статистика по категориям ===")
        income_by_category = defaultdict(float)
        expenses_by_category = defaultdict(float)
        
        for transaction in self.transactions:
            if transaction['type'] == 'Доходы':
                income_by_category[transaction['category']] += transaction['amount']
            else:
                expenses_by_category[transaction['category']] += transaction['amount']
        
        print("\nДоходы по категориям:")
        for category, amount in income_by_category.items():
            print(f"{category}: {amount}")
            
        print("\nРасходы по категориям:")
        for category, amount in expenses_by_category.items():
            print(f"{category}: {amount}")

    def get_monthly_stats(self):
        print("\n=== Ежемесячная статистика ===")
        current_month = datetime.now().strftime("%Y-%m")
        monthly_income = 0
        monthly_expenses = 0
        
        for transaction in self.transactions:
            if transaction['date'].startswith(current_month):
                if transaction['type'] == 'Доходы':
                    monthly_income += transaction['amount']
                else:
                    monthly_expenses += transaction['amount']
        
        print(f"\nДоходы за {current_month}: {monthly_income}")
        print(f"Расходы за {current_month}: {monthly_expenses}")
        print(f"Баланс: {monthly_income - monthly_expenses}")

    def get_goals_progress(self):
        print("\n=== Прогресс целей ===")
        if not self.goals:
            print("Нет целей")
            return
            
        for goal in self.goals:
            progress = (goal['current_amount'] / goal['target_amount']) * 100
            status = "Выполнено" if goal['completed'] else "В процессе"
            print(f"\nЦель: {goal['name']}")
            print(f"Прогресс: {progress:.1f}%")
            print(f"Статус: {status}")

    def category_analysis(self):
        summary = defaultdict(float)
        for transaction in self.transactions:
            if transaction['type'] == 'Расходы':
                summary[transaction['category']] += transaction['amount']
        print("\nАнализ по категориям расходов:")
        for cat, amt in summary.items():
            print(f"{cat}: {amt:.2f}")
        self.plot_pie_chart(summary)

    def plot_pie_chart(self, summary):
        if not summary:
            print("Нет данных для построения графика")
            return
            
        categories = list(summary.keys())
        values = list(summary.values())
        plt.figure(figsize=(8, 8))
        plt.pie(values, labels=categories, autopct='%1.1f%%')
        plt.title("Категории расходов")
        plt.show()

    def recommend(self):
        entertainment = sum(t['amount'] for t in self.transactions 
                          if t['type'] == 'Расходы' and t['category'].lower() == 'развлечения')
        total = sum(t['amount'] for t in self.transactions if t['type'] == 'Расходы')
        
        if total and entertainment / total > 0.3:
            print("Рекомендация: Вы тратите слишком много на развлечения. Попробуйте сократить эти расходы.")

    def menu(self):
        while True:
            print("\n=== Меню аналитики ===")
            print("1. Статистика по категориям")
            print("2. Ежемесячная статистика")
            print("3. Прогресс целей")
            print("4. Анализ расходов (график)")
            print("5. Рекомендации")
            print("0. Назад")
            choice = input("Выберите действие: ")

            if choice == "1":
                self.get_category_stats()
            elif choice == "2":
                self.get_monthly_stats()
            elif choice == "3":
                self.get_goals_progress()
            elif choice == "4":
                self.category_analysis()
            elif choice == "5":
                self.recommend()
            elif choice == "0":
                break
            else:
                print("Неверный выбор")
