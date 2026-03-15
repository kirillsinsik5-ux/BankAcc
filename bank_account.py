"""
Модуль для работы с банковскими счетами.
Содержит класс BankAccount для моделирования банковского счета.
"""
from datetime import datetime

class BankAccount:
    """
    Класс, представляющий банковский счет.
    
    Атрибуты:
        account_number (str): Номер счета
        owner (str): Владелец счета
        balance (float): Текущий баланс
        currency (str): Валюта счета
        transactions (list): История операций
        is_active (bool): Статус счета
    """
    
    def __init__(self, account_number, owner, initial_balance=0, currency="RUB"):
        """
        Конструктор класса. Вызывается при создании нового счета.
        
        Args:
            account_number (str): Номер счета
            owner (str): Владелец счета
            initial_balance (float): Начальный баланс (по умолчанию 0)
            currency (str): Валюта счета (по умолчанию "RUB")
        
        Raises:
            ValueError: При некорректных входных данных
        """
        # Проверка входных данных
        if not account_number or not isinstance(account_number, str):
            raise ValueError("Номер счета должен быть непустой строкой")
        
        if not owner or not isinstance(owner, str):
            raise ValueError("Имя владельца должно быть непустой строкой")
        
        if initial_balance < 0:
            raise ValueError("Начальный баланс не может быть отрицательным")
        
        # Приватные атрибуты (с защитой)
        self._account_number = account_number
        self._owner = owner
        self._balance = initial_balance
        self._currency = currency
        self._transactions = []  # Список для хранения всех операций
        self._is_active = True
        
        # Запись начальной операции
        if initial_balance > 0:
            self._add_transaction("DEPOSIT", initial_balance, "Начальный баланс")
        
        print(f"✅ Счет {account_number} создан для {owner}")
        print(f"   Начальный баланс: {initial_balance} {currency}")
    
    def _add_transaction(self, transaction_type, amount, description=""):
        """
        Добавляет запись в историю операций.
        
        Args:
            transaction_type (str): Тип операции (DEPOSIT/WITHDRAWAL)
            amount (float): Сумма операции
            description (str): Описание операции
        """
        transaction = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": transaction_type,
            "amount": amount,
            "balance_after": self._balance,
            "description": description
        }
        self._transactions.append(transaction)
    
    # Свойства для доступа к атрибутам
    @property
    def balance(self):
        """Возвращает текущий баланс (только для чтения)."""
        return self._balance
    
    @property
    def account_number(self):
        """Возвращает номер счета (только для чтения)."""
        return self._account_number
    
    @property
    def owner(self):
        """Возвращает владельца счета (только для чтения)."""
        return self._owner
    
    @property
    def currency(self):
        """Возвращает валюту счета (только для чтения)."""
        return self._currency
    
    @property
    def is_active(self):
        """Возвращает статус счета (только для чтения)."""
        return self._is_active
    
    def deposit(self, amount, description=""):
        """
        Вносит деньги на счет.
        
        Args:
            amount (float): Сумма для внесения
            description (str): Описание операции
            
        Returns:
            bool: True если операция успешна, False если сумма некорректна
        """
        if not self._is_active:
            print("❌ Ошибка: счет закрыт")
            return False
        
        if amount <= 0:
            print("❌ Ошибка: сумма должна быть положительной!")
            return False
        
        self._balance += amount
        self._add_transaction("DEPOSIT", amount, description)
        
        print(f"💰 Внесено: {amount} {self._currency}")
        if description:
            print(f"   Описание: {description}")
        print(f"   Текущий баланс: {self._balance} {self._currency}")
        return True
    
    def withdraw(self, amount, description=""):
        """
        Снимает деньги со счета.
        
        Args:
            amount (float): Сумма для снятия
            description (str): Описание операции
            
        Returns:
            bool: True если операция успешна, False если недостаточно средств
        """
        if not self._is_active:
            print("❌ Ошибка: счет закрыт")
            return False
        
        if amount <= 0:
            print("❌ Ошибка: сумма должна быть положительной!")
            return False
        
        if amount > self._balance:
            print(f"❌ Ошибка: недостаточно средств!")
            print(f"   Запрошено: {amount} {self._currency}")
            print(f"   Доступно: {self._balance} {self._currency}")
            return False
        
        self._balance -= amount
        self._add_transaction("WITHDRAWAL", amount, description)
        
        print(f"💸 Снято: {amount} {self._currency}")
        if description:
            print(f"   Описание: {description}")
        print(f"   Текущий баланс: {self._balance} {self._currency}")
        return True
    
    def transfer(self, to_account, amount, description=""):
        """
        Переводит деньги на другой счет.
        
        Args:
            to_account (BankAccount): Счет получателя
            amount (float): Сумма перевода
            description (str): Описание операции
            
        Returns:
            bool: True если операция успешна
        """
        if not isinstance(to_account, BankAccount):
            print("❌ Ошибка: получатель должен быть объектом BankAccount")
            return False
        
        # Сначала снимаем деньги с текущего счета
        if self.withdraw(amount, f"Перевод: {description}"):
            # Зачисляем на счет получателя
            to_account.deposit(amount, f"Перевод от {self._owner}: {description}")
            print(f"✅ Перевод выполнен успешно")
            return True
        
        return False
    
    def close_account(self):
        """Закрывает счет."""
        if self._balance > 0:
            print(f"⚠️ На счете остались средства: {self._balance} {self._currency}")
            print("   Сначала снимите все деньги")
            return False
        
        self._is_active = False
        print(f"🔒 Счет {self._account_number} закрыт")
        return True
    
    def get_balance(self):
        """
        Возвращает текущий баланс.
        
        Returns:
            float: Текущий баланс
        """
        return self._balance
    
    def display_info(self):
        """Выводит информацию о счете."""
        status = "Активен" if self._is_active else "Закрыт"
        
        print("\n" + "=" * 50)
        print(f"ИНФОРМАЦИЯ О СЧЕТЕ")
        print("=" * 50)
        print(f"Номер счета: {self._account_number}")
        print(f"Владелец: {self._owner}")
        print(f"Баланс: {self._balance} {self._currency}")
        print(f"Статус: {status}")
        print(f"Количество операций: {len(self._transactions)}")
        print("=" * 50)
    
    def show_history(self, last_n=None):
        """
        Показывает историю операций.
        
        Args:
            last_n (int, optional): Показать только последние N операций
        """
        print("\n" + "=" * 70)
        print(f"ИСТОРИЯ ОПЕРАЦИЙ ПО СЧЕТУ {self._account_number}")
        print("=" * 70)
        
        if not self._transactions:
            print("История операций пуста")
            return
        
        transactions_to_show = self._transactions
        if last_n:
            transactions_to_show = self._transactions[-last_n:]
            print(f"Показаны последние {last_n} операций:\n")
        
        for t in transactions_to_show:
            emoji = "💰" if t["type"] == "DEPOSIT" else "💸"
            operation = "Пополнение" if t["type"] == "DEPOSIT" else "Снятие"
            
            print(f"{emoji} {t['date']} | {operation}")
            print(f"   Сумма: {t['amount']} {self._currency}")
            if t['description']:
                print(f"   Описание: {t['description']}")
            print(f"   Баланс после: {t['balance_after']} {self._currency}")
            print("-" * 70)


