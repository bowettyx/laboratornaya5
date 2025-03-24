from abc import ABC, abstractmethod

class Product(ABC):
    def __init__(self, name, price):
        self.name = name
        self.price = price

    @abstractmethod
    def get_description(self):
        pass


class Electronics(Product):
    def __init__(self, name, price, brand):
        super().__init__(name, price)
        self.brand = brand

    def get_description(self):
        return f"{self.name}, {self.brand}"


class Clothing(Product):
    def __init__(self, name, price, size):
        super().__init__(name, price)
        self.size = size

    def get_description(self):
        return f"{self.name}, размер: {self.size}"


class Book(Product):
    def __init__(self, name, price, author):
        super().__init__(name, price)
        self.author = author

    def get_description(self):
        return f"{self.name}, автор: {self.author}"


class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, index):
        if len(self.items) > index >= 0:
            del self.items[index]

    def total_price(self):
        return sum(item.price for item in self.items)

    def display_items(self):
        for i, item in enumerate(self.items):
            print(f"{i + 1}. {item.get_description()} - Цена: {item.price}")


class Account:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
        else:
            raise InsufficientFundsError("Недостаточно средств")

    def get_balance(self):
        return self.balance


class PurchaseHistory:
    def __init__(self):
        self.purchases = []

    def add_purchase(self, cart):
        self.purchases.append(cart)

    def display_purchases(self):
        for purchase in self.purchases:
            print("----- Покупка -----")
            purchase.display_items()
            print(f"Общая стоимость: {purchase.total_price()}\n")


class InsufficientFundsError(Exception):
    pass


def main():
    # Создаем несколько продуктов
    electronics = [
        Electronics("Телефон", 10000, "Apple"),
        Electronics("Ноутбук", 50000, "Lenovo")
    ]

    clothing = [
        Clothing("Футболка", 1500, "M"),
        Clothing("Штаны", 2500, "L")
    ]

    books = [
        Book("Война и мир", 800, "Толстой"),
        Book("Преступление и наказание", 600, "Достоевский")
    ]

    categories = {
        1: ("Электроника", electronics),
        2: ("Одежда", clothing),
        3: ("Книги", books)
    }

    account = Account()
    cart = Cart()
    history = PurchaseHistory()

    while True:
        print("\nДобро пожаловать! Выберите действие:")
        print("1) Посмотреть категории")
        print("2) Перейти в корзину")
        print("3) Перейти в историю покупок")
        print("4) Посмотреть счет")
        choice = input("Ваш выбор: ")

        try:
            choice = int(choice)
        except ValueError:
            print("Неверный ввод!")
            continue

        if choice == 1:
            for category_id, (category_name, _) in categories.items():
                print(f"{category_id}) {category_name}")
            selected_category = int(input("Выберите категорию: "))
            if selected_category not in categories:
                print("Категория не найдена!")
                continue
            _, products = categories[selected_category]
            for i, product in enumerate(products):
                print(f"{i + 1}. {product.get_description()} - Цена: {product.price}")
            action = input("Хотите добавить товар в корзину? (y/n): ").lower()
            if action == 'y':
                item_index = int(input("Введите номер товара: ")) - 1
                if item_index < 0 or item_index >= len(products):
                    print("Товар не найден!")
                    continue
                cart.add_item(products[item_index])
                print("Товар добавлен в корзину.")

        elif choice == 2:
            cart.display_items()
            if not cart.items:
                print("Корзина пуста.")
                continue
            action = input("Оформить заказ? (y/n): ").lower()
            if action == 'y':
                total_cost = cart.total_price()
                if account.get_balance() < total_cost:
                    raise InsufficientFundsError("Недостаточно средств")
                account.withdraw(total_cost)
                history.add_purchase(cart)
                cart.items.clear()
                print("Заказ оформлен успешно!")
            else:
                continue

        elif choice == 3:
            history.display_purchases()

        elif choice == 4:
            print(f"Ваш баланс: {account.get_balance()}")
            action = input("Пополнить счет? (y/n): ").lower()
            if action == 'y':
                amount = float(input("Укажите сумму пополнения: "))
                account.deposit(amount)
                print("Счет пополнен успешно!")

if __name__ == "__main__":
    main()