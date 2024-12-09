import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk

def create_calculator():
    root = tk.Tk()
    root.title("Calculator")

    expression = tk.StringVar()
    
    display = tk.Entry(root, textvariable=expression, font=("Arial", 24), bd=10, insertwidth=2, width=14, borderwidth=4)
    display.grid(row=0, column=0, columnspan=4)

    def append_to_expression(value):
        expression.set(expression.get() + str(value))

    def clear_expression():
        expression.set("")

    def calculate_expression():
        try:
            response = requests.post('http://127.0.0.1:5000/calculate', json={'expression': expression.get()})
            result = response.json().get('result')
            if result is not None:
                expression.set(str(result))
            else:
                raise ValueError("Error en el cálculo")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def generate_tree():
        try:
            response = requests.post('http://127.0.0.1:5000/tree', json={'expression': expression.get()})
            image_path = response.json().get('tree_image')
            if image_path:
                img = Image.open(image_path)
                img.show()
            else:
                raise ValueError("Error al generar el árbol")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    buttons = [
        ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('+', 1, 3),
        ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
        ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('*', 3, 3),
        ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('/', 4, 3),
    ]

    for (text, row, col) in buttons:
        action = calculate_expression if text == '=' else lambda x=text: append_to_expression(x)
        tk.Button(root, text=text, padx=20, pady=20, font=("Arial", 18), command=action).grid(row=row, column=col)

    tk.Button(root, text="C", padx=20, pady=20, font=("Arial", 18), command=clear_expression).grid(row=4, column=3)
    tk.Button(root, text="Tree", padx=20, pady=20, font=("Arial", 18), command=generate_tree).grid(row=5, column=0, columnspan=4)

    root.mainloop()

create_calculator()
