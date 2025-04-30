import os
from modules.user_management import UserManager
from modules.finance import FinanceManager
from modules.goals import GoalManager
from modules.analytics import Analytics
from modules.notifications import NotificationManager
from modules.reports import ReportManager
from modules.integration import IntegrationManager


def main_menu(user, user_manager):
    while True:
        print("\n=== Главное меню ===")
        print("1. Учёт доходов и расходов")
        print("2. Финансовые цели")
        print("3. Аналитика")
        print("4. Уведомления")
        print("5. Отчёты")
        print("6. Интеграция")
        print("0. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            finance_manager = FinanceManager(user)
            finance_manager.menu()
            user_manager.save_data()
        elif choice == "2":
            goal_manager = GoalManager(user)
            goal_manager.menu()
            user_manager.save_data()
        elif choice == "3":
            analytics = Analytics(user)
            analytics.menu()
        elif choice == "4":
            notification_manager = NotificationManager(user)
            notification_manager.menu()
            user_manager.save_data()
        elif choice == "5":
            report_manager = ReportManager(user)
            report_manager.menu()
        elif choice == "6":
            integration_manager = IntegrationManager(user)
            integration_manager.menu()
            user_manager.save_data()
        elif choice == "0":
            print("Выход из приложения.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    user_manager = UserManager()
    user = user_manager.menu()
    if user:
        main_menu(user, user_manager)
