import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as messagebox
from classes import Matrix
from classes import Vector


def load_file(var):
    filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
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
        raise ValueError(f'Помилка даних: {e}')
    except Exception as e:
        raise Exception(f'Помилка: {e}')


def user_choose(file1, file2, operation, operations):
    window = tk.Tk()
    window.title("Відображення даних")
    window.configure(bg='pink')

    try:
        input1 = file1.get("1.0", "end").strip()
        input2 = file2.get("1.0", "end").strip()
        data1 = read_data_entry(input1)
        data2 = read_data_entry(input2)

        row = data1.display_in_window(window, row=1, column=0)
        row = data2.display_in_window(window, row=row, column=0)

        label1 = tk.Label(window, text="Результат:", bg="pink")
        label1.grid(row=row, column=0, sticky="e")
        row += 1

        operation = operation.get()

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
              "максимальний за модулем об’єкт"]
operation_var.set(operations[0])

operation_dropdown = tk.OptionMenu(root, operation_var, *operations)
operation_dropdown.config(bg="violet", activebackground="pink", highlightbackground="purple")
operation_dropdown["menu"].config(bg="violet", activebackground="pink")
operation_dropdown.grid(row=3, columnspan=3, pady=10)

continue_button2 = tk.Button(root, text="Обчислити",
                            command=lambda: user_choose(file1_entry, file2_entry, operation_var, operations), bg="violet")
continue_button2.grid(row=4, columnspan=3, pady=30)

root.mainloop()
