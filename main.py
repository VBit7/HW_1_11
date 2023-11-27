"""
Homework Assignment. Python Core. Module 10
For a description of the task, please refer to the README.md file
"""

from collections import UserDict
from datetime import datetime, timedelta
from typing import Optional


class Field:
    """
    Базовий клас для полів запису.
    Буде батьківським для всіх полів, у ньому реалізується логіка загальна для всіх полів
    """
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self.validate(new_value)
        self._value = new_value

    def validate(self, value):
        # Базова валідація, можна розширити в похідних класах
        pass

    def __str__(self):
        return str(self.value)


class Name(Field):
    """
    Клас для зберігання імені контакту.
    Обов'язкове поле.
    """
    def __init__(self, value):
        if not value.isalpha():
            raise ValueError("Invalid name: name should consist of letters only")
        super().__init__(value)


class Phone(Field):
    """
    Клас для зберігання номера телефону.
    Має валідацію формату (10 цифр).
    Необов'язкове поле з телефоном та таких один запис Record може містити декілька.
    """
    # def __init__(self, value):
    #     if not value.isdigit() or len(value) != 10:
    #         raise ValueError("Invalid phone: phone should consist of 10 digits only")
    #     # super().__init__(value)
    #     super().validate(value)

    def validate(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Invalid phone: phone should consist of 10 digits only")
        super().validate(value)


class Birthday(Field):
    """
    Клас для зберігання дня народження контакту.
    Може бути тільки одне таке поле у записі.
    """
    def __init__(self, value):
        try:
            date_obj = datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Invalid birthday format. Please use 'YYYY-MM-DD'")
        
        super().__init__(date_obj)

    def __str__(self):
        return self.value.strftime('%Y-%m-%d')


class Record:
    """
    Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
    Відповідає за логіку додавання/видалення/редагування необов'язкових полів та зберігання обов'язкового поля Name
    """
    def __init__(self, name, birthday: Optional[Birthday] = None):
        self.name = Name(name)
        self.phones = []
        self.birthday = birthday
    
    # Додавання телефонів
    def add_phone(self, phone):
        phone = Phone(phone)
        self.phones.append(phone)

    # Видалення телефонів
    def remove_phone(self, phone):
        self.phones = [num for num in self.phones if num.value != phone]

    # Редагування телефонів
    def edit_phone(self, old_phone, new_phone):
        if not self.find_phone(old_phone):
            raise ValueError("Phone not found")
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    # Пошук телефону
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    
    # Повертає кількість днів до наступного дня народження
    def days_to_birthday(self):
        if not self.birthday:
            return None

        today = datetime.today()
        next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day)

        if today > next_birthday:
            next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day)

        days_remaining = (next_birthday - today).days
        return days_remaining    

    def __str__(self):
        phones_str = '; '.join(str(p.value) for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}, birthday: {self.birthday}"



class AddressBook(UserDict):
    """
    Клас для зберігання та управління записами.
    Успадковується від UserDict, та містить логіку пошуку за записами до цього класу
    """

    # Додавання записів
    def add_record(self, record):
        self.data[record.name.value] = record

    # Пошук записів за іменем
    def find(self, name):
        return self.data.get(name, None)

    # Видалення записів за іменем
    def delete(self, name):
        if name in self.data:
            del self.data[name]
    
    # Повертає генератор за записами AddressBook і за одну ітерацію повертає уявлення для N записів
    def iterator(self, batch_size=1):
        records = list(self.data.values())
        for i in range(0, len(records), batch_size):
            yield records[i:i + batch_size]


if __name__ == "__main__":
    # Створення об'єкта класу AddressBook
    address_book = AddressBook()

    # Додавання записів до книги
    record1 = Record(name="JohnDoe", birthday=Birthday("1990-01-01"))
    record1.add_phone("1234567890")
    record1.add_phone("9876543210")
    address_book.add_record(record1)

    record2 = Record(name="JaneDoe")
    record2.add_phone("1112223333")
    address_book.add_record(record2)

    # Виведення усіх записів з книги
    for record_batch in address_book.iterator(batch_size=1):
        for record in record_batch:
            print(record)

    # Редагування номера телефону
    record1.edit_phone("1234567890", "9990001111")

    # Виведення усіх записів після редагування
    for record_batch in address_book.iterator(batch_size=1):
        for record in record_batch:
            print(record)

    # Видалення запису з книги
    address_book.delete("JaneDoe")

    # Виведення усіх записів після видалення
    for record_batch in address_book.iterator(batch_size=1):
        for record in record_batch:
            print(record)

    # Виведення кількості днів до наступного дня народження
    for record_batch in address_book.iterator(batch_size=1):
        for record in record_batch:
            days_to_birthday = record.days_to_birthday()
            if days_to_birthday is not None:
                print(f"Days to {record.name.value}'s birthday: {days_to_birthday}")
