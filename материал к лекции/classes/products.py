# 1. Базовый класс Product и производные классы для различных типов продуктов

class Product:
    """
    Базовый класс, представляющий продукт.
    """
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def get_details(self):
        return f"Продукт: {self.name}, Цера: {self.price} руб."

class Electronics(Product):
    """
    Класс, представляющий электронный продукт, наследующий класс Product.
    """
    def __init__(self, name, price, brand, warranty_period):
        super().__init__(name, price)
        self.brand = brand
        self.warranty_period = warranty_period

    def get_details(self):
        return f"Электроника: {self.name}, Бренд: {self.brand}, Цена: {self.price} руб, Гарантия: {self.warranty_period} лет"

class Clothing(Product):
    """
    Класс, представляющий одежду, наследующий класс Product.
    """
    def __init__(self, name, price, size, material):
        super().__init__(name, price)
        self.size = size
        self.material = material

    def get_details(self):
        return f"Одежда: {self.name}, Размер: {self.size}, Материал: {self.material}, Цена: {self.price} руб."

class HouseholdChemistry(Product):
    """
    Класс, представляющий товар из категории бытовой химии,
    наследующий базовый класс Product.
    """

    def __init__(self, name, price, purpose, is_toxic):
        # вызываем конструктор базового класса Product
        super().__init__(name, price)
        self.purpose = purpose      # назначение средства (например, "для пола", "для посуды")
        self.is_toxic = is_toxic    # токсичное/нет (True/False)

    def get_details(self):
        toxicity_text = "токсичное средство" if self.is_toxic else "безопасное средство"
        return (
            f"Бытовая химия: {self.name}, Назначение: {self.purpose}, "
            f"{toxicity_text}, Цена: {self.price} руб."
        )
