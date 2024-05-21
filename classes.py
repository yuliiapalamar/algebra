import tkinter as tk

class Vector:
    def __init__(self, data=None):
        if data is None:
            self.__data = []
        elif isinstance(data, list) and all(isinstance(item, (int, float)) for item in data):
            self.__data = [float(item) for item in data]
        else:
            raise ValueError('Некоректні дані для вектора')

    @property
    def data(self):
        return self.__data

    def __len__(self):
        return len(self.__data)

    def __add__(self, other):
        if len(self.__data) != len(other.data):
            raise ValueError("Вектори мають бути однакового розміру")
        return Vector([x + y for x, y in zip(self.__data, other.data)])

    def __sub__(self, other):
        if len(self.__data) != len(other.data):
            raise ValueError("Вектори мають бути однакового розміру")
        return Vector([x - y for x, y in zip(self.__data, other.data)])

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector([x * other for x in self.__data])
        elif isinstance(other, Vector):
            if len(self.__data) != len(other.data):
                raise ValueError("Вектори мають бути однакового розміру")
            return sum(x * y for x, y in zip(self.__data, other.data))
        elif isinstance(other, Matrix):
            if len(other.data) != len(self.__data):
                raise ValueError("Кількість рядків в матриці не дорівнює кількості елементів в векторі")
            result = Vector([0] * len(other.data[0]))
            for i in range(len(other.data[0])):
                for j in range(len(self.__data)):
                    result.data[i] += other.data[j][i] * self.__data[j]
            return result
        else:
            raise TypeError("Множення неможливе")

    def euclidean_norm(self):
        return round(sum(x ** 2 for x in self.__data) ** 0.5, 2)

    def max_norm(self):
        return max(abs(x) for x in self.__data)

    def display_in_window(self, root, row, column):
        label = tk.Label(root, text="Вектор:", bg="pink")
        label.grid(row=row + 1, sticky="w")
        row += 1
        for i, val in enumerate(self.__data):
            label = tk.Label(root, text=str(val), bg="pink")
            label.grid(row=row + i + 1, column=column, pady=2, sticky="e")
        return row + len(self.__data) + 2


