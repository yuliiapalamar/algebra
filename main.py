import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as messagebox
from matrix import Matrix
from classes import Vector
from LinearEquationSystem import LinearEquationSystem
from sparse import SparseMatrix


def load_file(var):
    filename = filedialog.askopenfilename(initialdir="C:\\Users\\Adminnn\\Desktop\\папочка\\унік\\algebra", title="Select a File", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if filename:
        with open(filename, 'r') as file:
            var.delete("1.0", "end")
            var.insert("1.0", file.read())


def read_data_entry(data_entry):
    data = []
    try:
        lines = data_entry.split("\n")
        for line in lines:
            values = [float(x) for x in line.strip().split()]
            data.append(values)
        if len(data) > 1:
            return Matrix(data)
        else:
            return Vector(data[0])
    except ValueError as e:
        raise ValueError(f'Помилка типів даних: {e}')
    except Exception as e:
        raise Exception(f'Помилка: {e}')


def user_choose(file1, file2, operation, operations, z1, z2):
    window = tk.Tk()
    window.title("Відображення даних")
    window.configure(bg='pink')
    operation = operation.get()

    try:
        input1 = file1.get("1.0", "end").strip()
        input2 = file2.get("1.0", "end").strip()
        if operations[6] == operation:
            data =[]
            lines = input1.split("\n")
            for line in lines:
                values = [float(x) for x in line.strip().split()]
                data.append(values)
            # messagebox.showerror("Error", f"ERROR: {data}")

            data1 = SparseMatrix(data[0])
            # messagebox.showerror("Error", f"ERROR: {data1.row_count}")
            label = tk.Label(window, text=str(input1), bg="pink")
            label.grid(row=1, column=0, pady=2, sticky="e")
            row = 2
        else:
            data1 = read_data_entry(input1)
            row = data1.display_in_window(window, row=1, column=0)

        data2 = read_data_entry(input2)
        row = data2.display_in_window(window, row=row, column=0)

        label1 = tk.Label(window, text="Результат:", bg="pink")
        label1.grid(row=row, column=0, sticky="w")
        row += 1


        if operations[0] == operation:
            (data1 + data2).display_in_window(window, row, 0)
        elif operations[1] == operation:
            (data1 - data2).display_in_window(window, row, 0)
        elif operations[2] == operation:
            result = data1 * data2
            if isinstance(result, Vector) or isinstance(result, Matrix):
                result.display_in_window(window, row, 0)
            else:
                label = tk.Label(window, text=str(result))
                label.grid(row=row + 1, column=0, pady=2, sticky="e")
        elif operations[3] == operation:
            res1 = data1.euclidean_norm()
            res2 = data2.euclidean_norm()
            res = f"1 - {res1}, 2 - {res2}"
            label2 = tk.Label(window, text=res, bg="pink")
            label2.grid(row=row, column=0, sticky="e")
        elif operations[4] == operation:
            res1 = data1.max_norm()
            res2 = data2.max_norm()
            res = f"1 - {res1}, 2 - {res2}"
            label3 = tk.Label(window, text=res, bg="pink")
            label3.grid(row=row, column=0, sticky="e")
        elif operations[5] == operation:
            system1 = LinearEquationSystem(data1, data2)
            solution, decomp_matrix, inverse = system1.solve(filename="history.txt")
            row = solution.display_in_window(window, row, 0)
            label3 = tk.Label(window, text="Декомпонована матриця", bg="pink")
            label3.grid(row=row, column=0, sticky="w")
            row += 1
            row = decomp_matrix.display_in_window(window, row, 0)
            label3 = tk.Label(window, text="Інверсна матриця", bg="pink")
            label3.grid(row=row, column=0, sticky="w")
            row += 1
            inverse.display_in_window(window, row, 0)
        elif operations[6] == operation:
            LinearEquationSystem.gaussian_sparse_matrix(data1, data2).display_in_window(window, row, 0)
        elif operations[7] == operation:
            z1_get = z1.get("1.0", "end").strip()
            z2_get = z2.get("1.0", "end").strip()

            if z1_get and z2_get:
                result, number_of_iterations, residual_norm = LinearEquationSystem.gauss_seidel(data1, data2,
                                                                                                float(z1_get),
                                                                                                int(z2_get))

            elif z1_get and not z2_get:
                result, number_of_iterations, residual_norm = LinearEquationSystem.gauss_seidel(input_matrix=data1,
                                                                                                input_vector=data2,
                                                                                                tolerance=float(z1_get))

            elif not z1_get and z2_get:
                result, number_of_iterations, residual_norm = LinearEquationSystem.gauss_seidel(input_matrix=data1,
                                                                                                input_vector=data2,
                                                                                                max_iterations=int(
                                                                                                    z2_get))

            else:
                result, number_of_iterations, residual_norm = LinearEquationSystem.gauss_seidel(input_matrix=data1,
                                                                                                input_vector=data2)

            row = result.display_in_window(window, row, 0)
            label3 = tk.Label(window, text=f"Кількість ітерацій:{number_of_iterations}", bg="pink")
            label3.grid(row=row, column=0, sticky="w")
            row += 1
            label3 = tk.Label(window, text=f"Норма: {residual_norm}", bg="pink")
            label3.grid(row=row, column=0, sticky="w")
    except Exception as e:
        # window.destroy()
        messagebox.showerror("Error", f"ERROR: {str(e)}")


root = tk.Tk()
root.title("Обчислення матриць та векторів")
root.configure(bg='pink')

label = tk.Label(root, text="Введіть дані", bg="pink")
label.grid(row=0, columnspan=3, pady=20)

file1_label = tk.Label(root, text="Перший елемент (матриця або вектор) :", bg="pink")
file1_label.grid(row=1, column=0, sticky="w")
file1_entry = tk.Text(root, height=10, width=30)
file1_entry.grid(row=1, column=1)
file1_button = tk.Button(root, text="Обрати файл", command=lambda: load_file(file1_entry), bg="violet")
file1_button.grid(row=1, column=2, padx=5)

file2_label = tk.Label(root, text="Другий елемент (матриця або вектор) :", bg="pink")
file2_label.grid(row=2, column=0, sticky="w")
file2_entry = tk.Text(root, height=10, width=30)
file2_entry.grid(row=2, column=1)
file2_button = tk.Button(root, text="Обрати файл", command=lambda: load_file(file2_entry), bg="violet")
file2_button.grid(row=2, column=2, padx=5)


operation_var = tk.StringVar(root)
operations = ["додавання", "віднімання", "множення", "евклідова норма",
              "максимальний за модулем об’єкт", "СЛАР", "стрічкова матриця", "метод Зейделя"]
operation_var.set(operations[0])

operation_dropdown = tk.OptionMenu(root, operation_var, *operations)
operation_dropdown.config(bg="violet", activebackground="pink", highlightbackground="purple")
operation_dropdown["menu"].config(bg="violet", activebackground="pink")
operation_dropdown.grid(row=3, columnspan=3, pady=10)

file3_label = tk.Label(root, text="точність для Зейделя:", bg="pink")
file3_label.grid(row=4, column=0, sticky="w")
file3_entry = tk.Text(root, height=2, width=30)
file3_entry.grid(row=4, column=1)
file4_label = tk.Label(root, text="к-сть ітерацій для Зейделя:", bg="pink")
file4_label.grid(row=4, column=2, sticky="w")
file4_entry = tk.Text(root, height=2, width=30)
file4_entry.grid(row=4, column=3)

continue_button2 = tk.Button(root, text="Обчислити",
                            command=lambda: user_choose(file1_entry, file2_entry, operation_var, operations, file3_entry, file4_entry), bg="violet")
continue_button2.grid(row=5, columnspan=3, pady=30)

root.mainloop()
