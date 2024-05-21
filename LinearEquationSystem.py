from matrix import Matrix
from classes import Vector
from copy import deepcopy


class LinearEquationSystem:
    def __init__(self, coefficients, constants):
        if isinstance(coefficients, Matrix) and isinstance(constants, Vector):
            self.__matrix = coefficients
            self.__vector = constants
        else:
            raise TypeError("Задані дані не є СЛАР")

    def __combine_matrix(self, matrix, vector):
        combined = []
        for i in range(len(matrix.data)):
            combined.append(matrix.data[i] + [vector.data[i]])
        return Matrix(combined)

    def solve(self, filename):
        with open(filename, 'a') as file:
            file.write("РОЗВ'ЯЗУВАННЯ СЛАР\n")
        result, decomp_m = self.__gaussian_elimination_with_pivot(self.__matrix, self.__vector, filename)
        inverse = self.inverse_matrix(filename)
        return result, decomp_m, inverse

    def __gaussian_elimination_with_pivot(self, matrix, vector, filename):
        augmented_matrix = self.__combine_matrix(matrix, vector)
        n = len(matrix)

        precision = '.4f'
        with open(filename, 'a') as file:
            file.write("Історія розв'язку\n")
            file.write("Початкова розширена матриця:\n")
            for row in matrix.data:
                row_str = ' '.join(format(element, precision) for element in row)
                file.write(f"{row_str}\n")

        for i in range(n):
            max_index = i
            for j in range(i + 1, n):
                if abs(augmented_matrix.data[j][i]) > abs(augmented_matrix.data[max_index][i]):
                    max_index = j
            with open(filename, 'a') as file:
                file.write(f"\nЕтап {i + 1}: Вибір головного елемента")
                file.write(f"Максимальний за модулем елемент у {i + 1}-му стовпці рядків: {max_index + 1}")

            augmented_matrix.data[i], augmented_matrix.data[max_index] = augmented_matrix.data[max_index], \
                                                                         augmented_matrix.data[i]

            with open(filename, 'a') as file:
                file.write("Після обміну рядків:\n")
                for row in matrix.data:
                    row_str = ' '.join(format(element, precision) for element in row)
                    file.write(f"{row_str}\n")

            pivot = augmented_matrix.data[i][i]
            if pivot == 0:
                raise ValueError("Матриця є сингулярною.")

            for j in range(i + 1, n):
                ratio = augmented_matrix.data[j][i] / pivot
                for k in range(i, n + 1):
                    augmented_matrix.data[j][k] -= ratio * augmented_matrix.data[i][k]

            with open(filename, 'a') as file:
                file.write("Приведення до східчастої форми:\n")
                for row in matrix.data:
                    row_str = ' '.join(format(element, precision) for element in row)
                    file.write(f"{row_str}\n")

        decomp_matrix = augmented_matrix

        solution = Vector([0] * n)
        for i in range(n - 1, -1, -1):
            solution.data[i] = augmented_matrix.data[i][-1]
            for j in range(i + 1, n):
                solution.data[i] -= augmented_matrix.data[i][j] * solution.data[j]
            solution.data[i] /= augmented_matrix.data[i][i]

        with open(filename, 'a') as file:
            file.write("Розв'язок системи рівнянь:\n")
            for i in range(n):
                file.write(f"x{i + 1} = {format(solution.data[i], precision)}\n")

        solution = Vector([round(x, 2) for x in solution.data])
        decomp_matrix = Matrix([[round(x, 2) for x in row] for row in decomp_matrix.data])
        return solution, decomp_matrix

    @staticmethod
    def __print_matrix(matrix):
        for row in matrix.data:
            print(row)

    def inverse_matrix(self, filename):
        n = len(self.__matrix)
        with open(filename, 'a') as file:
            file.write("\n\n\nПОШУК ІНВЕРСНОЇ МАТРИЦІ\n")
        inverse = Matrix([[0] * n for _ in range(n)])
        for i in range(n):
            column = Vector([1 if j == i else 0 for j in range(n)])

            inverted_column, decomp_m = self.__gaussian_elimination_with_pivot(self.__matrix, column, filename)
            for j in range(len(inverted_column)):
                inverse.data[j][i] = inverted_column.data[j]

        precision = '.4f'
        with open(filename, 'a') as file:
            file.write("\n\Інверсна матриця:\n")
            for row in inverse.data:
                row_str = ' '.join(format(element, precision) for element in row)
                file.write(f"{row_str}\n")

        for i in range(n):
            for j in range(n):
                inverse.data[i][j] = round(inverse.data[i][j], 2)

        return inverse

    @staticmethod
    def gaussian_sparse_matrix(input_tape_matrix, input_vector):
        tape_matrix = input_tape_matrix.matrix_list
        vector = deepcopy(input_vector.data)
        row_count = input_tape_matrix.row_count
        band_width = input_tape_matrix.band_width

        def calc_element_pos(row_index, row_length):
            return row_index * (band_width + 1) - sum(range(band_width - row_length + 1))

        print(row_count, band_width, tape_matrix)
        # 3 - 0 = 3
        for row_index in range(row_count - 1):
            multiplying_row_length = min(band_width + 1, row_count - row_index)
            multiplying_element_pos = calc_element_pos(row_index, multiplying_row_length)
 # 1 2 3            1
 # 2 3(-1) 4(-2)    1
 # 3 4 1(-8)        1
            for i in range(multiplying_row_length - 1):
                current_row_length = min(band_width + 1, row_count - row_index - 1 - i)
                current_element_pos = calc_element_pos(row_index + i + 1, current_row_length)

                multiplier = tape_matrix[multiplying_element_pos + i + 1] / tape_matrix[multiplying_element_pos]
                # 2

                if (current_row_length != band_width + 1):
                    print("opt1")
                    range_limit = current_row_length
                else:
                    print("opt2")
                    range_limit = current_row_length - 1

                for j in range(range_limit):
                    tape_matrix[current_element_pos + j] = tape_matrix[current_element_pos + j] - \
                                                           multiplier * tape_matrix[multiplying_element_pos + i + j + 1]
                    print(tape_matrix)
                vector[row_index + i + 1] = vector[row_index + i + 1] - multiplier * vector[row_index]


        answers = [0] * row_count
        answers[-1] = vector[-1] / tape_matrix[-1]

        for row_index in range(row_count - 2, -1, -1):
            row_length = min(band_width + 1, row_count - row_index)
            element_pos = calc_element_pos(row_index, row_length)
            answers[row_index] = vector[row_index]

            for j in range(1, row_length):
                answers[row_index] -= tape_matrix[element_pos + j] * answers[row_index + j]

            answers[row_index] /= tape_matrix[element_pos]

        return Vector(answers)

    @staticmethod
    def gauss_seidel(input_matrix, input_vector, tolerance=1e-10, max_iterations=1000):
        matrix = deepcopy(input_matrix)
        vector = deepcopy(input_vector)
        num_variables = len(vector.data)
        result = [0 for _ in range(num_variables)]

        for k in range(max_iterations):
            old_result = result.copy()

            for i in range(num_variables):
                sum1 = 0
                for j in range(i):
                    sum1 += matrix.data[i][j] * result[j]

                sum2 = 0
                for j in range(i + 1, num_variables):
                    sum2 += matrix.data[i][j] * old_result[j]
                # print(sum1)
                # print(sum2)
                result[i] = (vector.data[i] - sum1 - sum2) / matrix.data[i][i]

            number_of_iterations = str(k + 1)
            if all(abs(result[i] - old_result[i]) < tolerance for i in range(num_variables)):
                break
        else:
            number_of_iterations = 'Досягнуто макс к-ті ітерацій: ' + str(max_iterations)

        residual = []
        for i in range(num_variables):
            sum_term = 0
            for j in range(num_variables):
                sum_term += matrix.data[i][j] * result[j]
            residual.append(sum_term - vector.data[i])

        residual_norm = 0
        for r in residual:
            residual_norm += r ** 2
        residual_norm **= 0.5

        return Vector(result), number_of_iterations, residual_norm