import json
import os
from datetime import datetime
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

class ReportManager:
    def __init__(self, user):
        self.user = user
        self.finance_file = f"data/finance_{user['email']}.json"
        self.finance_manager = FinanceManager(user)
        self.goal_manager = GoalManager(user)

    def load_data(self):
        with open(self.finance_file, 'r') as f:
            return json.load(f)

    def generate_report(self, period):
        data = self.load_data()
        filtered = []
        now = datetime.now()

        for item in data:
            item_date = datetime.strptime(item['date'], "%Y-%m-%d")
            if period == 'month' and item_date.month == now.month and item_date.year == now.year:
                filtered.append(item)
            elif period == 'quarter' and (now.month - 1) // 3 == (item_date.month - 1) // 3 and item_date.year == now.year:
                filtered.append(item)
            elif period == 'year' and item_date.year == now.year:
                filtered.append(item)

        filename = f"report_{period}_{now.strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['type', 'amount', 'category', 'note', 'date'])
            writer.writeheader()
            writer.writerows(filtered)
        print(f"Отчет сохранен в файл {filename}.")

    def generate_pdf_report(self, period):
        filename = f"report_{period}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        c = canvas.Canvas(filename, pagesize=A4)
        
        # Заголовок
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 800, f"Финансовый отчет за {period}")
        c.drawString(50, 780, f"Пользователь: {self.user['name']}")
        c.drawString(50, 760, f"Дата: {datetime.now().strftime('%Y-%m-%d')}")
        
        # Статистика
        c.setFont("Helvetica", 12)
        y = 700
        income, expenses = self._get_period_stats(period)
        c.drawString(50, y, f"Доходы: {income}")
        c.drawString(50, y-20, f"Расходы: {expenses}")
        c.drawString(50, y-40, f"Баланс: {income - expenses}")
        
        # Таблица транзакций
        y -= 80
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Транзакции:")
        
        data = [['Дата', 'Тип', 'Категория', 'Сумма', 'Описание']]
        for t in self._filter_transactions(period):
            data.append([
                t['date'],
                t['type'],
                t['category'],
                str(t['amount']),
                t['description']
            ])
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        table.wrapOn(c, 50, y-20)
        table.drawOn(c, 50, y-20)
        
        # Цели
        y = 300
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Финансовые цели:")
        
        for goal in self.goal_manager.goals:
            progress = (goal['current_amount'] / goal['target_amount']) * 100
            c.setFont("Helvetica", 10)
            c.drawString(50, y-20, f"Цель: {goal['name']}")
            c.drawString(50, y-40, f"Прогресс: {progress:.1f}%")
            y -= 60
        
        c.save()
        print(f"Отчет сохранен в файл {filename}")

    def _get_period_stats(self, period):
        transactions = self._filter_transactions(period)
        income = sum(t['amount'] for t in transactions if t['type'] == 'Доходы')
        expenses = sum(t['amount'] for t in transactions if t['type'] == 'Расходы')
        return income, expenses

    def _filter_transactions(self, period):
        now = datetime.now()
        filtered = []
        
        for t in self.finance_manager.transactions:
            t_date = datetime.strptime(t['date'], '%Y-%m-%d')
            if period == 'month' and t_date.month == now.month and t_date.year == now.year:
                filtered.append(t)
            elif period == 'quarter' and (now.month - 1) // 3 == (t_date.month - 1) // 3 and t_date.year == now.year:
                filtered.append(t)
            elif period == 'year' and t_date.year == now.year:
                filtered.append(t)
                
        return filtered

    def generate_monthly_report(self):
        print("\n=== Ежемесячный отчет ===")
        current_month = datetime.now().strftime("%Y-%m")
        
        monthly_income = 0
        monthly_expenses = 0
        income_by_category = {}
        expenses_by_category = {}
        
        for transaction in self.finance_manager.transactions:
            if transaction['date'].startswith(current_month):
                if transaction['type'] == 'Доходы':
                    monthly_income += transaction['amount']
                    income_by_category[transaction['category']] = income_by_category.get(transaction['category'], 0) + transaction['amount']
                else:
                    monthly_expenses += transaction['amount']
                    expenses_by_category[transaction['category']] = expenses_by_category.get(transaction['category'], 0) + transaction['amount']
        
        print(f"\nДоходы за {current_month}: {monthly_income}")
        print("По категориям:")
        for category, amount in income_by_category.items():
            print(f"- {category}: {amount}")
            
        print(f"\nРасходы за {current_month}: {monthly_expenses}")
        print("По категориям:")
        for category, amount in expenses_by_category.items():
            print(f"- {category}: {amount}")
            
        print(f"\nБаланс: {monthly_income - monthly_expenses}")

    def generate_goals_report(self):
        print("\n=== Отчет по целям ===")
        if not self.goal_manager.goals:
            print("Нет целей")
            return
            
        for goal in self.goal_manager.goals:
            progress = (goal['current_amount'] / goal['target_amount']) * 100
            print(f"\nЦель: {goal['name']}")
            print(f"Целевая сумма: {goal['target_amount']}")
            print(f"Текущая сумма: {goal['current_amount']}")
            print(f"Прогресс: {progress:.1f}%")
            print(f"Срок: {goal['deadline']}")
            print(f"Статус: {'Выполнено' if goal['completed'] else 'В процессе'}")

    def export_to_csv(self):
        filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Тип', 'Категория', 'Сумма', 'Описание', 'Дата'])
            for transaction in self.finance_manager.transactions:
                writer.writerow([
                    transaction['type'],
                    transaction['category'],
                    transaction['amount'],
                    transaction['description'],
                    transaction['date']
                ])
        print(f"Отчет сохранен в файл {filename}")

    def menu(self):
        while True:
            print("\n=== Меню отчетов ===")
            print("1. Ежемесячный отчет")
            print("2. Отчет по целям")
            print("3. Экспорт в CSV")
            print("4. Экспорт в PDF")
            print("0. Назад")
            choice = input("Выберите действие: ")

            if choice == "1":
                self.generate_monthly_report()
            elif choice == "2":
                self.generate_goals_report()
            elif choice == "3":
                self.export_to_csv()
            elif choice == "4":
                period = input("Выберите период (month/quarter/year): ")
                if period in ['month', 'quarter', 'year']:
                    self.generate_pdf_report(period)
                else:
                    print("Неверный период")
            elif choice == "0":
                break
            else:
                print("Неверный выбор")
