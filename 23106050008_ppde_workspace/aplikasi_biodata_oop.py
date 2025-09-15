import tkinter as tk
from tkinter import messagebox

# Membuat kelas utama aplikasi yang mewarisi dari tk.Tk
class AplikasiBiodata(tk.Tk):
    def submit_data(self):
    # Cek checkbox
        if self.var_setuju.get() == 0:
            messagebox.showwarning("Peringatan", "Anda harus menyetujui pengumpulan data!")
            return

        # Ambil data dari form
        nama = self.entry_nama.get()
        nim = self.entry_nim.get()
        jurusan = self.entry_jurusan.get()
        alamat = self.text_alamat.get("1.0", tk.END).strip()
        jenis_kelamin = self.var_jk.get()

        # Cek field kosong
        if not nama or not nim or not jurusan:
            messagebox.showwarning("Input Kosong", "Semua field harus diisi!")
            return

        # Tampilkan hasil
        hasil = f"Nama: {nama}\nNIM: {nim}\nJurusan: {jurusan}\nAlamat: {alamat}\nJenis Kelamin: {jenis_kelamin}"
        messagebox.showinfo("Data Tersimpan", hasil)

        # Tampilkan hasil di label
        self.label_hasil.config(text=f"BIODATA TERSIMPAN:\n\n{hasil}")

    def validate_form(self, *args):
        nama_valid = self.var_nama.get().strip() != ""
        nim_valid = self.var_nim.get().strip() != ""
        jurusan_valid = self.var_jurusan.get().strip() != ""
        setuju_valid = self.var_setuju.get() == 1

        if nama_valid and nim_valid and jurusan_valid and setuju_valid:
            self.btn_submit.config(state=tk.NORMAL)
        else:
            self.btn_submit.config(state=tk.DISABLED)

    def on_enter(self, event):
        if self.btn_submit['state'] == tk.NORMAL:
            self.btn_submit.config(bg="lightblue")

    def on_leave(self, event):
        self.btn_submit.config(bg="SystemButtonFace")

    def submit_shortcut(self, event=None):
        if self.btn_submit['state'] == tk.NORMAL:
            self.submit_data()

    def _coba_login(self, event=None):
        """Metode untuk memvalidasi dan memproses login."""
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        # Contoh validasi sederhana
        if username == "admin" and password == "123":
            messagebox.showinfo("Login Berhasil", "Selamat datang, admin!")
            self._pindah_ke(self.frame_biodata)
        elif username == "user1" and password == "password1":
            messagebox.showinfo("Login Berhasil", "Selamat datang, user1!")
            self._pindah_ke(self.frame_biodata)
        elif username == "mahasiswa" and password == "123456":
            messagebox.showinfo("Login Berhasil", "Selamat datang, mahasiswa!")
            self._pindah_ke(self.frame_biodata)
        else:
            messagebox.showerror("Login Gagal", "Username atau password salah.")

    def _pindah_ke(self, frame_tujuan):
        """Method untuk berpindah antar tampilan"""
        if self.frame_aktif is not None:
            self.frame_aktif.pack_forget()

        self.frame_aktif = frame_tujuan
        self.frame_aktif.pack(fill=tk.BOTH, expand=True)

        # Auto-focus berdasarkan frame yang ditampilkan
        if frame_tujuan == self.frame_login:
            self.after(100, lambda: self.entry_username.focus_set())
        elif frame_tujuan == self.frame_biodata:
            self.after(100, lambda: self.entry_nama.focus_set())

    def _buat_tampilan_login(self):
        """Metode untuk membuat tampilan halaman login."""
        self.frame_login = tk.Frame(master=self, padx=20, pady=100)

        # Konfigurasi grid untuk frame login agar terpusat
        self.frame_login.grid_columnconfigure(0, weight=1)
        self.frame_login.grid_columnconfigure(1, weight=1)

        # Judul Login
        tk.Label(
            self.frame_login, 
            text="HALAMAN LOGIN", 
            font=("Arial", 16, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=20)

        # Input Username
        tk.Label(
            self.frame_login, 
            text="Username:", 
            font=("Arial", 12)
        ).grid(row=1, column=0, sticky="W", pady=5)
        self.entry_username = tk.Entry(self.frame_login, font=("Arial", 12))
        self.entry_username.grid(row=1, column=1, pady=5, sticky="EW")
        
        # Input Password
        tk.Label(
            self.frame_login, 
            text="Password:", 
            font=("Arial", 12)
        ).grid(row=2, column=0, sticky="W", pady=5)
        self.entry_password = tk.Entry(self.frame_login, font=("Arial", 12), show='*')
        self.entry_password.grid(row=2, column=1, pady=5, sticky="EW")
        
        # Tombol Login
        self.btn_login = tk.Button(
            self.frame_login,
            text="Login",
            font=("Arial", 12, "bold"),
            command=self._coba_login
        )
        self.btn_login.grid(row=3, column=0, columnspan=2, pady=20, sticky="EW")

        # Keyboard shortcuts untuk login
        self.entry_username.bind("<Return>", lambda e: self.entry_password.focus_set())
        self.entry_password.bind("<Return>", lambda e: self._coba_login())
        
        # Info untuk user
        info_label = tk.Label(
            self.frame_login,
            text="Info: Username yang tersedia:\nadmin (password: 123)\nuser1 (password: password1)\nmahasiswa (password: 123456)",
            font=("Arial", 9),
            fg="gray",
            justify=tk.LEFT
        )
        info_label.grid(row=4, column=0, columnspan=2, pady=10)

    # Metode untuk membuat dan menempatkan semua widget
    def _buat_tampilan_biodata(self):
        """Metode untuk membuat tampilan formulir biodata."""
        # --- Variabel Kontrol Tkinter ---
        self.var_nama = tk.StringVar()
        self.var_nim = tk.StringVar()
        self.var_jurusan = tk.StringVar()
        self.var_jk = tk.StringVar(value="Pria")
        self.var_setuju = tk.IntVar()

        # Aktifkan trace untuk validasi real-time
        self.var_nama.trace_add("write", self.validate_form)
        self.var_nim.trace_add("write", self.validate_form)
        self.var_jurusan.trace_add("write", self.validate_form)

        # --- Frame Biodata ---
        self.frame_biodata = tk.Frame(master=self, padx=20, pady=20)
        self.frame_biodata.columnconfigure(1, weight=1)

        # Judul
        self.label_judul = tk.Label(
            master=self.frame_biodata, 
            text="FORM BIODATA MAHASISWA", 
            font=("Arial", 16, "bold")
        )
        self.label_judul.grid(row=0, column=0, columnspan=2, pady=20)

        # Frame khusus untuk input dengan border
        self.frame_input = tk.Frame(
            master=self.frame_biodata, 
            relief=tk.GROOVE, 
            borderwidth=2, 
            padx=10, 
            pady=10
        )

        # Input Nama
        self.label_nama = tk.Label(
            master=self.frame_input, 
            text="Nama Lengkap:", 
            font=("Arial", 12)
        )
        self.label_nama.grid(row=0, column=0, sticky="W", pady=2)
        self.entry_nama = tk.Entry(
            master=self.frame_input, 
            width=30, 
            font=("Arial", 12), 
            textvariable=self.var_nama
        )
        self.entry_nama.grid(row=0, column=1, pady=2)

        # Input NIM
        self.label_nim = tk.Label(
            master=self.frame_input, 
            text="NIM:", 
            font=("Arial", 12)
        )
        self.label_nim.grid(row=1, column=0, sticky="W", pady=2)
        self.entry_nim = tk.Entry(
            master=self.frame_input, 
            width=30, 
            font=("Arial", 12), 
            textvariable=self.var_nim
        )
        self.entry_nim.grid(row=1, column=1, pady=2)

        # Input Jurusan
        self.label_jurusan = tk.Label(
            master=self.frame_input, 
            text="Jurusan:", 
            font=("Arial", 12)
        )
        self.label_jurusan.grid(row=2, column=0, sticky="W", pady=2)
        self.entry_jurusan = tk.Entry(
            master=self.frame_input, 
            width=30, 
            font=("Arial", 12), 
            textvariable=self.var_jurusan
        )
        self.entry_jurusan.grid(row=2, column=1, pady=2)

        # Input alamat dengan Text widget
        self.label_alamat = tk.Label(
            master=self.frame_input, 
            text="Alamat:", 
            font=("Arial", 12)
        )
        self.label_alamat.grid(row=3, column=0, sticky="NW", pady=2)

        # Frame untuk Text dan Scrollbar
        self.frame_alamat = tk.Frame(
            master=self.frame_input, 
            relief=tk.SUNKEN, 
            borderwidth=1
        )

        # Scrollbar untuk alamat
        self.scrollbar_alamat = tk.Scrollbar(master=self.frame_alamat)
        self.scrollbar_alamat.pack(side=tk.RIGHT, fill=tk.Y)

        # Text widget untuk alamat
        self.text_alamat = tk.Text(
            master=self.frame_alamat, 
            height=5, 
            width=28, 
            font=("Arial", 12)
        )
        self.text_alamat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Hubungkan scrollbar dengan text
        self.scrollbar_alamat.config(command=self.text_alamat.yview)
        self.text_alamat.config(yscrollcommand=self.scrollbar_alamat.set)

        self.frame_alamat.grid(row=3, column=1, pady=2)

        # Jenis kelamin
        self.label_jk = tk.Label(
            master=self.frame_input, 
            text="Jenis Kelamin:", 
            font=("Arial", 12)
        )
        self.label_jk.grid(row=4, column=0, sticky="W", pady=2)

        self.frame_jk = tk.Frame(master=self.frame_input)
        self.frame_jk.grid(row=4, column=1, sticky="W")

        self.radio_pria = tk.Radiobutton(
            master=self.frame_jk, 
            text="Pria", 
            variable=self.var_jk, 
            value="Pria"
        )
        self.radio_pria.pack(side=tk.LEFT)
        self.radio_wanita = tk.Radiobutton(
            master=self.frame_jk, 
            text="Wanita", 
            variable=self.var_jk, 
            value="Wanita"
        )
        self.radio_wanita.pack(side=tk.LEFT)

        # Checkbox persetujuan
        self.check_setuju = tk.Checkbutton(
            master=self.frame_input,
            text="Saya menyetujui pengumpulan data ini.",
            variable=self.var_setuju,
            font=("Arial", 10),
            command=self.validate_form
        )
        self.check_setuju.grid(row=5, column=0, columnspan=2, pady=10, sticky="W")

        self.frame_input.grid(row=1, column=0, columnspan=2, sticky="EW")

        # Tombol submit
        self.btn_submit = tk.Button(
            master=self.frame_biodata, 
            text="Submit Biodata", 
            font=("Arial", 12, "bold"),
            command=self.submit_data,
            state=tk.DISABLED
        )
        self.btn_submit.grid(row=6, column=0, columnspan=2, pady=20, sticky="EW")

        # Event bindings untuk hover dan keyboard shortcuts
        self.btn_submit.bind("<Enter>", self.on_enter)
        self.btn_submit.bind("<Leave>", self.on_leave)

        # Keyboard shortcuts
        self.entry_nama.bind("<Return>", self.submit_shortcut)
        self.entry_nim.bind("<Return>", self.submit_shortcut)
        self.entry_jurusan.bind("<Return>", self.submit_shortcut)
        self.text_alamat.bind("<Return>", self.submit_shortcut)

        # Label hasil
        self.label_hasil = tk.Label(
            master=self.frame_biodata, 
            text="", 
            font=("Arial", 12, "italic"), 
            justify=tk.LEFT
        )
        self.label_hasil.grid(row=7, column=0, columnspan=2, sticky="W", padx=10)

    # Metode __init__ adalah constructor yang akan dijalankan saat objek dibuat
    def __init__(self):
        super().__init__()
        self.title("Aplikasi Biodata Mahasiswa")
        self.geometry("600x700")
        self.resizable(True, True)

        # Database user sederhana (dalam aplikasi nyata, ini akan di database)
        self.users_db = {
            "admin": "123",
            "user1": "password1",
            "mahasiswa": "123456"
        }

        # Status login
        self.current_user = None

        # Atribut untuk manajemen frame
        self.frame_aktif = None

        # Buat tampilan
        self._buat_tampilan_login()
        self._buat_tampilan_biodata()

        # Tampilkan frame login di awal
        self._pindah_ke(self.frame_login)

# Blok berikut hanya akan dieksekusi jika file ini dijalankan secara langsung
if __name__ == "__main__":
    # Membuat instance dari kelas aplikasi kita
    app = AplikasiBiodata()
    # Menjalankan mainloop dari instance tersebut
    app.mainloop()