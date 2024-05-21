from copy import deepcopy


class SparseMatrix:
    def __init__(self, data=None):
        self.__sparseMatrix = []
        self.__row_count = 0
        self.__band_width = 0
        if isinstance(data, list):
            try:
                values = [float(item) for item in data]
                self.__sparseMatrix = values[2:]
                self.__row_count = int(values[0])
                self.__band_width = int(values[1])
            except ValueError as e:
                raise ValueError(f'Помилка перетворення даних: {e}')

    def __getitem__(self, index):
        return self.__sparseMatrix[index]

    def __setitem__(self, index, value):
        self.__sparseMatrix[index] = deepcopy(value)

    @property
    def matrix_list(self) -> list:
        return deepcopy(self.__sparseMatrix)

    @property
    def band_width(self):
        return self.__band_width

    @band_width.setter
    def band_width(self, value: int):
        if value < 0:
            raise ValueError("М має бути більше нуля")
        else:
            self.__band_width = value

    @property
    def row_count(self):
        return self.__row_count

    @row_count.setter
    def row_count(self, value: int):
        if value < 0:
            raise ValueError("Кількість рядків має бути більше 0")
        else:
            self.__row_count = value

    def __str__(self):
        return ', '.join(str(list_) for list_ in self.__sparseMatrix)

    def __len__(self):
        return len(self.__sparseMatrix)

    def pop(self, pos: int):
        return self.__sparseMatrix.pop(pos)

    def print_full_matrix(self):
        # Initialize a full matrix with zeros
        full_matrix = [[0] * self.__row_count for _ in range(self.__row_count)]
        band_width = self.__band_width
        matrix = self.__sparseMatrix

        for i in range(self.__row_count):
            # Center diagonal
            full_matrix[i][i] = matrix[i * (band_width + 1)]
            # Below main diagonal
            for j in range(1, min(band_width + 1, self.__row_count - i)):
                full_matrix[i + j][i] = matrix[i * (band_width + 1) + j]
                full_matrix[i][i + j] = matrix[i * (band_width + 1) + j]

        # Print the full matrix
        for row in full_matrix:
            print(" ".join(map(str, row)))
