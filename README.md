# Личный финансовый менеджер

Приложение для управления личными финансами, постановки финансовых целей и отслеживания прогресса.

## Функциональность

- Учет доходов и расходов
- Постановка и отслеживание финансовых целей
- Аналитика и визуализация данных
- Уведомления и напоминания
- Генерация отчетов (PDF, CSV)
- Интеграция с Google Calendar
- Импорт данных из CSV

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/username/pytech.git
cd pytech
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
venv\Scripts\activate 
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Для работы с Google Calendar:
   - Создайте проект в Google Cloud Console
   - Включите Google Calendar API
   - Создайте OAuth 2.0 credentials
   - Сохраните credentials в файл `credentials.json` в корне проекта

Использование

1. Запустите приложение:
```bash
python main.py
```

2. При первом запуске:
   - Зарегистрируйте нового пользователя
   - Или используйте админ-панель

Структура проекта

```
pytech/
├── modules/
│   ├── user_management.py
│   ├── finance.py
│   ├── goals.py
│   ├── analytics.py
│   ├── notifications.py
│   ├── reports.py
│   └── integration.py
├── data/
│   └── users/
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```
