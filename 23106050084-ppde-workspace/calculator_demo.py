import tkinter as tk
from tkinter import messagebox

class KalkulatorEventDriven:
    def __init__(self):
        # Buat window
        self.window = tk.Tk()
        self.window.title("Kalkulator Event-Driven")
        self.window.geometry("300x400")
        self.window.configure(bg="lightgray")

        # State
        self.current_input = ""
        self.operator = ""
        self.first_number = 0.0

        # Bangun UI
        self.buat_interface()

    def buat_interface(self):
        # Display untuk menampilkan angka (readonly)
        self.display = tk.Entry(
            self.window,
            font=("Arial", 16),
            justify="right",
            state="readonly",
            readonlybackground="white"
        )
        self.display.pack(fill=tk.X, padx=10, pady=10)

        # Frame untuk tombol
        button_frame = tk.Frame(self.window, bg="lightgray")
        button_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Tombol angka 1-9 (grid 3x3)
        for i in range(3):
            for j in range(3):
                angka = i * 3 + j + 1
                btn = tk.Button(
                    button_frame,
                    text=str(angka),
                    font=("Arial", 14),
                    width=5,
                    height=2,
                    command=lambda n=angka: self.input_angka(n)
                )
                btn.grid(row=i, column=j, padx=2, pady=2)

        # Tombol 0, titik, dan clear di baris ke-3
        btn_clear = tk.Button(
            button_frame,
            text="C",
            font=("Arial", 14),
            width=5,
            height=2,
            bg="red",
            fg="white",
            command=self.clear_all
        )
        btn_clear.grid(row=3, column=0, padx=2, pady=2)

        btn_0 = tk.Button(
            button_frame,
            text="0",
            font=("Arial", 14),
            width=5,
            height=2,
            command=lambda: self.input_angka(0)
        )
        btn_0.grid(row=3, column=1, padx=2, pady=2)

        btn_dot = tk.Button(
            button_frame,
            text=".",
            font=("Arial", 14),
            width=5,
            height=2,
            command=self.input_titik
        )
        btn_dot.grid(row=3, column=2, padx=2, pady=2)

        # Tombol operator di kolom ke-3 (0..3)
        operators = ['+', '-', '*', '/']
        for i, op in enumerate(operators):
            btn_op = tk.Button(
                button_frame,
                text=op,
                font=("Arial", 14),
                width=5,
                height=2,
                bg="orange",
                command=lambda o=op: self.input_operator(o)
            )
            btn_op.grid(row=i, column=3, padx=2, pady=2)

        # Tombol sama dengan (besar, di bawah operator)
        btn_equals = tk.Button(
            button_frame,
            text="=",
            font=("Arial", 14),
            width=5,
            height=2,
            bg="lightblue",
            command=self.hitung_hasil
        )
        btn_equals.grid(row=4, column=0, columnspan=4, sticky="ew", padx=2, pady=8)

        # Inisialisasi tampilan awal
        self.update_display()

    def input_angka(self, angka):
        """Event handler untuk input angka"""
        # Hindari leading zeros yang tidak perlu (kecuali ada titik)
        if self.current_input == "0" and angka == 0:
            return
        if self.current_input == "0" and angka != 0 and "." not in self.current_input:
            self.current_input = str(angka)
        else:
            self.current_input += str(angka)
        self.update_display()

    def input_titik(self):
        """Tambahkan tanda desimal jika belum ada"""
        if "." not in self.current_input:
            if self.current_input == "":
                self.current_input = "0."
            else:
                self.current_input += "."
            self.update_display()

    def update_display(self):
        """Method untuk memperbarui tampilan display"""
        # Entry di-set normal untuk update lalu kembali ke readonly
        self.display.config(state="normal")
        self.display.delete(0, tk.END)
        # Tampilkan current_input atau 0 jika kosong
        self.display.insert(0, self.current_input if self.current_input != "" else "0")
        self.display.config(state="readonly")

    def input_operator(self, op):
        """Event handler untuk input operator"""
        if self.current_input:
            try:
                self.first_number = float(self.current_input)
            except ValueError:
                messagebox.showerror("Error", "Input tidak valid!")
                return
            self.operator = op
            self.current_input = ""
            self.update_display()

    def hitung_hasil(self):
        """Event handler untuk menghitung hasil"""
        if self.operator and self.current_input != "":
            try:
                second_number = float(self.current_input)
                if self.operator == '+':
                    result = self.first_number + second_number
                elif self.operator == '-':
                    result = self.first_number - second_number
                elif self.operator == '*':
                    result = self.first_number * second_number
                elif self.operator == '/':
                    if second_number == 0:
                        messagebox.showerror("Error", "Pembagian dengan nol!")
                        return
                    result = self.first_number / second_number
                else:
                    return

                # Hilangkan .0 jika bilangan bulat
                if result.is_integer():
                    self.current_input = str(int(result))
                else:
                    self.current_input = str(result)

                # Reset operator & first_number
                self.operator = ""
                self.first_number = 0.0
                self.update_display()

            except ValueError:
                messagebox.showerror("Error", "Input tidak valid!")

    def clear_all(self):
        """Event handler untuk clear semua"""
        self.current_input = ""
        self.operator = ""
        self.first_number = 0.0
        self.update_display()

    def jalankan(self):
        """Method untuk menjalankan aplikasi"""
        self.window.mainloop()


if __name__ == "__main__":
    kalkulator = KalkulatorEventDriven()
    kalkulator.jalankan()
