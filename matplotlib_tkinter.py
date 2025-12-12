import tkinter as tk
from tkinter import ttk
import numpy as np

import matplotlib
matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class MatplotlibApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Matplotlib in Tkinter")
        self.root.geometry("800x650")
        self.root.configure(bg='#ffffff')

        self.current_function = "x²"

        self.create_widgets()
        self.plot_graph()

    def create_widgets(self):
        header_frame = tk.Frame(self.root, bg="#2c3e50")
        header_frame.pack(fill="x", padx=20, pady=10)

        title = tk.Label(
            header_frame,
            text="📊 График Matplotlib в Tkinter",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#2c3e50"
        )
        title.pack()

        subtitle = tk.Label(
            header_frame,
            text="Демонстрация интеграции matplotlib с Tkinter (задание 4)",
            font=("Arial", 10),
            fg="#bdc3c7",
            bg="#2c3e50"
        )
        subtitle.pack()

        control_frame = tk.Frame(self.root, bg="#34495e", padx=10, pady=10)
        control_frame.pack(fill="x", padx=20, pady=(0, 10))

        tk.Label(
            control_frame,
            text="Выберите функцию:",
            font=("Arial", 11),
            fg="white",
            bg="#34495e"
        ).pack(side="left", padx=(0, 10))

        self.function_var = tk.StringVar(value="x²")
        functions = ["x²", "sin(x)", "cos(x)", "x³", "√x", "log(x)"]

        self.function_combo = ttk.Combobox(
            control_frame,
            textvariable=self.function_var,
            values=functions,
            state="readonly",
            width=15,
            font=("Arial", 11)
        )
        self.function_combo.pack(side="left", padx=5)
        self.function_combo.bind("<<ComboboxSelected>>", self.on_function_change)

        tk.Label(
            control_frame,
            text="Диапазон X:",
            font=("Arial", 11),
            fg="white",
            bg="#34495e"
        ).pack(side="left", padx=(20, 5))

        self.x_min_var = tk.StringVar(value="-10")
        self.x_min_entry = tk.Entry(control_frame, textvariable=self.x_min_var, width=5)
        self.x_min_entry.pack(side="left", padx=2)

        tk.Label(control_frame, text="before", fg="white",
                 bg="#34495e").pack(side="left", padx=5)

        self.x_max_var = tk.StringVar(value="10")
        self.x_max_entry = tk.Entry(control_frame, textvariable=self.x_max_var, width=5)
        self.x_max_entry.pack(side="left", padx=2)

        update_btn = tk.Button(
            control_frame,
            text="Обновить",
            command=self.plot_graph,
            bg="#27ae60",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=15,
            pady=5
        )
        update_btn.pack(side="left", padx=20)

        graph_frame = tk.Frame(self.root, bg="white")
        graph_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        self.figure = Figure(figsize=(8, 5), dpi=100, facecolor='#f8f9fa')
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=graph_frame)
        self.canvas.draw()

        toolbar_frame = tk.Frame(graph_frame)
        toolbar_frame.pack(side="top", fill="x")
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()

        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        info_frame = tk.Frame(self.root, bg="#ecf0f1", padx=10, pady=8)
        info_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.info_label = tk.Label(
            info_frame,
            text="",
            font=("Arial", 10),
            fg="#2c3e50",
            bg="#ecf0f1"
        )
        self.info_label.pack()

    def get_function_data(self, x):
        func_name = self.function_var.get()
        if func_name == "x²":
            return x ** 2, "y = x²"
        elif func_name == "sin(x)":
            return np.sin(x), "y = sin(x)"
        elif func_name == "cos(x)":
            return np.cos(x), "y = cos(x)"
        elif func_name == "x³":
            return x ** 3, "y = x³"
        elif func_name == "√x":
            x_positive = np.maximum(x, 0)
            return np.sqrt(x_positive), "y = √x (x ≥ 0)"
        else:
            return x ** 2, "y = x²"

    def plot_graph(self):
        try:
            x_min = float(self.x_min_var.get())
            x_max = float(self.x_max_var.get())

            if x_min >= x_max:
                self.info_label.config(text="Ошибка: минимум должен быть меньше максимума!", fg="#e74c3c")
                return

            x = np.linspace(x_min, x_max, 500)
            y, title = self.get_function_data(x)

            self.ax.clear()

            self.ax.plot(x, y, color='#3498db', linewidth=2.5, label=title)

            self.ax.axhline(y=0, color='#7f8c8d', linewidth=0.8)
            self.ax.axvline(x=0, color='#7f8c8d', linewidth=0.8)

            self.ax.grid(True, linestyle='--', alpha=0.7)

            self.ax.set_title(f"График функции {title}", fontsize=14, fontweight='bold', pad=15)
            self.ax.set_xlabel("x", fontsize=12)
            self.ax.set_ylabel("y", fontsize=12)
            self.ax.legend(loc='upper right')

            self.figure.tight_layout()
            self.canvas.draw()

            y_min, y_max = np.min(y), np.max(y)
            self.info_label.config(text=f"✓ Функция: {title} | Диапазон X: [{x_min}, {x_max}] | "
                                        f"Диапазон Y: [{y_min:.2f}, {y_max:.2f}]",fg="#27ae60"
            )

        except ValueError as e:
            self.info_label.config(text=f"Ошибка: введите корректные числа! {str(e)}", fg="#e74c3c")

    def on_function_change(self, event):
        self.plot_graph()


def main():
    root = tk.Tk()

    style = ttk.Style()
    style.theme_use('clam')

    app = MatplotlibApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()


