import modules.user_management as user_management
import modules.reports as reports
import modules.integration as integration
import modules.notifications as notifications
import modules.analytics as analytics
import modules.finance as finance
import modules.goals as goals
from datetime import datetime, timedelta
import uuid
import csv

def test_all_functions():
    print("=== Начало тестирования всех функций ===")
    
    test_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    test_user = {
        "name": "test_user",
        "email": test_email,
        "password": "password123",
        "data": {
            "transactions": [],
            "goals": [],
            "notifications": [],
            "integrations": {}
        }
    }
    
    print("\n1. Тестирование управления пользователями:")
    try:
        user_manager = user_management.UserManager()
        user_manager.create_user(test_user["name"], test_user["email"], test_user["password"])
        print("✓ Создание пользователя: Успешно")
        
        # Тестирование профиля
        user_manager.current_user = test_user
        print("\nТестирование просмотра профиля:")
        user_manager.view_profile()
        print("✓ Просмотр профиля: Успешно")
        
        # Тестирование изменения аватара
        print("\nТестирование изменения аватара:")
        user_manager.change_avatar()
        print("✓ Изменение аватара: Успешно")
        
        # Тестирование просмотра аватара из CSV
        print("\nТестирование просмотра аватара из CSV:")
        # Создаем тестовый CSV файл
        test_csv = "test_avatars.csv"
        with open(test_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['email', 'avatar'])
            writer.writeheader()
            writer.writerow({'email': test_user['email'], 'avatar': test_user.get('avatar', '')})
        user_manager.view_avatar_from_csv()
        print("✓ Просмотр аватара из CSV: Успешно")
    except Exception as e:
        print(f"✗ Создание пользователя: Ошибка - {str(e)}")
    
    
    print("\n2. Тестирование финансовых функций:")
    try:
        finance_manager = finance.FinanceManager(test_user)
        finance_manager.add_transaction(1000, "Доходы", "Зарплата")
        print("✓ Добавление транзакции: Успешно")
    except Exception as e:
        print(f"✗ Добавление транзакции: Ошибка - {str(e)}")
    
   
    print("\n3. Тестирование целей:")
    try:
        goal_manager = goals.GoalManager(test_user)
        goal_manager.set_goal("Накопления", 10000, datetime.now() + timedelta(days=30))
        print("✓ Установка цели: Успешно")
    except Exception as e:
        print(f"✗ Установка цели: Ошибка - {str(e)}")
    
  
    print("\n4. Тестирование аналитики:")
    try:
        analytics_manager = analytics.Analytics(test_user)
        analytics_manager.get_monthly_stats()
        print("✓ Анализ расходов: Успешно")
    except Exception as e:
        print(f"✗ Анализ расходов: Ошибка - {str(e)}")
    
   
    print("\n5. Тестирование уведомлений:")
    try:
        notification_manager = notifications.NotificationManager(test_user)
        notification_manager.send_notification("Тестовое уведомление")
        print("✓ Отправка уведомления: Успешно")
    except Exception as e:
        print(f"✗ Отправка уведомления: Ошибка - {str(e)}")
    
    
    print("\n6. Тестирование интеграций:")
    try:
        integration_manager = integration.IntegrationManager(test_user)
        integration_manager.sync_bank_account("test_bank")
        print("✓ Синхронизация банковского счета: Успешно")
    except Exception as e:
        print(f"✗ Синхронизация банковского счета: Ошибка - {str(e)}")
    
   
    print("\n7. Тестирование отчетов:")
    try:
        report_manager = reports.ReportManager(test_user)
        report_manager.generate_monthly_report()
        print("✓ Генерация месячного отчета: Успешно")
    except Exception as e:
        print(f"✗ Генерация месячного отчета: Ошибка - {str(e)}")
    
    print("\n=== Тестирование завершено ===")

if __name__ == "__main__":
    test_all_functions() 