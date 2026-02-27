import math
import tkinter as tk
from tkinter import ttk, messagebox


G = 9.81


class SolverApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Math & Physics Solver")
        self.geometry("760x560")
        self.minsize(720, 520)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.math_tab = ttk.Frame(notebook)
        self.physics_tab = ttk.Frame(notebook)
        notebook.add(self.math_tab, text="Математика")
        notebook.add(self.physics_tab, text="Физика")

        self._build_math_tab()
        self._build_physics_tab()

    def _build_math_tab(self) -> None:
        frm = self.math_tab

        ttk.Label(frm, text="Квадратное уравнение: ax² + bx + c = 0", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(12, 6), padx=12)

        inputs = ttk.Frame(frm)
        inputs.pack(fill="x", padx=12)

        self.a_var = tk.StringVar(value="1")
        self.b_var = tk.StringVar(value="0")
        self.c_var = tk.StringVar(value="0")

        self._labeled_entry(inputs, "a", self.a_var, 0)
        self._labeled_entry(inputs, "b", self.b_var, 1)
        self._labeled_entry(inputs, "c", self.c_var, 2)

        ttk.Button(frm, text="Решить квадратное", command=self.solve_quadratic).pack(anchor="w", padx=12, pady=8)

        ttk.Label(frm, text="Площадь и периметр прямоугольника", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(18, 6), padx=12)

        rect = ttk.Frame(frm)
        rect.pack(fill="x", padx=12)

        self.w_var = tk.StringVar(value="5")
        self.h_var = tk.StringVar(value="4")
        self._labeled_entry(rect, "Ширина", self.w_var, 0)
        self._labeled_entry(rect, "Высота", self.h_var, 1)
        ttk.Button(frm, text="Вычислить прямоугольник", command=self.solve_rectangle).pack(anchor="w", padx=12, pady=8)

        self.math_output = tk.Text(frm, height=11, wrap="word")
        self.math_output.pack(fill="both", expand=True, padx=12, pady=(10, 12))

    def _build_physics_tab(self) -> None:
        frm = self.physics_tab

        ttk.Label(frm, text="Сила: F = m · a", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(12, 6), padx=12)
        force = ttk.Frame(frm)
        force.pack(fill="x", padx=12)

        self.mass_var = tk.StringVar(value="2")
        self.accel_var = tk.StringVar(value="3")
        self._labeled_entry(force, "Масса (kg)", self.mass_var, 0)
        self._labeled_entry(force, "Ускорение (m/s²)", self.accel_var, 1)
        ttk.Button(frm, text="Рассчитать силу", command=self.solve_force).pack(anchor="w", padx=12, pady=8)

        ttk.Label(frm, text="Потенциальная энергия: E = m · g · h", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(18, 6), padx=12)
        energy = ttk.Frame(frm)
        energy.pack(fill="x", padx=12)

        self.emass_var = tk.StringVar(value="1")
        self.height_var = tk.StringVar(value="10")
        self._labeled_entry(energy, "Масса (kg)", self.emass_var, 0)
        self._labeled_entry(energy, "Высота (m)", self.height_var, 1)
        ttk.Button(frm, text="Рассчитать энергию", command=self.solve_energy).pack(anchor="w", padx=12, pady=8)

        self.physics_output = tk.Text(frm, height=12, wrap="word")
        self.physics_output.pack(fill="both", expand=True, padx=12, pady=(10, 12))

    @staticmethod
    def _labeled_entry(parent: ttk.Frame, title: str, variable: tk.StringVar, col: int) -> None:
        box = ttk.Frame(parent)
        box.grid(row=0, column=col, padx=8, pady=4, sticky="w")
        ttk.Label(box, text=title).pack(anchor="w")
        ttk.Entry(box, textvariable=variable, width=15).pack(anchor="w")

    @staticmethod
    def _to_float(value: str, field: str) -> float:
        try:
            return float(value.replace(",", ".").strip())
        except ValueError as exc:
            raise ValueError(f"Некорректное значение поля '{field}'") from exc

    def solve_quadratic(self) -> None:
        try:
            a = self._to_float(self.a_var.get(), "a")
            b = self._to_float(self.b_var.get(), "b")
            c = self._to_float(self.c_var.get(), "c")
            if a == 0:
                raise ValueError("Коэффициент a не может быть 0")

            d = b**2 - 4 * a * c
            if d > 0:
                x1 = (-b + math.sqrt(d)) / (2 * a)
                x2 = (-b - math.sqrt(d)) / (2 * a)
                text = f"D = {d:.4f}\nДва корня: x1 = {x1:.6g}, x2 = {x2:.6g}"
            elif d == 0:
                x = -b / (2 * a)
                text = f"D = 0\nОдин корень: x = {x:.6g}"
            else:
                real = -b / (2 * a)
                imag = math.sqrt(-d) / (2 * a)
                text = f"D = {d:.4f}\nКомплексные корни: x1 = {real:.6g} + {imag:.6g}i, x2 = {real:.6g} - {imag:.6g}i"

            self._append(self.math_output, "[Квадратное уравнение]\n" + text + "\n")
        except ValueError as err:
            messagebox.showerror("Ошибка", str(err))

    def solve_rectangle(self) -> None:
        try:
            w = self._to_float(self.w_var.get(), "Ширина")
            h = self._to_float(self.h_var.get(), "Высота")
            if w <= 0 or h <= 0:
                raise ValueError("Ширина и высота должны быть больше 0")
            area = w * h
            perimeter = 2 * (w + h)
            text = f"Площадь = {area:.6g}\nПериметр = {perimeter:.6g}"
            self._append(self.math_output, "[Прямоугольник]\n" + text + "\n")
        except ValueError as err:
            messagebox.showerror("Ошибка", str(err))

    def solve_force(self) -> None:
        try:
            m = self._to_float(self.mass_var.get(), "Масса")
            a = self._to_float(self.accel_var.get(), "Ускорение")
            if m < 0:
                raise ValueError("Масса не может быть отрицательной")
            force = m * a
            self._append(self.physics_output, f"[Сила]\nF = {force:.6g} Н\n")
        except ValueError as err:
            messagebox.showerror("Ошибка", str(err))

    def solve_energy(self) -> None:
        try:
            m = self._to_float(self.emass_var.get(), "Масса")
            h = self._to_float(self.height_var.get(), "Высота")
            if m < 0 or h < 0:
                raise ValueError("Масса и высота должны быть неотрицательными")
            energy = m * G * h
            self._append(self.physics_output, f"[Потенциальная энергия]\nE = {energy:.6g} Дж\n")
        except ValueError as err:
            messagebox.showerror("Ошибка", str(err))

    @staticmethod
    def _append(widget: tk.Text, text: str) -> None:
        widget.insert("end", text + "\n")
        widget.see("end")


if __name__ == "__main__":
    app = SolverApp()
    app.mainloop()
