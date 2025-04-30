import json
import os
from datetime import datetime, timedelta

class NotificationManager:
    def __init__(self, user):
        self.user = user
        self.notifications = user['data']['notifications']
        self.last_data_entry = self._get_last_data_entry()

    def _get_last_data_entry(self):
        if not self.user['data']['transactions']:
            return None
        return max(datetime.strptime(t['date'], '%Y-%m-%d') for t in self.user['data']['transactions'])

    def save_data(self):
        # Данные сохраняются через UserManager
        pass

    def add_notification(self, message, notification_type="info"):
        notification = {
            "message": message,
            "type": notification_type,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "read": False
        }
        self.notifications.append(notification)

    def check_data_entry_reminder(self):
        if not self.last_data_entry:
            self.add_notification("Добро пожаловать! Не забудьте внести свои первые доходы и расходы.", "reminder")
            return

        days_since_last_entry = (datetime.now() - self.last_data_entry).days
        if days_since_last_entry >= 3:
            self.add_notification(f"Вы не вносили данные уже {days_since_last_entry} дней. Не забудьте обновить информацию о доходах и расходах.", "reminder")

    def check_goals_progress(self):
        for goal in self.user['data']['goals']:
            if goal['completed']:
                continue
                
            progress = (goal['current_amount'] / goal['target_amount']) * 100
            if progress >= 50 and progress < 75:
                self.add_notification(f"Вы на 50% ближе к своей цели '{goal['name']}'!", "progress")
            elif progress >= 75 and progress < 100:
                self.add_notification(f"Вы на 75% ближе к своей цели '{goal['name']}'!", "progress")
            elif progress >= 100:
                self.add_notification(f"Поздравляем! Вы достигли цели '{goal['name']}'!", "success")

    def mark_all_as_read(self):
        for notification in self.notifications:
            notification["read"] = True
        print("Все уведомления отмечены как прочитанные")

    def view_notifications(self):
        if not self.notifications:
            print("Нет уведомлений")
            return
            
        print("\n=== Уведомления ===")
        unread_count = 0
        for notification in self.notifications:
            status = "Прочитано" if notification["read"] else "Новое"
            if not notification["read"]:
                unread_count += 1
            print(f"[{notification['date']}] {notification['message']} ({status})")
            
        if unread_count > 0:
            print(f"\nУ вас {unread_count} непрочитанных уведомлений")
            mark_read = input("Отметить все как прочитанные? (да/нет): ")
            if mark_read.lower() == "да":
                self.mark_all_as_read()

    def menu(self):
        # Проверяем напоминания при входе в меню
        self.check_data_entry_reminder()
        self.check_goals_progress()
        
        while True:
            print("\n=== Меню уведомлений ===")
            print("1. Просмотреть уведомления")
            print("0. Назад")
            choice = input("Выберите действие: ")

            if choice == "1":
                self.view_notifications()
            elif choice == "0":
                break
            else:
                print("Неверный выбор")
