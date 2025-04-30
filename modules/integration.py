import json
import os
import csv
from datetime import datetime
import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

class IntegrationManager:
    def __init__(self, user):
        self.user = user
        self.integrations = user['data']['integrations']
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']

    def import_from_csv(self):
        print("\n=== Импорт данных из CSV ===")
        file_path = input("Введите путь к CSV файлу: ")
        
        if not os.path.exists(file_path):
            print("Файл не найден")
            return
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                transactions = []
                
                for row in reader:
                    transaction = {
                        'type': row.get('type', ''),
                        'category': row.get('category', ''),
                        'amount': float(row.get('amount', 0)),
                        'description': row.get('description', ''),
                        'date': row.get('date', datetime.now().strftime('%Y-%m-%d'))
                    }
                    transactions.append(transaction)
                    
                self.user['data']['transactions'].extend(transactions)
                print(f"Успешно импортировано {len(transactions)} транзакций")
                
        except Exception as e:
            print(f"Ошибка при импорте: {str(e)}")

    def setup_google_calendar(self):
        print("\n=== Настройка интеграции с Google Calendar ===")
        creds = None
        
        # Загрузка сохраненных учетных данных
        if 'google_calendar' in self.integrations:
            creds = Credentials.from_authorized_user_info(
                self.integrations['google_calendar']['credentials'],
                self.SCOPES
            )
            
        # Если нет действительных учетных данных, запросить авторизацию
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
                
            # Сохранение учетных данных
            self.integrations['google_calendar'] = {
                'credentials': {
                    'token': creds.token,
                    'refresh_token': creds.refresh_token,
                    'token_uri': creds.token_uri,
                    'client_id': creds.client_id,
                    'client_secret': creds.client_secret,
                    'scopes': creds.scopes
                },
                'setup_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            print("Интеграция с Google Calendar успешно настроена")

    def add_calendar_reminder(self, event_title, event_date, event_description=""):
        if 'google_calendar' not in self.integrations:
            print("Сначала настройте интеграцию с Google Calendar")
            return
            
        try:
            creds = Credentials.from_authorized_user_info(
                self.integrations['google_calendar']['credentials'],
                self.SCOPES
            )
            
            service = build('calendar', 'v3', credentials=creds)
            
            event = {
                'summary': event_title,
                'description': event_description,
                'start': {
                    'dateTime': event_date,
                    'timeZone': 'Europe/Moscow',
                },
                'end': {
                    'dateTime': event_date,
                    'timeZone': 'Europe/Moscow',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 30},
                    ],
                },
            }
            
            event = service.events().insert(calendarId='primary', body=event).execute()
            print(f'Событие создано: {event.get("htmlLink")}')
            
        except Exception as e:
            print(f"Ошибка при создании события: {str(e)}")

    def add_integration(self):
        print("\n=== Добавление интеграции ===")
        print("Доступные сервисы:")
        print("1. Банковский счет")
        print("2. Инвестиционный портфель")
        print("3. Криптовалютный кошелек")
        print("4. Google Calendar")
        
        choice = input("Выберите сервис: ")
        if choice not in ["1", "2", "3", "4"]:
            print("Неверный выбор")
            return
            
        service_types = {
            "1": "Банковский счет",
            "2": "Инвестиционный портфель",
            "3": "Криптовалютный кошелек",
            "4": "Google Calendar"
        }
        
        service_name = service_types[choice]
        
        if choice == "4":
            self.setup_google_calendar()
            return
            
        account_name = input("Название аккаунта: ")
        api_key = input("API ключ (если требуется): ")
        
        integration = {
            "service": service_name,
            "account_name": account_name,
            "api_key": api_key,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_sync": None
        }
        
        self.integrations[account_name] = integration
        print("Интеграция успешно добавлена")

    def remove_integration(self):
        if not self.integrations:
            print("Нет интеграций")
            return
            
        print("\n=== Удаление интеграции ===")
        for i, (account_name, integration) in enumerate(self.integrations.items(), 1):
            print(f"{i}. {account_name} ({integration['service']})")
            
        try:
            choice = int(input("Выберите интеграцию для удаления: ")) - 1
            if 0 <= choice < len(self.integrations):
                account_name = list(self.integrations.keys())[choice]
                del self.integrations[account_name]
                print("Интеграция удалена")
            else:
                print("Неверный выбор")
        except ValueError:
            print("Неверный ввод")

    def view_integrations(self):
        if not self.integrations:
            print("Нет интеграций")
            return
            
        print("\n=== Интеграции ===")
        for account_name, integration in self.integrations.items():
            print(f"\nАккаунт: {account_name}")
            print(f"Сервис: {integration['service']}")
            print(f"Дата создания: {integration['created_at']}")
            if integration['last_sync']:
                print(f"Последняя синхронизация: {integration['last_sync']}")
            if integration.get('api_key'):
                print("API ключ: ********")

    def menu(self):
        while True:
            print("\n=== Меню интеграций ===")
            print("1. Добавить интеграцию")
            print("2. Просмотреть интеграции")
            print("3. Удалить интеграцию")
            print("4. Импорт из CSV")
            print("5. Добавить напоминание в календарь")
            print("0. Назад")
            choice = input("Выберите действие: ")

            if choice == "1":
                self.add_integration()
            elif choice == "2":
                self.view_integrations()
            elif choice == "3":
                self.remove_integration()
            elif choice == "4":
                self.import_from_csv()
            elif choice == "5":
                if 'google_calendar' in self.integrations:
                    title = input("Введите название события: ")
                    date = input("Введите дату и время (YYYY-MM-DD HH:MM): ")
                    description = input("Введите описание (необязательно): ")
                    self.add_calendar_reminder(title, date, description)
                else:
                    print("Сначала настройте интеграцию с Google Calendar")
            elif choice == "0":
                break
            else:
                print("Неверный выбор")
