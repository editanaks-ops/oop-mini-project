# 3. Класс для управления корзиной покупок


class ShoppingCart:
    """
    Класс, представляющий корзину покупок.
    """

    def __init__(self, customer, registered_by):
        """
        Инициализирует корзину покупок.
        :param customer: покупатель (объект класса Customer)
        :param registered_by: пользователь, зарегистрировавший покупку (объект Admin или User)
        """
        self.customer = customer            # покупатель
        self.registered_by = registered_by  # админ / пользователь, зарегистрировавший покупку
        self.items = []                     # список кортежей (product, quantity)

    def add_item(self, product, quantity):
        """
        Добавляет продукт в корзину.
        """
        self.items.append((product, quantity))

    def remove_item(self, product_name):
        """
        Удаляет продукт из корзины по имени продукта.
        """
        self.items = [
            (product, quantity)
            for (product, quantity) in self.items
            if product.name != product_name
        ]

    def get_total(self):
        """
        Возвращает общую стоимость продуктов в корзине.
        """
        return sum(product.price * quantity for product, quantity in self.items)

    def get_details(self):
        """
        Возвращает подробную информацию о корзине:
        - кто покупатель
        - какие товары и в каком количестве
        - общая сумма
        - кто зарегистрировал покупки
        """
        if not self.items:
            return (
                f"Покупатель {self.customer.username} пока ничего не купил.\n"
                f"Покупки зарегистрировал пользователь {self.registered_by.username}"
            )

        lines = [f"Покупатель {self.customer.username} приобрел:"]

        for product, quantity in self.items:
            # полиморфный вызов get_details у разных типов продуктов
            lines.append(f"- {product.get_details()}, Количество: {quantity}")

        total = self.get_total()
        lines.append(f"Общая сумма: {total} руб.")
        lines.append(f"Покупки зарегистрировал пользователь {self.registered_by.username}")

        return "\n".join(lines)




