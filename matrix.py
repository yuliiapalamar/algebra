import tkinter as tk
from classes import Vector


class Matrix:
    def __init__(self, data=None):
        if data is None:
            self.__data = []
        elif (isinstance(data, list) and all(isinstance(sublist, list) and
              all(isinstance(item, (int, float)) for item in sublist) for sublist in data)):
            if all(len(row) == len(data[0]) for row in data):
                self.__data = [[float(item) for item in sublist] for sublist in data]
            else:
                raise ValueError('Різна кількість даних в рядках')
        else:
            raise ValueError('Некоректні дані для матриці')

    @property
    def data(self):
        return self.__data

    def __len__(self):
        return len(self.__data)

    def __add__(self, other):
        if len(self.__data) != len(other.data) or len(self.__data[0]) != len(other.data[0]):
            raise ValueError("Матриці мають бути однакового розміру")
        return Matrix([[x + y for x, y in zip(row1, row2)] for row1, row2 in zip(self.__data, other.data)])

    def __sub__(self, other):
        if len(self.__data) != len(other.data) or len(self.__data[0]) != len(other.data[0]):
            raise ValueError("Матриці мають бути однакового розміру")
        return Matrix([[x - y for x, y in zip(row1, row2)] for row1, row2 in zip(self.__data, other.data)])

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Matrix([[x * other for x in row] for row in self.__data])
        elif isinstance(other, Vector):
            if len(other.data) != len(self.__data[0]):
                raise ValueError("Кількість колонок матриці не дорівнює кількості елементів в векторі")
            result = Vector([0] * len(self.__data))
            for i in range(len(self.__data)):
                for j in range(len(other.data)):
                        result.data[i] += self.__data[i][j] * other.data[j]
            return result
        elif isinstance(other, Matrix):
            if len(self.__data[0]) != len(other.data):
                raise ValueError("Кількість колонок матриці не дорівнює кількості рядків в другій матриці")
            result = Matrix([[0 for _ in range(len(other.data[0]))] for _ in range(len(self.__data))])
            for i in range(len(self.__data)):
                for j in range(len(other.data[0])):
                    for k in range(len(other.data)):
                        result.data[i][j] += self.__data[i][k] * other.data[k][j]
            return result
        else:
            raise TypeError("Множення неможливе")

    def euclidean_norm(self):
        return round(sum(sum(x ** 2 for x in row) for row in self.__data) ** 0.5, 2)

    def max_norm(self):
        return max(abs(self.__data[i][j]) for i in range(len(self.__data)) for j in range(len(self.__data[0])))

    def display_in_window(self, root, row, column):
        label = tk.Label(root, text="Матриця:", bg="pink")
        label.grid(row=row, sticky="w")
        row += 1
        for i, row_data in enumerate(self.__data):
            for j, val in enumerate(row_data):
                label = tk.Label(root, text=str(val), bg="pink")
                label.grid(row=row + i + 1, column=column + j, pady=2, sticky="e")
        return row + len(self.__data) + 2
