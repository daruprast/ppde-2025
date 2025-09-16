# Ahmad Zidni Hidayat
# 23106050077
# Pemrograman Platform Desktop dan Embedded A

# Belajar dan praktik membuat view terpisah dari logic aplikasi

import tkinter as tk
from tkinter import messagebox, ttk
import datetime
import logging
import re
import json
import os

# Setup logging
logging.basicConfig(
    filename='aplikasi_biodata.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Membuat kelas utama aplikasi yang mewarisi dari tk.Tk
class AplikasiBiodata(tk.Tk):
    def __init__(self):
        super().__init__()
        # Log aplikasi start
        logging.info("Aplikasi dimulai")

        self.title("Aplikasi Biodata Mahasiswa")
        self.geometry("650x800")
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

        # File untuk menyimpan remember me
        self.remember_file = "remember_me.json"

        # Buat tampilan
        self._buat_tampilan_login()
        self._buat_tampilan_biodata()

        # Tampilkan frame login di awal
        self._pindah_ke(self.frame_login)

        # Load remember me data
        self._load_remember_me()

    # === METHODS UNTUK NAVIGASI ANTAR FRAME ===
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

    # === METHODS UNTUK LOGIN ===
    def _buat_tampilan_login(self):
        # Frame utama login dengan background yang sama seperti biodata
        self.frame_login = tk.Frame(master=self, padx=20, pady=20, bg="lavender")

        # Konfigurasi untuk memusatkan konten secara vertikal dan horizontal
        self.frame_login.pack(fill=tk.BOTH, expand=True)
        self.frame_login.grid_rowconfigure(0, weight=1)  # Spacer atas
        self.frame_login.grid_rowconfigure(6, weight=1)  # Spacer bawah
        self.frame_login.grid_columnconfigure(0, weight=1)
        self.frame_login.grid_columnconfigure(1, weight=1)

        # Frame container untuk form login agar lebih terpusat
        login_container = tk.Frame(
            master=self.frame_login, 
            relief=tk.GROOVE, 
            borderwidth=2, 
            padx=30, 
            pady=30,
            bg="white"
        )
        login_container.grid(row=1, column=0, columnspan=2, pady=50, sticky="")
        login_container.grid_columnconfigure(1, weight=1)

        # Judul Login
        tk.Label(
            login_container, 
            text="HALAMAN LOGIN", 
            font=("Arial", 16, "bold"),
            bg="white"
        ).grid(row=0, column=0, columnspan=2, pady=(0, 30))

        # Input Username
        tk.Label(
            login_container, 
            text="Username:", 
            font=("Arial", 12),
            bg="white"
        ).grid(row=1, column=0, sticky="W", pady=8, padx=(0, 10))

        self.entry_username = tk.Entry(login_container, font=("Arial", 12), width=25)
        self.entry_username.grid(row=1, column=1, pady=8, sticky="EW")

        # Input Password dengan frame untuk tombol show/hide
        tk.Label(
            login_container, 
            text="Password:", 
            font=("Arial", 12),
            bg="white"
        ).grid(row=2, column=0, sticky="W", pady=8, padx=(0, 10))

        password_frame = tk.Frame(login_container, bg="white")
        password_frame.grid(row=2, column=1, pady=8, sticky="EW")
        password_frame.grid_columnconfigure(0, weight=1)

        self.entry_password = tk.Entry(
            password_frame, 
            font=("Arial", 12), 
            show="*",
            width=20
        )
        self.entry_password.grid(row=0, column=0, sticky="EW", padx=(0, 5))

        # Tombol Show/Hide Password
        self.btn_show_password = tk.Button(
            password_frame,
            text="👁",
            font=("Arial", 10),
            command=self._toggle_password_visibility,
            width=3
        )
        self.btn_show_password.grid(row=0, column=1)

        # Remember Me Checkbox
        self.var_remember = tk.IntVar()
        self.check_remember = tk.Checkbutton(
            login_container,
            text="Remember Me",
            variable=self.var_remember,
            font=("Arial", 10),
            bg="white"
        )
        self.check_remember.grid(row=3, column=0, columnspan=2, pady=10, sticky="W")

        # Tombol Login
        self.btn_login = tk.Button(
            login_container, 
            text="Login", 
            font=("Arial", 12, "bold"),
            command=self._coba_login,
            bg="lightblue",
            relief=tk.RAISED,
            padx=20,
            pady=5
        )
        self.btn_login.grid(row=4, column=0, columnspan=2, pady=20, sticky="EW")

        # Keyboard shortcuts untuk login
        self.entry_username.bind("<Return>", lambda e: self.entry_password.focus_set())
        self.entry_password.bind("<Return>", lambda e: self._coba_login())

        # Info untuk user dengan background yang sama
        info_label = tk.Label(
            login_container,
            text="Info: Username yang tersedia:\nadmin (password: 123)\nuser1 (password: password1)\nmahasiswa (password: 123456)",
            font=("Arial", 9),
            fg="gray",
            justify=tk.LEFT,
            bg="white"
        )
        info_label.grid(row=5, column=0, columnspan=2, pady=(10, 0))

    def _toggle_password_visibility(self):
        """Toggle show/hide password"""
        if self.entry_password.cget('show') == '':
            self.entry_password.config(show='*')
            self.btn_show_password.config(text="👁")
        else:
            self.entry_password.config(show='')
            self.btn_show_password.config(text="🙈")

    def _save_remember_me(self, username):
        """Simpan username untuk remember me"""
        try:
            data = {"username": username if self.var_remember.get() else ""}
            with open(self.remember_file, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            logging.error(f"Error saving remember me: {str(e)}")

    def _load_remember_me(self):
        """Load username dari remember me"""
        try:
            if os.path.exists(self.remember_file):
                with open(self.remember_file, 'r') as f:
                    data = json.load(f)
                    if data.get("username"):
                        self.entry_username.insert(0, data["username"])
                        self.var_remember.set(1)
        except Exception as e:
            logging.error(f"Error loading remember me: {str(e)}")

    def _coba_login(self):
        """Method untuk memproses attempt login dengan logging"""
        username = self.entry_username.get().strip()
        password = self.entry_password.get()

        # Log attempt login
        logging.info(f"Login attempt for username: {username}")

        # Validasi input kosong
        if not username or not password:
            logging.warning(f"Empty credentials attempt for username: {username}")
            messagebox.showwarning("Login Gagal", "Username dan Password tidak boleh kosong.")
            self.entry_username.focus_set()
            return

        # Validasi panjang minimum
        if len(username) < 3:
            logging.warning(f"Username too short: {username}")
            messagebox.showwarning("Login Gagal", "Username minimal 3 karakter.")
            self.entry_username.focus_set()
            return

        # Cek kredensial di database
        if username in self.users_db and self.users_db[username] == password:
            self.current_user = username
            logging.info(f"Successful login for user: {username}")
            
            # Save remember me
            self._save_remember_me(username)
            
            messagebox.showinfo("Login Berhasil", f"Selamat Datang, {username}!")
            self._reset_form_biodata()
            self._update_title_with_user()
            self._pindah_ke(self.frame_biodata)
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
        else:
            logging.warning(f"Failed login attempt for username: {username}")
            messagebox.showerror("Login Gagal", "Username atau Password salah.")
            self.entry_password.delete(0, tk.END)
            self.entry_username.focus_set()

    def _logout(self):
        """Method untuk logout dengan logging"""
        if messagebox.askyesno("Logout", f"Apakah {self.current_user} yakin ingin logout?"):
            logging.info(f"User logout: {self.current_user}")
            # Reset status user
            self.current_user = None
            # Update title
            self._update_title_with_user()
            # Bersihkan field login
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            # Load remember me data
            self._load_remember_me()
            # Reset form biodata
            self._reset_form_biodata()
            # Kembali ke halaman login
            self._pindah_ke(self.frame_login)
            # Focus ke username field
            self.entry_username.focus_set()

    # === METHODS UNTUK BIODATA ===
    def _buat_tampilan_biodata(self):
        # --- Variabel Kontrol Tkinter ---
        self.var_nama = tk.StringVar()
        self.var_nim = tk.StringVar()
        self.var_jurusan = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_telepon = tk.StringVar()
        self.var_jk = tk.StringVar(value="Pria")
        self.var_setuju = tk.IntVar()

        # --- Frame Utama ---
        self.frame_biodata = tk.Frame(master=self, padx=20, pady=20, bg="lavender")
        self.frame_biodata.pack(fill=tk.BOTH, expand=True)
        self.frame_biodata.columnconfigure(1, weight=1)

        # Aktifkan trace untuk validasi real-time
        self.var_nama.trace_add("write", self.validate_form)
        self.var_nim.trace_add("write", self.validate_form)
        self.var_jurusan.trace_add("write", self.validate_form)
        self.var_email.trace_add("write", self.validate_form)
        self.var_telepon.trace_add("write", self.validate_form)

        # --- Judul ---
        self.label_judul = tk.Label(
            master=self.frame_biodata,
            text="FORM BIODATA MAHASISWA",
            font=("Arial", 16, "bold"),
            bg="lavender"
        )
        self.label_judul.grid(row=0, column=0, columnspan=2, pady=20)

        # --- Frame Input ---
        self.frame_input = tk.Frame(
            master=self.frame_biodata,
            relief=tk.GROOVE,
            borderwidth=2,
            padx=10,
            pady=10,
            bg="white"
        )
        self.frame_input.grid(row=1, column=0, columnspan=2, sticky="EW")
        self.frame_input.columnconfigure(1, weight=1)

        # Input Nama
        self.label_nama = tk.Label(master=self.frame_input, text="Nama Lengkap:", font=("Arial", 12), bg="white")
        self.label_nama.grid(row=0, column=0, sticky="W", pady=2)
        self.entry_nama = tk.Entry(master=self.frame_input, font=("Arial", 12), textvariable=self.var_nama)
        self.entry_nama.grid(row=0, column=1, pady=2, sticky="EW")

        # Input NIM
        self.label_nim = tk.Label(master=self.frame_input, text="NIM:", font=("Arial", 12), bg="white")
        self.label_nim.grid(row=1, column=0, sticky="W", pady=2)
        self.entry_nim = tk.Entry(master=self.frame_input, font=("Arial", 12), textvariable=self.var_nim)
        self.entry_nim.grid(row=1, column=1, pady=2, sticky="EW")

        # Input Jurusan
        self.label_jurusan = tk.Label(master=self.frame_input, text="Jurusan:", font=("Arial", 12), bg="white")
        self.label_jurusan.grid(row=2, column=0, sticky="W", pady=2)
        self.entry_jurusan = tk.Entry(master=self.frame_input, font=("Arial", 12), textvariable=self.var_jurusan)
        self.entry_jurusan.grid(row=2, column=1, pady=2, sticky="EW")

        # Input Email
        self.label_email = tk.Label(master=self.frame_input, text="Email:", font=("Arial", 12), bg="white")
        self.label_email.grid(row=3, column=0, sticky="W", pady=2)
        self.entry_email = tk.Entry(master=self.frame_input, font=("Arial", 12), textvariable=self.var_email)
        self.entry_email.grid(row=3, column=1, pady=2, sticky="EW")

        # Input Telepon
        self.label_telepon = tk.Label(master=self.frame_input, text="Telepon:", font=("Arial", 12), bg="white")
        self.label_telepon.grid(row=4, column=0, sticky="W", pady=2)
        self.entry_telepon = tk.Entry(master=self.frame_input, font=("Arial", 12), textvariable=self.var_telepon)
        self.entry_telepon.grid(row=4, column=1, pady=2, sticky="EW")

        # Input Tanggal Lahir
        self.label_tgl_lahir = tk.Label(master=self.frame_input, text="Tanggal Lahir:", font=("Arial", 12), bg="white")
        self.label_tgl_lahir.grid(row=5, column=0, sticky="W", pady=2)
        
        # Frame untuk tanggal lahir
        self.frame_tgl_lahir = tk.Frame(master=self.frame_input, bg="white")
        self.frame_tgl_lahir.grid(row=5, column=1, pady=2, sticky="EW")
        
        # ComboBox untuk tanggal, bulan, tahun
        self.combo_hari = ttk.Combobox(self.frame_tgl_lahir, width=5, values=[str(i) for i in range(1, 32)])
        self.combo_hari.grid(row=0, column=0, padx=(0, 5))
        self.combo_hari.set("1")
        
        self.combo_bulan = ttk.Combobox(self.frame_tgl_lahir, width=12, values=[
            "Januari", "Februari", "Maret", "April", "Mei", "Juni",
            "Juli", "Agustus", "September", "Oktober", "November", "Desember"
        ])
        self.combo_bulan.grid(row=0, column=1, padx=(0, 5))
        self.combo_bulan.set("Januari")
        
        current_year = datetime.datetime.now().year
        self.combo_tahun = ttk.Combobox(self.frame_tgl_lahir, width=8, values=[str(i) for i in range(1950, current_year + 1)])
        self.combo_tahun.grid(row=0, column=2)
        self.combo_tahun.set(str(current_year - 20))

        # Input Alamat
        self.label_alamat = tk.Label(master=self.frame_input, text="Alamat:", font=("Arial", 12), bg="white")
        self.label_alamat.grid(row=6, column=0, sticky="NW", pady=2)

        self.frame_alamat = tk.Frame(master=self.frame_input, relief=tk.SUNKEN, borderwidth=1)
        self.frame_alamat.grid(row=6, column=1, pady=2, sticky="EW")
        self.frame_alamat.columnconfigure(0, weight=1)

        self.scrollbar_alamat = tk.Scrollbar(master=self.frame_alamat)
        self.scrollbar_alamat.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_alamat = tk.Text(master=self.frame_alamat, height=4, font=("Arial", 12), wrap="word")
        self.text_alamat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar_alamat.config(command=self.text_alamat.yview)
        self.text_alamat.config(yscrollcommand=self.scrollbar_alamat.set)

        # Jenis Kelamin
        self.label_jk = tk.Label(master=self.frame_input, text="Jenis Kelamin:", font=("Arial", 12), bg="white")
        self.label_jk.grid(row=7, column=0, sticky="W", pady=2)

        self.frame_jk = tk.Frame(master=self.frame_input, bg="white")
        self.frame_jk.grid(row=7, column=1, sticky="W")

        self.radio_pria = tk.Radiobutton(master=self.frame_jk, text="Pria", variable=self.var_jk, value="Pria", bg="white")
        self.radio_pria.pack(side=tk.LEFT)
        self.radio_wanita = tk.Radiobutton(master=self.frame_jk, text="Wanita", variable=self.var_jk, value="Wanita", bg="white")
        self.radio_wanita.pack(side=tk.LEFT)

        # Checkbox Persetujuan
        self.check_setuju = tk.Checkbutton(
            master=self.frame_input,
            text="Saya menyetujui pengumpulan data ini.",
            variable=self.var_setuju,
            font=("Arial", 10),
            command=self.validate_form,
            bg="white"
        )
        self.check_setuju.grid(row=8, column=0, columnspan=2, pady=10, sticky="W")

        # Frame untuk tombol
        self.frame_buttons = tk.Frame(master=self.frame_biodata, bg="lavender")
        self.frame_buttons.grid(row=6, column=0, columnspan=2, pady=20, sticky="EW")
        self.frame_buttons.columnconfigure(0, weight=1)
        self.frame_buttons.columnconfigure(1, weight=1)

        # Tombol Reset
        self.btn_reset = tk.Button(
            master=self.frame_buttons,
            text="Reset Form",
            font=("Arial", 12, "bold"),
            command=self._reset_form_biodata,
            bg="orange",
            relief=tk.RAISED,
            padx=20,
            pady=5
        )
        self.btn_reset.grid(row=0, column=0, padx=(0, 10), sticky="EW")

        # Tombol Submit
        self.btn_submit = tk.Button(
            master=self.frame_buttons,
            text="Submit Biodata",
            font=("Arial", 12, "bold"),
            command=self.submit_data,
            state=tk.DISABLED,
            bg="lightblue",
            relief=tk.RAISED,
            padx=20,
            pady=5
        )
        self.btn_submit.grid(row=0, column=1, padx=(10, 0), sticky="EW")

        # Hover dan Shortcut
        self.btn_submit.bind("<Enter>", self.on_enter)
        self.btn_submit.bind("<Leave>", self.on_leave)

        self.entry_nama.bind("<Return>", self.submit_shortcut)
        self.entry_nim.bind("<Return>", self.submit_shortcut)
        self.entry_jurusan.bind("<Return>", self.submit_shortcut)
        self.entry_email.bind("<Return>", self.submit_shortcut)
        self.entry_telepon.bind("<Return>", self.submit_shortcut)
        self.text_alamat.bind("<Return>", self.submit_shortcut)

        # Label Hasil
        self.label_hasil = tk.Label(
            master=self.frame_biodata,
            text="",
            font=("Arial", 12, "italic"),
            justify=tk.LEFT,
            background="lavender"
        )
        self.label_hasil.grid(row=7, column=0, columnspan=2, sticky="W", padx=10)

        # Membuat menu
        self._buat_menu()

    # === VALIDATION METHODS ===
    def _validate_email(self, email):
        """Validasi format email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def _validate_phone(self, phone):
        """Validasi format telepon Indonesia"""
        # Format yang diterima: +62xxx, 08xxx, 62xxx
        pattern = r'^(\+62|62|0)8[1-9][0-9]{6,9}$'
        return re.match(pattern, phone) is not None

    def submit_data(self):
        """Submit data biodata dengan validasi lengkap"""
        try:
            # Cek checkbox
            if self.var_setuju.get() == 0:
                messagebox.showwarning("Peringatan", "Anda harus menyetujui pengumpulan data!")
                return

            # Ambil data dari form
            nama = self.entry_nama.get().strip()
            nim = self.entry_nim.get().strip()
            jurusan = self.entry_jurusan.get().strip()
            email = self.entry_email.get().strip()
            telepon = self.entry_telepon.get().strip()
            alamat = self.text_alamat.get("1.0", tk.END).strip()
            jenis_kelamin = self.var_jk.get()
            
            # Format tanggal lahir
            tgl_lahir = f"{self.combo_hari.get()} {self.combo_bulan.get()} {self.combo_tahun.get()}"

            # Validasi field kosong
            if not nama or not nim or not jurusan or not email or not telepon:
                messagebox.showwarning("Input Kosong", "Nama, NIM, Jurusan, Email, dan Telepon harus diisi!")
                return
            
            # Validasi format NIM (harus angka dan minimal 8 digit)
            if not nim.isdigit() or len(nim) < 8:
                messagebox.showwarning("Format NIM Salah", "NIM harus berupa angka minimal 8 digit!")
                self.entry_nim.focus_set()
                return

            # Validasi nama (tidak boleh hanya angka)
            if nama.isdigit():
                messagebox.showwarning("Format Nama Salah", "Nama tidak boleh hanya berupa angka!")
                self.entry_nama.focus_set()
                return

            # Validasi email
            if not self._validate_email(email):
                messagebox.showwarning("Format Email Salah", "Format email tidak valid!\nContoh: nama@domain.com")
                self.entry_email.focus_set()
                return

            # Validasi telepon
            if not self._validate_phone(telepon):
                messagebox.showwarning("Format Telepon Salah", "Format telepon tidak valid!\nContoh: 08123456789, +628123456789")
                self.entry_telepon.focus_set()
                return

            # Tampilkan hasil
            hasil = f"Nama: {nama}\nNIM: {nim}\nJurusan: {jurusan}\nEmail: {email}\nTelepon: {telepon}\nTanggal Lahir: {tgl_lahir}\nAlamat: {alamat}\nJenis Kelamin: {jenis_kelamin}"
            messagebox.showinfo("Data Tersimpan", hasil)

            # Tampilkan hasil di label dengan info user
            hasil_lengkap = f"BIODATA TERSIMPAN:\nDiinput oleh: {self.current_user}\n\n{hasil}"
            self.label_hasil.config(text=hasil_lengkap)

            logging.info(f"Data submitted by user: {self.current_user} - NIM: {nim}")

        except Exception as e:
            logging.error(f"Error in submit_data by {self.current_user}: {str(e)}")
            messagebox.showerror("Error", f"Terjadi kesalahan saat memproses data:\n{str(e)}")

    def validate_form(self, *args):
        nama_valid = self.var_nama.get().strip() != ""
        nim_valid = self.var_nim.get().strip() != ""
        jurusan_valid = self.var_jurusan.get().strip() != ""
        email_valid = self.var_email.get().strip() != ""
        telepon_valid = self.var_telepon.get().strip() != ""
        setuju_valid = self.var_setuju.get() == 1

        if nama_valid and nim_valid and jurusan_valid and email_valid and telepon_valid and setuju_valid:
            self.btn_submit.config(state=tk.NORMAL)
        else:
            self.btn_submit.config(state=tk.DISABLED)

    def _reset_form_biodata(self):
        """Reset semua field di form biodata"""
        if messagebox.askyesno("Reset Form", "Apakah Anda yakin ingin mereset semua field?"):
            self.var_nama.set("")
            self.var_nim.set("")
            self.var_jurusan.set("")
            self.var_email.set("")
            self.var_telepon.set("")
            self.text_alamat.delete("1.0", tk.END)
            self.var_jk.set("Pria")
            self.var_setuju.set(0)
            self.label_hasil.config(text="")
            self.combo_hari.set("1")
            self.combo_bulan.set("Januari")
            current_year = datetime.datetime.now().year
            self.combo_tahun.set(str(current_year - 20))
            self.entry_nama.focus_set()

    # === EVENT HANDLERS ===
    def on_enter(self, event):
        if self.btn_submit['state'] == tk.NORMAL:
            self.btn_submit.config(bg="darkblue", fg="white")

    def on_leave(self, event):
        self.btn_submit.config(bg="lightblue", fg="black")

    def submit_shortcut(self, event=None):
        if self.btn_submit['state'] == tk.NORMAL:
            self.submit_data()

    # === UTILITY METHODS ===
    def _update_title_with_user(self):
        """Update judul window dengan nama user yang login"""
        if self.current_user:
            self.title(f"Aplikasi Biodata Mahasiswa - User: {self.current_user}")
        else:
            self.title("Aplikasi Biodata Mahasiswa")

    # === MENU METHODS ===
    def _buat_menu(self):
        """Membuat menu bar untuk aplikasi"""
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)

        file_menu = tk.Menu(master=menu_bar, tearoff=0)
        file_menu.add_command(label="Simpan Hasil", command=self.simpan_hasil)
        file_menu.add_separator()
        file_menu.add_command(label="Reset Form", command=self._reset_form_biodata)
        file_menu.add_separator()
        file_menu.add_command(label="Logout", command=self._logout)
        file_menu.add_separator()
        file_menu.add_command(label="Keluar", command=self.destroy)

        menu_bar.add_cascade(label="File", menu=file_menu)

    def _hapus_menu(self):
        """Menghapus menu bar dari window."""
        empty_menu = tk.Menu(self)
        self.config(menu=empty_menu)

    # === FILE OPERATIONS ===
    def simpan_hasil(self):
        """Simpan hasil biodata ke file dengan error handling"""
        try:
            hasil_tersimpan = self.label_hasil.cget("text")

            if not hasil_tersimpan or "BIODATA TERSIMPAN" not in hasil_tersimpan:
                messagebox.showwarning("Peringatan", "Tidak ada data untuk disimpan. Mohon submit terlebih dahulu.")
                return

            # Buat nama file dengan timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"biodata_{self.current_user}_{timestamp}.txt"

            with open(filename, "w", encoding="utf-8") as file:
                file.write(f"Data disimpan oleh: {self.current_user}\n")
                file.write(f"Waktu penyimpanan: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write("-" * 50 + "\n")
                file.write(hasil_tersimpan)

            messagebox.showinfo("Info", f"Data berhasil disimpan ke file '{filename}'.")

        except PermissionError:
            messagebox.showerror("Error", "Tidak memiliki izin untuk menyimpan file di lokasi ini.")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat menyimpan file:\n{str(e)}")

    def keluar_aplikasi(self):
        """Keluar dari aplikasi dengan konfirmasi"""
        if messagebox.askokcancel("Keluar", "Apakah Anda yakin ingin keluar dari aplikasi?"):
            logging.info(f"Application closed by user: {self.current_user}")
            self.destroy()


# Blok berikut hanya akan dieksekusi jika file ini dijalankan secara langsung
if __name__ == "__main__":
    app = AplikasiBiodata()
    app.mainloop()
