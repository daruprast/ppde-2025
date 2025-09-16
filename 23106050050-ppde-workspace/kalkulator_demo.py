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
kalkulator_prosedural()