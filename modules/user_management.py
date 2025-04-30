import json
import os
from datetime import datetime
import base64

class UserManager:
    def __init__(self):
        self.current_user = None
        self.users_dir = "data/users"
        if not os.path.exists(self.users_dir):
            os.makedirs(self.users_dir)
        self.users_index_file = "data/users_index.json"
        self.users_index = self._load_users_index()
        self.admin_password = "qwe12" 

    def _load_users_index(self):
        if os.path.exists(self.users_index_file):
            with open(self.users_index_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_users_index(self):
        with open(self.users_index_file, 'w') as f:
            json.dump(self.users_index, f, indent=4)

    def _get_user_file(self, email):
        return os.path.join(self.users_dir, f"{email}.json")

    def _encode_avatar(self, avatar_path):
        if not avatar_path or not os.path.exists(avatar_path):
            return ""
        with open(avatar_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def admin_panel(self):
        print("\n=== Админ-панель ===")
        password = input("Введите пароль админа: ")
        if password != self.admin_password:
            print("Неверный пароль")
            return None

        print("\nСписок пользователей:")
        for i, email in enumerate(self.users_index.keys(), 1):
            print(f"{i}. {email}")

        try:
            choice = int(input("\nВыберите номер пользователя для входа: ")) - 1
            if 0 <= choice < len(self.users_index):
                email = list(self.users_index.keys())[choice]
                user_file = self._get_user_file(email)
                with open(user_file, 'r') as f:
                    user = json.load(f)
                print(f"Вход выполнен как {email}")
                return user
            else:
                print("Неверный выбор")
        except ValueError:
            print("Неверный ввод")
        return None

    def register(self):
        print("\n=== Регистрация ===")
        email = input("Введите email: ")
        
        # Проверка на существующий email
        if email in self.users_index:
            print("Пользователь с таким email уже существует")
            return None
            
        name = input("Введите имя: ")
        password = input("Введите пароль: ")
        confirm_password = input("Подтвердите пароль: ")
        
        if password != confirm_password:
            print("Пароли не совпадают")
            return None

        avatar_path = input("Введите путь к аватару (оставьте пустым, чтобы пропустить): ")
        avatar = self._encode_avatar(avatar_path)
            
        user = {
            "name": name,
            "email": email,
            "password": password,
            "avatar": avatar,
            "role": "user",  # По умолчанию обычный пользователь
            "data": {
                "transactions": [],
                "goals": [],
                "notifications": [],
                "integrations": {}
            }
        }
        
        # Сохраняем пользователя в отдельный файл
        user_file = self._get_user_file(email)
        with open(user_file, 'w') as f:
            json.dump(user, f, indent=4)
            
        # Обновляем индекс пользователей
        self.users_index[email] = {
            "file": user_file,
            "last_login": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self._save_users_index()
        
        print("Регистрация успешна")
        return user

    def login(self):
        print("\n=== Вход ===")
        email = input("Введите email: ")
        password = input("Введите пароль: ")
        
        if email not in self.users_index:
            print("Пользователь не найден")
            return None
            
        user_file = self._get_user_file(email)
        if not os.path.exists(user_file):
            print("Ошибка: файл пользователя не найден")
            return None
            
        with open(user_file, 'r') as f:
            user = json.load(f)
            
        if user['password'] != password:
            print("Неверный пароль")
            return None
            
        # Обновляем время последнего входа
        self.users_index[email]['last_login'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._save_users_index()
        
        print("Вход выполнен успешно")
        return user

    def save_data(self):
        if not self.current_user:
            return
            
        user_file = self._get_user_file(self.current_user['email'])
        with open(user_file, 'w') as f:
            json.dump(self.current_user, f, indent=4)

    def is_admin(self, user):
        return user.get('role') == 'admin'

    def menu(self):
        while True:
            print("\n=== Меню пользователя ===")
            print("1. Вход")
            print("2. Регистрация")
            print("3. Админ-панель")
            print("0. Выход")
            choice = input("Выберите действие: ")

            if choice == "1":
                user = self.login()
                if user:
                    self.current_user = user
                    return user
            elif choice == "2":
                user = self.register()
                if user:
                    self.current_user = user
                    return user
            elif choice == "3":
                user = self.admin_panel()
                if user:
                    self.current_user = user
                    return user
            elif choice == "0":
                return None
            else:
                print("Неверный выбор")
