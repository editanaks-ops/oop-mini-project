import hashlib
import uuid

class User:
    """
    Базовый класс, представляющий пользователя.
    """
    users = []  # Список для хранения всех пользователей

    def __init__(self, username: str, email: str, password: str):
        """
        При создании пользователя сразу хешируем пароль
        и сохраняем только хеш + соль.
        """
        self.username = username
        self.email = email
        self.password_hashed = self.hash_password(password)
        User.users.append(self)

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Хеширование пароля с использованием соли.
        Формат хранения: "salt$hash".
        """
        salt = uuid.uuid4().hex
        hash_value = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
        return f"{salt}${hash_value}"

    @staticmethod
    def check_password(stored_password: str, provided_password: str) -> bool:
        """
        Проверка пароля:
        1. Достаем соль из сохраненной строки.
        2. Пересчитываем хеш для введённого пароля.
        3. Сравниваем.
        """
        try:
            salt, stored_hash = stored_password.split("$", maxsplit=1)
        except ValueError:
            # Некорректный формат сохраненного пароля
            return False

        recalculated_hash = hashlib.sha256(
            (salt + provided_password).encode("utf-8")
        ).hexdigest()

        return stored_hash == recalculated_hash

    def get_details(self) -> str:
        """
        Базовое представление пользователя.
        Потомки переопределяют под себя.
        """
        return f"Пользователь: {self.username}, Email: {self.email}"


class Customer(User):
    """
    Класс, представляющий клиента, наследующий класс User.
    """

    def __init__(self, username: str, email: str, password: str, address: str):
        super().__init__(username, email, password)
        self.address = address

    def get_details(self) -> str:
        return (
            f"Клиент: {self.username}, Email: {self.email}, "
            f"Адрес: {self.address}"
        )


class Admin(User):
    """
    Класс, представляющий администратора, наследующий класс User.
    """

    def __init__(self, username: str, email: str, password: str, admin_level: int):
        super().__init__(username, email, password)
        self.admin_level = admin_level

    def get_details(self) -> str:
        return (
            f"Админ: {self.username}, Email: {self.email}, "
            f"Уровень доступа: {self.admin_level}"
        )

    @staticmethod
    def list_users():
        """
        Выводит список всех пользователей.
        (Логически этим должен пользоваться только админ.)
        """
        if not User.users:
            print("Пользователей пока нет.")
            return

        print("Список пользователей:")
        for user in User.users:
            print("-", user.get_details())

    @staticmethod
    def delete_user(username: str) -> bool:
        """
        Удаляет пользователя по username.
        Возвращает True, если удаление прошло успешно.
        """
        for user in list(User.users):
            if user.username == username:
                User.users.remove(user)
                print(f"Пользователь {username} удалён.")
                return True

        print(f"Пользователь {username} не найден.")
        return False


class AuthenticationService:
    """
    Сервис для управления регистрацией, аутентификацией
    и сессиями пользователей.
    """

    def __init__(self):
        self.current_user: User | None = None
        self.session_token: str | None = None

    def register(self, user_class, username: str, email: str, password: str, *args):
        """
        Регистрация нового пользователя.

        user_class — класс, который нужно создать (Customer или Admin).
        *args — дополнительные аргументы конструктора (address, admin_level).
        """
        # Проверка уникальности имени пользователя
        for user in User.users:
            if user.username == username:
                return f"Ошибка: пользователь с именем {username} уже существует."

        # Создаем пользователя нужного типа
        new_user = user_class(username, email, password, *args)
        return (
            f"Пользователь {new_user.username} успешно зарегистрирован как "
            f"{new_user.__class__.__name__}."
        )

    def login(self, username: str, password: str) -> str:
        """
        Аутентификация пользователя.
        """
        for user in User.users:
            if user.username == username:
                if User.check_password(user.password_hashed, password):
                    self.current_user = user
                    self.session_token = uuid.uuid4().hex
                    return (
                        f"Успешный вход. Текущий пользователь: {user.username}, "
                        f"токен сессии: {self.session_token}"
                    )
                else:
                    return "Ошибка: неверный пароль."

        return f"Ошибка: пользователь {username} не найден."

    def logout(self) -> str:
        """
        Завершение сессии текущего пользователя.
        """
        if self.current_user is None:
            return "Ошибка: никто не вошёл в систему."

        username = self.current_user.username
        self.current_user = None
        self.session_token = None
        return f"Пользователь {username} вышел из системы."

    def get_current_user(self) -> str:
        """
        Возвращает информацию о текущем вошедшем пользователе.
        """
        if self.current_user is None:
            return "Сейчас никто не вошёл в систему."
        return f"Сейчас в системе: {self.current_user.get_details()}"


# Пример использования
if __name__ == "__main__":
    auth_service = AuthenticationService()

    # Регистрация пользователей
    print(auth_service.register(
        Customer,
        "mikhail",
        "mikhail@example.com",
        "pass123",
        "Moscow, Red Square"
    ))

    print(auth_service.register(
        Admin,
        "root",
        "admin@example.com",
        "adminpass",
        10
    ))

    # Попытка зарегистрировать пользователя с тем же именем
    print(auth_service.register(
        Customer,
        "mikhail",
        "other@example.com",
        "qwerty",
        "Somewhere"
    ))

    # Вход обычного пользователя
    print(auth_service.login("mikhail", "pass123"))
    print(auth_service.get_current_user())
    print(auth_service.logout())

    # Вход администратора
    print(auth_service.login("root", "adminpass"))
    print(auth_service.get_current_user())

    # Админ смотрит список пользователей и удаляет одного
    if isinstance(auth_service.current_user, Admin):
        Admin.list_users()
        Admin.delete_user("mikhail")
        Admin.list_users()

    print(auth_service.logout())
