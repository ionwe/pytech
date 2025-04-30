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

    def _decode_avatar(self, avatar_base64):
        if not avatar_base64:
            return None
        try:
            return base64.b64decode(avatar_base64)
        except:
            return None

    def _display_avatar(self, avatar_data):
        if not avatar_data:
            print("┌─────────────┐")
            print("│             │")
            print("│     👤      │")
            print("│             │")
            print("└─────────────┘")
            return
            
        # Сохраняем временный файл для отображения
        temp_file = "temp_avatar.png"
        try:
            with open(temp_file, "wb") as f:
                f.write(avatar_data)
            print(f"\nАватар сохранен как {temp_file}")
            print("Вы можете открыть его в любом просмотрщике изображений")
        except Exception as e:
            print(f"Ошибка при сохранении аватара: {str(e)}")

    def create_user(self, name, email, password, avatar_path=""):
        if email in self.users_index:
            raise ValueError("Пользователь с таким email уже существует")
            
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
        
        return user

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
        return self.create_user(name, email, password, avatar_path)

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
        
        # Устанавливаем текущего пользователя
        self.current_user = user
        
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

    def view_profile(self):
        if not self.current_user:
            print("Сначала войдите в систему")
            return
            
        print("\n=== Ваш профиль ===")
        print(f"Имя: {self.current_user['name']}")
        print(f"Email: {self.current_user['email']}")
        print(f"Роль: {self.current_user['role']}")
        
        print("\nАватар:")
        avatar_data = self._decode_avatar(self.current_user['avatar'])
        self._display_avatar(avatar_data)
            
        print("\n1. Изменить аватар")
        print("2. Просмотреть аватар из CSV")
        print("3. Назад")
        choice = input("Выберите действие: ")
        
        if choice == "1":
            self.change_avatar()
        elif choice == "2":
            self.view_avatar_from_csv()
        elif choice != "3":
            print("Неверный выбор")

    def view_avatar_from_csv(self):
        if not self.current_user:
            print("Сначала войдите в систему")
            return
            
        print("\n=== Просмотр аватара из CSV ===")
        csv_path = input("Введите путь к CSV файлу: ")
        
        if not os.path.exists(csv_path):
            print("Файл не найден")
            return
            
        try:
            import csv
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('email') == self.current_user['email']:
                        avatar_base64 = row.get('avatar', '')
                        if avatar_base64:
                            avatar_data = self._decode_avatar(avatar_base64)
                            self._display_avatar(avatar_data)
                            return
                print("Аватар не найден в CSV файле")
        except Exception as e:
            print(f"Ошибка при чтении CSV файла: {str(e)}")

    def change_avatar(self):
        if not self.current_user:
            print("Сначала войдите в систему")
            return
            
        print("\n=== Изменение аватара ===")
        avatar_path = input("Введите путь к новому аватару (оставьте пустым, чтобы удалить): ")
        
        if avatar_path:
            if not os.path.exists(avatar_path):
                print("Файл не найден")
                return
                
            try:
                self.current_user['avatar'] = self._encode_avatar(avatar_path)
                self.save_data()
                print("Аватар успешно обновлен")
            except Exception as e:
                print(f"Ошибка при обновлении аватара: {str(e)}")
        else:
            self.current_user['avatar'] = ""
            self.save_data()
            print("Аватар удален")

    def menu(self):
        while True:
            print("\n=== Главное меню ===")
            print("1. Вход")
            print("2. Регистрация")
            print("3. Админ-панель")
            print("0. Выход")
            choice = input("Выберите действие: ")

            if choice == "1":
                user = self.login()
                if user:
                    self.current_user = user
                    self.main_menu()
            elif choice == "2":
                user = self.register()
                if user:
                    self.current_user = user
                    self.main_menu()
            elif choice == "3":
                user = self.admin_panel()
                if user:
                    self.current_user = user
                    self.main_menu()
            elif choice == "0":
                return None
            else:
                print("Неверный выбор")

    def main_menu(self):
        while True:
            print("\n=== Главное меню ===")
            print("1. Просмотр профиля")
            print("2. Финансы")
            print("3. Цели")
            print("4. Аналитика")
            print("5. Отчеты")
            print("6. Уведомления")
            print("7. Интеграции")
            print("0. Выход")
            choice = input("Выберите действие: ")

            if choice == "1":
                self.view_profile()
            elif choice == "2":
                # Здесь будет вызов меню финансов
                pass
            elif choice == "3":
                # Здесь будет вызов меню целей
                pass
            elif choice == "4":
                # Здесь будет вызов меню аналитики
                pass
            elif choice == "5":
                # Здесь будет вызов меню отчетов
                pass
            elif choice == "6":
                # Здесь будет вызов меню уведомлений
                pass
            elif choice == "7":
                # Здесь будет вызов меню интеграций
                pass
            elif choice == "0":
                self.current_user = None
                return
            else:
                print("Неверный выбор")
