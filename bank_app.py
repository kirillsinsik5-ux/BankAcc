"""
Интерактивное приложение для управления банковскими счетами.
"""

from bank_account import BankAccount
import sys

class BankApplication:
    """Интерактивное приложение для работы с банковскими счетами."""
    
    def __init__(self):
        self.accounts = {}  # Словарь для хранения счетов: номер -> счет
        self.current_account = None
    
    def print_menu(self):
        """Выводит главное меню."""
        print("\n" + "=" * 50)
        print("🏦 БАНКОВСКОЕ ПРИЛОЖЕНИЕ")
        print("=" * 50)
        print("1. Создать новый счет")
        print("2. Выбрать счет")
        print("3. Внести деньги")
        print("4. Снять деньги")
        print("5. Перевести деньги")
        print("6. Показать информацию о счете")
        print("7. Показать историю операций")
        print("8. Показать все счета")
        print("9. Закрыть счет")
        print("0. Выход")
        print("=" * 50)
    
    def create_account(self):
        """Создает новый банковский счет."""
        print("\n--- Создание нового счета ---")
        
        account_number = input("Введите номер счета: ").strip()
        if not account_number:
            print("❌ Номер счета не может быть пустым")
            return
        
        if account_number in self.accounts:
            print("❌ Счет с таким номером уже существует")
            return
        
        owner = input("Введите имя владельца: ").strip()
        if not owner:
            print("❌ Имя владельца не может быть пустым")
            return
        
        try:
            initial_balance = float(input("Введите начальный баланс (по умолчанию 0): ") or "0")
            if initial_balance < 0:
                print("❌ Начальный баланс не может быть отрицательным")
                return
        except ValueError:
            print("❌ Некорректное число")
            return
        
        currency = input("Введите валюту (по умолчанию RUB): ").strip().upper() or "RUB"
        
        # Создаем счет
        try:
            account = BankAccount(account_number, owner, initial_balance, currency)
            self.accounts[account_number] = account
            print(f"✅ Счет успешно создан!")
        except ValueError as e:
            print(f"❌ Ошибка при создании счета: {e}")
    
    def select_account(self):
        """Выбирает текущий счет."""
        if not self.accounts:
            print("❌ Нет доступных счетов")
            return
        
        print("\n--- Доступные счета ---")
        for acc_num, acc in self.accounts.items():
            status = "🔒" if not acc.is_active else ""
            print(f" {acc_num} - {acc.owner} ({acc.balance} {acc.currency}) {status}")
        
        account_number = input("\nВведите номер счета: ").strip()
        
        if account_number in self.accounts:
            self.current_account = self.accounts[account_number]
            if not self.current_account.is_active:
                print(f"⚠️ Внимание: счет {account_number} закрыт")
            print(f"✅ Выбран счет: {account_number}")
            self.current_account.display_info()
        else:
            print("❌ Счет не найден")
    
    def deposit(self):
        """Вносит деньги на текущий счет."""
        if not self.current_account:
            print("❌ Сначала выберите счет (пункт 2)")
            return
        
        try:
            amount = float(input("Введите сумму для внесения: "))
            description = input("Введите описание (необязательно): ").strip()
            
            self.current_account.deposit(amount, description)
        except ValueError:
            print("❌ Некорректное число")
    
    def withdraw(self):
        """Снимает деньги с текущего счета."""
        if not self.current_account:
            print("❌ Сначала выберите счет (пункт 2)")
            return
        
        try:
            amount = float(input("Введите сумму для снятия: "))
            description = input("Введите описание (необязательно): ").strip()
            
            self.current_account.withdraw(amount, description)
        except ValueError:
            print("❌ Некорректное число")
    
    def transfer(self):
        """Переводит деньги между счетами."""
        if not self.current_account:
            print("❌ Сначала выберите счет отправителя (пункт 2)")
            return
        
        if len(self.accounts) < 2:
            print("❌ Нужно минимум 2 счета для перевода")
            return
        
        if not self.current_account.is_active:
            print("❌ Счет отправителя закрыт")
            return
        
        print("\n--- Доступные счета получателей ---")
        for acc_num, acc in self.accounts.items():
            if acc_num != self.current_account.account_number and acc.is_active:
                print(f" {acc_num} - {acc.owner} ({acc.balance} {acc.currency})")
        
        to_account_num = input("\nВведите номер счета получателя: ").strip()
        
        if to_account_num not in self.accounts:
            print("❌ Счет получателя не найден")
            return
        
        if to_account_num == self.current_account.account_number:
            print("❌ Нельзя перевести деньги на тот же счет")
            return
        
        if not self.accounts[to_account_num].is_active:
            print("❌ Счет получателя закрыт")
            return
        
        try:
            amount = float(input("Введите сумму перевода: "))
            description = input("Введите описание перевода (необязательно): ").strip()
            
            to_account = self.accounts[to_account_num]
            self.current_account.transfer(to_account, amount, description)
        except ValueError:
            print("❌ Некорректное число")
    
    def show_info(self):
        """Показывает информацию о текущем счете."""
        if not self.current_account:
            print("❌ Сначала выберите счет (пункт 2)")
            return
        
        self.current_account.display_info()
    
    def show_history(self):
        """Показывает историю операций текущего счета."""
        if not self.current_account:
            print("❌ Сначала выберите счет (пункт 2)")
            return
        
        try:
            last_n = input("Введите количество последних операций (Enter - все): ").strip()
            if last_n:
                self.current_account.show_history(int(last_n))
            else:
                self.current_account.show_history()
        except ValueError:
            print("❌ Некорректное число")
    
    def show_all_accounts(self):
        """Показывает все существующие счета."""
        if not self.accounts:
            print("❌ Нет доступных счетов")
            return
        
        print("\n" + "=" * 60)
        print(f"ВСЕ СЧЕТА (всего: {len(self.accounts)})")
        print("=" * 60)
        
        total_balance = 0
        for acc_num, acc in self.accounts.items():
            status = "🔒 ЗАКРЫТ" if not acc.is_active else "АКТИВЕН"
            print(f"\nСчет: {acc_num}")
            print(f"Владелец: {acc.owner}")
            print(f"Баланс: {acc.balance} {acc.currency}")
            print(f"Статус: {status}")
            print(f"Операций: {len(acc._transactions)}")
            print("-" * 40)
            
            if acc.is_active:
                total_balance += acc.balance
        
        print(f"\n💰 ОБЩИЙ БАЛАНС АКТИВНЫХ СЧЕТОВ: {total_balance}")
        print("=" * 60)
    
    def close_current_account(self):
        """Закрывает текущий счет."""
        if not self.current_account:
            print("❌ Сначала выберите счет (пункт 2)")
            return
        
        self.current_account.close_account()
        if not self.current_account.is_active:
            # Если счет закрыт, убираем его из текущего выбора
            self.current_account = None
    
    def run(self):
        """Запускает основное меню приложения."""
        print("\n" + "=" * 60)
        print("ДОБРО ПОЖАЛОВАТЬ В БАНКОВСКОЕ ПРИЛОЖЕНИЕ!")
        print("=" * 60)
        
        # Создаем тестовые счета для демонстрации
        if not self.accounts:
            print("\nСоздание тестовых счетов...")
            try:
                acc1 = BankAccount("ACC001", "Иван Петров", 1000, "RUB")
                acc2 = BankAccount("ACC002", "Мария Сидорова", 500, "RUB")
                self.accounts["ACC001"] = acc1
                self.accounts["ACC002"] = acc2
                print("✅ Тестовые счета созданы!")
            except Exception as e:
                print(f"❌ Ошибка при создании тестовых счетов: {e}")
        
        while True:
            if self.current_account:
                print(f"\n📍 Текущий счет: {self.current_account.account_number} ({self.current_account.owner})")
            
            self.print_menu()
            
            choice = input("Выберите пункт меню: ").strip()
            
            if choice == "1":
                self.create_account()
            elif choice == "2":
                self.select_account()
            elif choice == "3":
                self.deposit()
            elif choice == "4":
                self.withdraw()
            elif choice == "5":
                self.transfer()
            elif choice == "6":
                self.show_info()
            elif choice == "7":
                self.show_history()
            elif choice == "8":
                self.show_all_accounts()
            elif choice == "9":
                self.close_current_account()
            elif choice == "0":
                print("\n👋 Спасибо за использование банковского приложения!")
                print("До свидания!")
                sys.exit(0)
            else:
                print("❌ Неверный пункт меню. Попробуйте снова.")


if __name__ == "__main__":
    app = BankApplication()
    app.run()
