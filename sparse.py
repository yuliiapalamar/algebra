from copy import deepcopy
import csv


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
                raise ValueError(f'Error converting data to float: {e}')

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
            raise ValueError("Row number cannot be negative")
        else:
            self.__band_width = value

    @property
    def row_count(self):
        return self.__row_count

    @row_count.setter
    def row_count(self, value: int):
        if value < 0:
            raise ValueError("Row number cannot be negative")
        else:
            self.__row_count = value

    def __set_sparse_matrix_from_csv(self, file_path):
        try:
            with open(file_path, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                data = next(reader)
                values = [float(item) for item in data]
                self.__row_count = int(values[0])
                self.__band_width = int(values[1])
                self.__sparseMatrix = values[2:]

        except FileNotFoundError:
            raise FileNotFoundError(f'The file {file_path} was not found.')
        except ValueError as e:
            raise ValueError(f'Error converting data to float: {e}')
        except Exception as e:
            raise Exception(f'An unexpected error occurred: {e}')

    def __sort(self):
        self.__sparseMatrix.sort(key=lambda x: (x[0], x[1]))

    def __str__(self):
        return ', '.join(str(list_) for list_ in self.__sparseMatrix)

    def __len__(self):
        return len(self.__sparseMatrix)

    def pop(self, pos: int):
        return self.__sparseMatrix.pop(pos)
