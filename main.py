class Person:
    """Класс, представляющий человека.

    Атрибуты:
        name (str): Имя человека.
        age (int): Возраст человека.
    """

    def __init__(self, name: str, age: int):
        """Инициализирует объект Person с заданным именем и возрастом.

        Args:
            name (str): Имя человека.
            age (int): Возраст человека.
        """
        self.name = name
        self.age = age

    def introduce(self) -> str:
        """Представляет человека.

        Returns:
            str: Строка с представлением человека.
        """
        return f"Меня зовут {self.name}, мне {self.age} лет."


class Student(Person):
    """Класс, представляющий студента, наследующий от класса Person.

    Атрибуты:
        group (str): Группа, к которой принадлежит студент.
    """

    def __init__(self, name: str, age: int, group: str):
        """Инициализирует объект Student с заданным именем, возрастом и группой.

        Args:
            name (str): Имя студента.
            age (int): Возраст студента.
            group (str): Группа студента.
        """
        super().__init__(name, age)
        self.group = group

    def introduce(self) -> str:
        """Представляет студента, включая информацию о группе.

        Returns:
            str: Строка с представлением студента.
        """
        return f"Меня зовут {self.name}, мне {self.age} лет, я учусь в группе {self.group}."


# Пример использования классов
if __name__ == "__main__":
    person = Person("Иван", 30)
    print(person.introduce())

    student = Student("Анна", 20, "Группа 101")
    print(student.introduce())
    