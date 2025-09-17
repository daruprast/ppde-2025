"""
Aplikasi Kalkulator Event-Driven (Tkinter)

Fitur:
- Tampilan tombol angka dan operator (+, -, *, /, %, (, ), ., =)
- Tombol fungsi: C (clear), ⌫ (hapus satu), = (hitung)
- Input via keyboard: angka, operator, Enter (=), Esc (clear), Backspace (hapus)
- Evaluasi ekspresi menggunakan parser AST (aman, tanpa eval langsung)

Catatan: Disusun mengacu pada konsep Event-Driven dari praktikum PPDE.
"""

from __future__ import annotations

import ast
import operator
import tkinter as tk
from tkinter import ttk


# Evaluator aman menggunakan AST untuk ekspresi aritmatika dasar
class SafeEvaluator:
    ALLOWED_OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    @classmethod
    def eval(cls, expression: str) -> float:
        try:
            node = ast.parse(expression, mode="eval")
            return cls._eval_node(node.body)
        except ZeroDivisionError as e:
            raise ZeroDivisionError("Pembagian dengan nol tidak diizinkan") from e
        except Exception as e:
            raise ValueError("Ekspresi tidak valid") from e

    @classmethod
    def _eval_node(cls, node):
        if isinstance(node, ast.Num):  # Python <=3.7
            return node.n
        if isinstance(node, ast.Constant):  # Python 3.8+
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Tipe konstanta tidak didukung")
        if isinstance(node, ast.BinOp):
            left = cls._eval_node(node.left)
            right = cls._eval_node(node.right)
            op_type = type(node.op)
            if op_type in cls.ALLOWED_OPERATORS:
                return cls.ALLOWED_OPERATORS[op_type](left, right)
            raise ValueError("Operator tidak didukung")
        if isinstance(node, ast.UnaryOp):
            operand = cls._eval_node(node.operand)
            op_type = type(node.op)
            if op_type in cls.ALLOWED_OPERATORS:
                return cls.ALLOWED_OPERATORS[op_type](operand)
            raise ValueError("Operator unary tidak didukung")
        if isinstance(node, ast.Expr):
            return cls._eval_node(node.value)
        if isinstance(node, ast.Call):
            raise ValueError("Pemanggilan fungsi tidak diizinkan")
        raise ValueError("Node AST tidak didukung")


class CalculatorApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Kalkulator Event-Driven")
        self.geometry("360x480")
        self.resizable(False, False)

        self.style = ttk.Style(self)
        # Gunakan tema default agar konsisten di Windows
        try:
            self.style.theme_use("default")
        except Exception:
            pass

        self.expression_var = tk.StringVar(value="")
        self.result_var = tk.StringVar(value="0")

        self._build_ui()
        self._bind_events()

    # UI
    def _build_ui(self) -> None:
        outer = ttk.Frame(self, padding=12)
        outer.pack(fill=tk.BOTH, expand=True)

        # Display ekspresi
        expr_entry = ttk.Entry(
            outer,
            textvariable=self.expression_var,
            font=("Segoe UI", 16),
            justify="right",
        )
        expr_entry.pack(fill=tk.X, pady=(0, 6))
        expr_entry.focus_set()
        self.expr_entry = expr_entry

        # Display hasil
        result_label = ttk.Label(
            outer,
            textvariable=self.result_var,
            anchor="e",
            font=("Segoe UI", 22, "bold"),
            background="#ffffff",
            relief=tk.SUNKEN,
        )
        result_label.pack(fill=tk.X, pady=(0, 12))

        # Tombol
        btns = [
            ["C", "(", ")", "⌫"],
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "%", "+"],
            ["=",],
        ]

        grid = ttk.Frame(outer)
        grid.pack(fill=tk.BOTH, expand=True)

        for r, row in enumerate(btns):
            for c, label in enumerate(row):
                span = 4 if label == "=" else 1
                btn = ttk.Button(grid, text=label, command=lambda t=label: self.on_button(t))
                btn.grid(row=r, column=c, columnspan=span, sticky="nsew", padx=4, pady=4)
                if span == 4:
                    break

        for i in range(4):
            grid.columnconfigure(i, weight=1)
        for i in range(len(btns)):
            grid.rowconfigure(i, weight=1)

        # Hint keyboard
        hint = ttk.Label(
            outer,
            text="Keyboard: angka & operator, Enter(=), Esc(C), Backspace(⌫)",
            foreground="#666",
        )
        hint.pack(fill=tk.X, pady=(8, 0))

    # Binding event keyboard
    def _bind_events(self) -> None:
        self.bind("<Key>", self.on_key)
        self.bind("<Return>", lambda e: self.calculate())
        self.bind("<KP_Enter>", lambda e: self.calculate())
        self.bind("<Escape>", lambda e: self.clear())
        self.bind("<BackSpace>", lambda e: self.backspace())

    # Event handlers
    def on_button(self, text: str) -> None:
        if text == "C":
            self.clear()
        elif text == "⌫":
            self.backspace()
        elif text == "=":
            self.calculate()
        else:
            self.append(text)

    def on_key(self, event: tk.Event) -> None:
        ch = event.char
        if ch in "0123456789.+-*/%()":
            self.append(ch)
        # Enter/Esc/Backspace ditangani oleh binding spesifik di _bind_events

    def append(self, text: str) -> None:
        self.expression_var.set(self.expression_var.get() + text)

    def clear(self) -> None:
        self.expression_var.set("")
        self.result_var.set("0")

    def backspace(self) -> None:
        expr = self.expression_var.get()
        if expr:
            self.expression_var.set(expr[:-1])

    def calculate(self) -> None:
        expr = self.expression_var.get().strip()
        if not expr:
            self.result_var.set("0")
            return
        try:
            result = SafeEvaluator.eval(expr)
            # Format hasil: hapus .0 untuk integer
            if isinstance(result, float) and result.is_integer():
                self.result_var.set(str(int(result)))
            else:
                self.result_var.set(str(result))
        except Exception as e:
            self.result_var.set("Error")


if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
