import tkinter as tk
from tkinter import messagebox

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Full-Fledged Calculator")
        self.geometry("500x700")
        self.resizable(True, True)
        self.expression = ""
        self.create_widgets()

    def create_widgets(self):
        self.display = tk.Entry(self, font=("Arial", 40), borderwidth=3, relief="groove", justify="right")
        self.display.grid(row=0, column=0, columnspan=4, padx=20, pady=30, sticky="nsew")

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('C', 5, 0), ('(', 5, 1), (')', 5, 2), ('Exit', 5, 3)
        ]
        for (text, row, col) in buttons:
            action = lambda x=text: self.on_button_click(x)
            btn = tk.Button(self, text=text, width=10, height=4, font=("Arial", 22, "bold"), command=action)
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        # Make grid cells expand
        for i in range(6):
            self.grid_rowconfigure(i, weight=1)
        for j in range(4):
            self.grid_columnconfigure(j, weight=1)

    def on_button_click(self, char):
        if char == 'C':
            self.expression = ""
            self.display.delete(0, tk.END)
        elif char == '=':
            try:
                # Only allow safe characters
                allowed = set('0123456789+-*/(). ')
                if not set(self.expression).issubset(allowed):
                    raise ValueError("Invalid characters in expression")
                result = str(eval(self.expression))
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, result)
                self.expression = result
            except ZeroDivisionError:
                messagebox.showerror("Error", "Division by zero is not allowed.")
                self.display.delete(0, tk.END)
                self.expression = ""
            except Exception:
                messagebox.showerror("Error", "Invalid Expression")
                self.display.delete(0, tk.END)
                self.expression = ""
        elif char == 'Exit':
            self.destroy()
        else:
            # Prevent consecutive operators
            if char in '+-*/' and (not self.expression or self.expression[-1] in '+-*/'):
                return
            self.expression += str(char)
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, self.expression)

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