# Тестирование базового класса
if __name__ == "__main__":
    print("ТЕСТИРОВАНИЕ КЛАССА BankAccount")
    print("=" * 70)
    
    # Создание счета
    print("\n--- Создание счета ---")
    account = BankAccount("40817810099910000123", "Иван Петров", 1000)
    
    # Тестирование методов
    print("\n--- Тестирование методов ---")
    account.display_info()
    
    account.deposit(500, "Зарплата")
    account.withdraw(200, "Продукты")
    account.withdraw(2000)  # Ошибка: недостаточно средств
    
    print(f"\nТекущий баланс: {account.get_balance()} RUB")
    
    # Тестирование истории
    print("\n--- История операций ---")
    account.show_history()
    
    # Тестирование перевода
    print("\n--- Тестирование перевода ---")
    account2 = BankAccount("40817810099910000124", "Мария Сидорова", 500)
    account.transfer(account2, 300, "Долг")
    
    # Проверка балансов после перевода
    print("\n--- Балансы после перевода ---")
    print(f"Счет 1: {account.balance} {account.currency}")
    print(f"Счет 2: {account2.balance} {account2.currency}")
    
    # Тестирование закрытия счета
    print("\n--- Тестирование закрытия счета ---")
    account.close_account()  # Не закроется, так есть деньги
    
    # Снимаем все деньги
    account.withdraw(account.balance, "Снятие всех средств")
    account.close_account()  # Теперь закроется
    
    # Попытка операции на закрытом счете
    print("\n--- Попытка операции на закрытом счете ---")
    account.deposit(100)
    
    # Тестирование валидации
    print("\n--- Тестирование валидации ---")
    try:
        bad_account = BankAccount("", "", -100)
    except ValueError as e:
        print(f"Ошибка при создании счета: {e}")
