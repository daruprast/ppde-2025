# Ahmad Zidni Hidayat
# 23106050077
# Pemrograman Platform Desktop dan Embedded A

# Simulasi pendekatan prosedural
def kalkulator_prosedural():
    print("=== KALKULATOR PROSEDURAL ===")
    print("Program berjalan berurutan, user harus mengikuti alur")

    while True:
        try:
            angka1 = float(input("Masukkan angka pertama: "))
            break
        except ValueError:
            print("Input harus berupa angka!")

    while True:
        operator = input("Masukkan operator (+, -, *, /): ")
        if operator in ['+', '-', '*', '/']:
            break
        print("Operator tidak valid!")

    while True:
        try:
            angka2 = float(input("Masukkan angka kedua: "))
            break
        except ValueError:
            print("Input harus berupa angka!")

    if operator == '+':
        hasil = angka1 + angka2
    elif operator == '-':
        hasil = angka1 - angka2
    elif operator == '*':
        hasil = angka1 * angka2
    elif operator == '/':
        if angka2 != 0:
            hasil = angka1 / angka2
        else:
            print("Error: Pembagian dengan nol!")
            return

    print(f"Hasil: {angka1} {operator} {angka2} = {hasil}")
    print("Program selesai")

# Uncomment baris berikut untuk menjalankan demo prosedural
# kalkulator_prosedural()


import tkinter as tk
from tkinter import messagebox

class KalkulatorEventDriven:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Kalkulator Event-Driven - Ahmad Zidni Hidayat")
        self.window.geometry("350x500")
        self.window.minsize(300, 400)
        self.window.configure(bg="lightgray")

        # Variabel untuk menyimpan state
        self.current_input = ""
        self.operator = ""
        self.first_number = 0

        self.buat_interface()

    def buat_interface(self):
        # Display untuk menampilkan angka
        self.display = tk.Entry(
            self.window, 
            font=("Arial", 24), 
            justify="right",
            state="readonly",
            bg="white",
            bd=3,
            relief="sunken",
        )
        self.display.pack(fill=tk.X, padx=15, pady=(15, 10), ipady=15)

        # Frame untuk tombol
        button_frame = tk.Frame(self.window, bg="lightgray")
        button_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # Konfigurasi grid untuk responsif
        for i in range(4):
            button_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            button_frame.grid_columnconfigure(j, weight=1)

        # Tombol angka (1-9)
        for i in range(3):
            for j in range(3):
                angka = i * 3 + j + 1
                btn = tk.Button(
                    button_frame,
                    text=str(angka),
                    font=("Arial", 16),
                    bg="white",
                    fg="black",
                    bd=2,
                    relief="raised",
                    command=lambda n=angka: self.input_angka(n)
                )
                btn.grid(row=i, column=j, padx=3, pady=3, sticky="nsew")

        # Tombol 0
        btn_0 = tk.Button(
            button_frame,
            text="0",
            font=("Arial", 16),
            bg="white",
            fg="black",
            bd=2,
            relief="raised",
            command=lambda: self.input_angka(0)
        )
        btn_0.grid(row=3, column=1, padx=3, pady=3, sticky="nsew")

        # Tombol operator
        operators = ['+', '-', '*', '/']
        for i, op in enumerate(operators):
            btn_op = tk.Button(
                button_frame,
                text=op,
                font=("Arial", 16, "bold"),
                bg="#FF9500",
                fg="white",
                bd=2,
                relief="raised",
                command=lambda o=op: self.input_operator(o)
            )
            btn_op.grid(row=i, column=3, padx=3, pady=3, sticky="nsew")

        # Tombol sama dengan
        btn_equals = tk.Button(
            button_frame,
            text="=",
            font=("Arial", 16, "bold"),
            bg="#4A90E2",
            fg="white",
            bd=2,
            relief="raised",
            command=self.hitung_hasil
        )
        btn_equals.grid(row=3, column=2, padx=3, pady=3, sticky="nsew")

        # Tombol clear
        btn_clear = tk.Button(
            button_frame,
            text="C",
            font=("Arial", 16, "bold"),
            bg="#FF3B30",
            fg="white",
            bd=2,
            relief="raised",
            command=self.clear_all
        )
        btn_clear.grid(row=3, column=0, padx=3, pady=3, sticky="nsew")

    def input_operator(self, op):
        """Event handler untuk input operator"""
        if self.current_input:
            self.first_number = float(self.current_input)
            self.operator = op
            self.current_input = f"{int(self.first_number) if self.first_number.is_integer() else self.first_number} {op} "
            self.update_display()

    def input_angka(self, angka):
        """Event handler untuk input angka"""
        # Jika ada operator di display, mulai input angka baru
        if self.operator and " " in self.current_input:
            if self.current_input.endswith(" "):
                self.current_input += str(angka)
            else:
                self.current_input += str(angka)
        else:
            self.current_input += str(angka)
        self.update_display()

    def update_display(self):
        """Method untuk memperbarui tampilan display"""
        self.display.config(state="normal")
        self.display.delete(0, tk.END)
        self.display.insert(0, self.current_input)
        self.display.config(state="readonly")
    def hitung_hasil(self):
        """Event handler untuk menghitung hasil"""
        if self.operator and " " in self.current_input:
            try:
                # Ambil angka kedua dari bagian terakhir display
                parts = self.current_input.split()
                if len(parts) >= 3:
                    second_number = float(parts[2])
                else:
                    return

                if self.operator == '+':
                    result = self.first_number + second_number
                elif self.operator == '-':
                    result = self.first_number - second_number
                elif self.operator == '*':
                    result = self.first_number * second_number
                elif self.operator == '/':
                    if second_number != 0:
                        result = self.first_number / second_number
                    else:
                        messagebox.showerror("Error", "Pembagian dengan nol!")
                        return

                # Format hasil untuk menghindari .0 pada bilangan bulat
                if result.is_integer():
                    self.current_input = str(int(result))
                else:
                    self.current_input = str(result)
                    
                self.operator = ""
                self.first_number = 0
                self.update_display()

            except (ValueError, IndexError):
                messagebox.showerror("Error", "Input tidak valid!")

    def clear_all(self):
        """Event handler untuk clear semua"""
        self.current_input = ""
        self.operator = ""
        self.first_number = 0
        self.update_display()

    def jalankan(self):
        """Method untuk menjalankan aplikasi"""
        self.window.mainloop()

# Untuk menjalankan kalkulator event-driven
if __name__ == "__main__":
    kalkulator = KalkulatorEventDriven()
    kalkulator.jalankan()