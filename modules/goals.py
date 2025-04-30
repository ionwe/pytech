import json
import os
from datetime import datetime

class GoalManager:
    def __init__(self, user):
        self.user = user
        self.goals = user['data']['goals']

    def save_data(self):
        # Данные сохраняются через UserManager
        pass

    def add_goal(self):
        print("\n=== Добавление цели ===")
        name = input("Название цели: ")
        target_amount = float(input("Целевая сумма: "))
        current_amount = float(input("Текущая сумма: "))
        deadline = input("Срок (YYYY-MM-DD): ")
        
        goal = {
            "name": name,
            "target_amount": target_amount,
            "current_amount": current_amount,
            "deadline": deadline,
            "completed": False
        }
        
        self.goals.append(goal)
        print("Цель успешно добавлена")

    def add_progress(self):
        if not self.goals:
            print("Нет целей")
            return
            
        print("\n=== Добавление прогресса ===")
        for i, goal in enumerate(self.goals, 1):
            progress = (goal['current_amount'] / goal['target_amount']) * 100
            print(f"{i}. {goal['name']} - {goal['current_amount']}/{goal['target_amount']} ({progress:.1f}%)")
            
        try:
            goal_index = int(input("Выберите цель: ")) - 1
            if 0 <= goal_index < len(self.goals):
                amount = float(input("Введите сумму для добавления: "))
                self.goals[goal_index]['current_amount'] += amount
                
                if self.goals[goal_index]['current_amount'] >= self.goals[goal_index]['target_amount']:
                    self.goals[goal_index]['completed'] = True
                    print("Цель достигнута!")
                    
                print("Прогресс обновлен")
            else:
                print("Неверный выбор цели")
        except ValueError:
            print("Неверный ввод")

    def view_goals(self):
        if not self.goals:
            print("Нет целей")
            return
            
        print("\n=== Ваши цели ===")
        for goal in self.goals:
            progress = (goal['current_amount'] / goal['target_amount']) * 100
            status = "Выполнено" if goal['completed'] else "В процессе"
            print(f"\nЦель: {goal['name']}")
            print(f"Прогресс: {goal['current_amount']}/{goal['target_amount']} ({progress:.1f}%)")
            print(f"Срок: {goal['deadline']}")
            print(f"Статус: {status}")

    def menu(self):
        while True:
            print("\n=== Меню целей ===")
            print("1. Добавить цель")
            print("2. Добавить прогресс")
            print("3. Просмотреть цели")
            print("0. Назад")
            choice = input("Выберите действие: ")

            if choice == "1":
                self.add_goal()
            elif choice == "2":
                self.add_progress()
            elif choice == "3":
                self.view_goals()
            elif choice == "0":
                break
            else:
                print("Неверный выбор")
