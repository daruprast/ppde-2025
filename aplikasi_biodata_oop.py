import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime
import logging
import os
import json
import re

PRIMARY_GREEN = "#006b3f"
ACCENT_GOLD = "#c7932c"
BG_LIGHT = "#F5E6A8"  # Kuning cream dari palette
TEXT_DARK = "#2f2f2f"
FORM_BG = "#ffffff"
ORANGE_ACCENT = "#F4A261"
RED_ACCENT = "#A4343A"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(SCRIPT_DIR, "logo-uinsk.png")

def _load_logo(path: str, max_width: int = 140):
    if not os.path.isfile(path):
        return None
    try:
        img = tk.PhotoImage(file=path)
        w = img.width()
        if w > max_width:
            factor = (w + max_width - 1) // max_width
            factor = max(1, factor)
            img = img.subsample(factor)
        return img
    except Exception:
        return None

# Data Fakultas dan Prodi (untuk dropdown terhubung)
fakultas_options = [    
    "Pilih Fakultas...",
    "Fakultas Adab dan Ilmu Budaya",
    "Fakultas Dakwah dan Komunikasi", 
    "Fakultas Ilmu Tarbiyah dan Keguruan",
    "Fakultas Syariah dan Hukum",
    "Fakultas Ushuluddin dan Pemikiran Islam",
    "Fakultas Sains dan Teknologi",
    "Fakultas Kedokteran",
    "Fakultas Ilmu Sosial dan Humaniora",
    "Fakultas Ekonomi dan Bisnis Islam"
]

jurusan_per_fakultas = {
    "Fakultas Adab dan Ilmu Budaya": [
        "Bahasa dan Sastra Arab", "Sejarah dan Kebudayaan Islam", 
        "Ilmu Perpustakaan dan Informasi", "Sastra Inggris"
    ],
    "Fakultas Dakwah dan Komunikasi": [
        "Komunikasi dan Penyiaran Islam", "Bimbingan dan Konseling Islam",
        "Pengembangan Masyarakat Islam", "Manajemen Dakwah", "Ilmu Kesejahteraan Sosial"
    ],
    "Fakultas Ilmu Tarbiyah dan Keguruan": [
        "Pendidikan Agama Islam", "Pendidikan Bahasa Arab", "Pendidikan Bahasa Inggris",
        "Pendidikan Matematika", "Pendidikan Biologi", "Pendidikan Fisika", 
        "Pendidikan Kimia", "Pendidikan Guru Madrasah Ibtidaiyah", "Pendidikan Islam Anak Usia Dini",
        "Manajemen Pendidikan Islam"
    ],
    "Fakultas Syariah dan Hukum": [
        "Hukum Keluarga Islam (Ahwal Syakhshiyyah)", "Hukum Tata Negara (Siyasah)",
        "Perbandingan Mazhab", "Hukum Ekonomi Syariah (Muamalah)", "Ilmu Hukum"
    ],
    "Fakultas Ushuluddin dan Pemikiran Islam": [
        "Aqidah dan Filsafat Islam", "Ilmu Al-Qur'an dan Tafsir",
        "Ilmu Hadits", "Perbandingan Agama", "Studi Agama-Agama"
    ],
    "Fakultas Sains dan Teknologi": [
        "Matematika", "Fisika", "Kimia", "Biologi", "Informatika",
        "Teknik Industri", "Arsitektur"
    ],
    "Fakultas Kedokteran": [
        "Pendidikan Dokter", "Biomedis"
    ],
    "Fakultas Ilmu Sosial dan Humaniora": [
        "Psikologi", "Ilmu Komunikasi"
    ],
    "Fakultas Ekonomi dan Bisnis Islam": [
        "Ekonomi Syariah", "Perbankan Syariah", "Akuntansi Syariah",
        "Manajemen Keuangan Syariah"
    ]
}

# Konfigurasi logging aplikasi
logging.basicConfig(
    filename="aplikasi_biodata.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

class AplikasiBiodata(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window config
        self.title("Aplikasi Biodata Mahasiswa")
        self.geometry("680x760")
        self.configure(bg=BG_LIGHT)
        self.resizable(True, True)
        self.protocol("WM_DELETE_WINDOW", self.keluar_aplikasi)

        # Database user sederhana
        self.users_db = {
            "admin": "123",
            "user1": "password1",
            "mahasiswa": "123456",
        }

        # Prefs & state
        self._prefs_path = os.path.join(os.path.dirname(__file__), "biodata_prefs.json")
        self._password_visible = False
        self.current_user = None
        self.frame_aktif = None
        self.prefs = self._load_prefs()

        # Siapkan tampilan dan menu
        self._buat_tampilan_login()
        self._buat_tampilan_biodata()
        self._buat_menu()

        # Tampilkan login dulu
        self._pindah_ke(self.frame_login)
        logging.info("Aplikasi dimulai")

    # ---------------- Login ----------------
    def _buat_tampilan_login(self):
        self.frame_login = tk.Frame(master=self, padx=20, pady=40, bg=BG_LIGHT)
        self.frame_login.grid_columnconfigure(0, weight=1)
        
        # Header frame untuk logo dan judul login
        header_login_frame = tk.Frame(master=self.frame_login, bg=BG_LIGHT)
        header_login_frame.grid(row=0, column=0, pady=(0, 20))
        
        # Logo UIN di halaman login
        self.logo_login = _load_logo(LOGO_PATH, max_width=160)
        if self.logo_login:
            lbl_logo_login = tk.Label(header_login_frame, image=self.logo_login, bg=BG_LIGHT)
            lbl_logo_login.pack(pady=(0, 5))
            
            # Teks universitas di halaman login
            label_univ_login = tk.Label(header_login_frame, text="UIN SUNAN KALIJAGA YOGYAKARTA", 
                                       font=("Segoe UI", 11, "bold"), bg=BG_LIGHT, fg="#84994F")
            label_univ_login.pack(pady=(0, 10))
        
        # Header HALAMAN LOGIN
        tk.Label(
            header_login_frame,
            text="HALAMAN LOGIN",
            font=("Segoe UI", 18, "bold"),
            bg=BG_LIGHT,
            fg="#2c3e50",
        ).pack()

        # Kartu/Panel login dengan border & padding
        self.frame_login_card = tk.Frame(
            self.frame_login,
            relief=tk.GROOVE,
            borderwidth=2,
            padx=16,
            pady=16,
            bg="white",
            highlightthickness=2,
            highlightbackground=ACCENT_GOLD,
        )
        self.frame_login_card.grid(row=1, column=0, sticky="EW")
        self.frame_login_card.grid_columnconfigure(0, weight=0)
        self.frame_login_card.grid_columnconfigure(1, weight=1)

        tk.Label(
            self.frame_login_card,
            text="Username:",
            font=("Arial", 12),
            anchor="w",
            justify=tk.LEFT,
        ).grid(row=0, column=0, sticky="W", pady=5, padx=(0, 6))
        self.entry_username = tk.Entry(self.frame_login_card, font=("Arial", 12))
        self.entry_username.grid(row=0, column=1, pady=5, sticky="EW")

        tk.Label(
            self.frame_login_card,
            text="Password:",
            font=("Arial", 12),
            anchor="w",
            justify=tk.LEFT,
        ).grid(row=1, column=0, sticky="W", pady=5, padx=(0, 6))
        # Frame untuk password + toggle show/hide
        self.frame_password = tk.Frame(self.frame_login_card, bg="white")
        self.frame_password.grid(row=1, column=1, pady=5, sticky="EW")
        self.frame_password.grid_columnconfigure(0, weight=1)
        self.entry_password = tk.Entry(self.frame_password, font=("Arial", 12), show="*")
        self.entry_password.grid(row=0, column=0, sticky="EW")
        self.btn_toggle_pwd = tk.Button(
            self.frame_password,
            text="Show",
            width=6,
            command=self._toggle_password_visibility,
        )
        self.btn_toggle_pwd.grid(row=0, column=1, padx=(6, 0))

        # Remember Me
        self.var_remember = tk.IntVar(value=1 if self.prefs.get("remember", False) else 0)
        self.chk_remember = tk.Checkbutton(self.frame_login_card, text="Remember Me", variable=self.var_remember, bg="white")
        self.chk_remember.grid(row=2, column=0, columnspan=2, sticky="W", pady=(2, 8))

        self.btn_login = tk.Button(
            self.frame_login,
            text="Login",
            font=("Arial", 12, "bold"),
            command=self._coba_login,
            bg=PRIMARY_GREEN,
            fg="white",
            activebackground=ACCENT_GOLD,
            activeforeground="white",
            relief=tk.RAISED,
            cursor="hand2",
        )
        self.btn_login.grid(row=2, column=0, pady=20, sticky="EW")

        # Shortcuts
        self.entry_username.bind("<Return>", lambda e: self.entry_password.focus_set())
        self.entry_password.bind("<Return>", lambda e: self._coba_login())

        tk.Label(
            self.frame_login,
            font=("Arial", 9),
            fg="gray",
            justify=tk.LEFT,
        ).grid(row=3, column=0, columnspan=2, pady=10)

        # Prefill username dari prefs jika diingat
        remembered_username = self.prefs.get("remembered_username") if self.prefs.get("remember", False) else None
        if remembered_username:
            self.entry_username.insert(0, remembered_username)
            self.after(50, lambda: self.entry_password.focus_set())
        self.frame_login.bind("<Configure>", lambda e: self._update_login_label_wrap())

    def _coba_login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get()
        logging.info(f"Login attempt for username: {username}")

        if not username or not password:
            logging.warning("Empty credentials on login")
            messagebox.showwarning("Login Gagal", "Username dan Password tidak boleh kosong.")
            self.entry_username.focus_set()
            return

        if len(username) < 3:
            logging.warning("Username too short")
            messagebox.showwarning("Login Gagal", "Username minimal 3 karakter.")
            self.entry_username.focus_set()
            return

        if self.users_db.get(username) == password:
            self.current_user = username
            logging.info(f"Successful login: {username}")
            self._update_title_with_user()
            self._reset_form_biodata()
            self._pindah_ke(self.frame_biodata)
            # Simpan prefs jika Remember Me dicentang
            if self.var_remember.get() == 1:
                self.prefs["remember"] = True
                self.prefs["remembered_username"] = username
            else:
                self.prefs["remember"] = False
                self.prefs.pop("remembered_username", None)
            self._save_prefs()
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            self.after(100, lambda: self.entry_nama.focus_set())
        else:
            logging.warning(f"Failed login attempt: {username}")
            messagebox.showerror("Login Gagal", "Username atau Password salah.")
            self.entry_password.delete(0, tk.END)
            self.entry_username.focus_set()

    # ---------------- Biodata ----------------
    def _buat_tampilan_biodata(self):
        # Variabel kontrol
        self.var_nama = tk.StringVar()
        self.var_nim = tk.StringVar()
        # Dropdown Fakultas & Prodi
        self.var_fakultas = tk.StringVar(value="Pilih Fakultas...")
        self.var_prodi = tk.StringVar(value="Pilih Jurusan...")
        self.var_email = tk.StringVar()
        self.var_tel = tk.StringVar()
        self.var_tgl = tk.StringVar()  # format YYYY-MM-DD
        self.var_jk = tk.StringVar(value="Pria")
        self.var_setuju = tk.IntVar()

        # Frame utama biodata
        self.frame_biodata = tk.Frame(master=self, padx=20, pady=20)
        self.frame_biodata.columnconfigure(0, weight=1)
        self.frame_biodata.grid_rowconfigure(1, weight=1)
        self.frame_biodata.configure(bg=BG_LIGHT)

        # Header frame untuk logo dan judul
        header_frame = tk.Frame(master=self.frame_biodata, bg=BG_LIGHT)
        header_frame.grid(row=0, column=0, columnspan=2, pady=20)

        # Logo UIN di atas judul form biodata
        self.logo_image = _load_logo(LOGO_PATH, max_width=180)
        if self.logo_image:
            lbl_logo = tk.Label(header_frame, image=self.logo_image, bg=BG_LIGHT)
            lbl_logo.pack(pady=(0, 5))
            
            # Teks universitas
            label_univ = tk.Label(header_frame, text="UIN SUNAN KALIJAGA YOGYAKARTA", 
                                 font=("Segoe UI", 12, "bold"), bg=BG_LIGHT, fg="#84994F")
            label_univ.pack(pady=(0, 10))

        # Judul form
        tk.Label(
            header_frame,
            text="FORM BIODATA MAHASISWA",
            font=("Segoe UI", 18, "bold"),
            bg=BG_LIGHT,
            fg="#2c3e50",
        ).pack()

        # Frame input dengan styling sesuai referensi
        self.frame_input = tk.Frame(
            self.frame_biodata,
            relief=tk.GROOVE,
            borderwidth=2,
            padx=10,
            pady=10,
            bg=FORM_BG,
            highlightbackground=RED_ACCENT,
            highlightthickness=2,
        )
        self.frame_input.grid(row=1, column=0, columnspan=2, sticky="NSEW", padx=5, pady=5)
        self.frame_input.grid_columnconfigure(0, weight=0)  # Label column tetap ukuran
        self.frame_input.grid_columnconfigure(1, weight=1)  # Input column bisa expand

        # Nama Lengkap
        tk.Label(
            self.frame_input, 
            text="Nama Lengkap:", 
            font=("Segoe UI", 11), 
            bg=FORM_BG, 
            fg="#000000"
        ).grid(row=0, column=0, sticky="W", pady=2)
        self.entry_nama = tk.Entry(
            self.frame_input, 
            width=30, 
            font=("Segoe UI", 11), 
            textvariable=self.var_nama,
            bg=FORM_BG, 
            fg="#000000", 
            relief=tk.FLAT, 
            highlightthickness=1, 
            highlightbackground=ORANGE_ACCENT
        )
        self.entry_nama.grid(row=0, column=1, pady=2, sticky="EW")

        # NIM
        tk.Label(
            self.frame_input, 
            text="NIM:", 
            font=("Segoe UI", 11), 
            bg=FORM_BG, 
            fg="#000000"
        ).grid(row=1, column=0, sticky="W", pady=2)
        self.entry_nim = tk.Entry(
            self.frame_input, 
            width=30, 
            font=("Segoe UI", 11), 
            textvariable=self.var_nim,
            bg=FORM_BG, 
            fg="#000000", 
            relief=tk.FLAT, 
            highlightthickness=1, 
            highlightbackground=ORANGE_ACCENT
        )
        self.entry_nim.grid(row=1, column=1, pady=2, sticky="EW")

        # Fakultas dengan styling ttk.Combobox
        tk.Label(
            self.frame_input, 
            text="Fakultas:", 
            font=("Segoe UI", 11), 
            bg=FORM_BG, 
            fg="#000000"
        ).grid(row=2, column=0, sticky="W", pady=2)
        
        self.combo_fakultas = ttk.Combobox(
            self.frame_input, 
            textvariable=self.var_fakultas,
            values=fakultas_options[1:],  # Exclude "Pilih Fakultas..." dari values
            state="readonly",
            font=("Segoe UI", 11),
            width=28
        )
        self.combo_fakultas.set("Pilih Fakultas...")  # Set default text
        self.combo_fakultas.grid(row=2, column=1, pady=2, sticky="EW")
        self.combo_fakultas.bind("<<ComboboxSelected>>", self._update_jurusan_options)

        # Jurusan dengan styling ttk.Combobox
        tk.Label(
            self.frame_input, 
            text="Jurusan:", 
            font=("Segoe UI", 11), 
            bg=FORM_BG, 
            fg="#000000"
        ).grid(row=3, column=0, sticky="W", pady=2)
        
        self.combo_jurusan = ttk.Combobox(
            self.frame_input, 
            textvariable=self.var_prodi,
            values=[],  # Akan diisi berdasarkan fakultas
            state="disabled",  # Disabled sampai fakultas dipilih
            font=("Segoe UI", 11),
            width=28
        )
        self.combo_jurusan.set("Pilih Fakultas terlebih dahulu")
        self.combo_jurusan.grid(row=3, column=1, pady=2, sticky="EW")

        # Style untuk combobox agar sesuai tema
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TCombobox', 
                        fieldbackground=FORM_BG,
                        background=ORANGE_ACCENT,
                        bordercolor=ORANGE_ACCENT,
                        arrowcolor=RED_ACCENT)

        # Email
        tk.Label(
            self.frame_input, 
            text="Email:", 
            font=("Segoe UI", 11), 
            bg=FORM_BG, 
            fg="#000000"
        ).grid(row=4, column=0, sticky="W", pady=2)
        self.entry_email = tk.Entry(
            self.frame_input, 
            width=30, 
            font=("Segoe UI", 11), 
            textvariable=self.var_email,
            bg=FORM_BG, 
            fg="#000000", 
            relief=tk.FLAT, 
            highlightthickness=1, 
            highlightbackground=ORANGE_ACCENT
        )
        self.entry_email.grid(row=4, column=1, pady=2, sticky="EW")

        # Telepon
        tk.Label(
            self.frame_input, 
            text="Telepon:", 
            font=("Segoe UI", 11), 
            bg=FORM_BG, 
            fg="#000000"
        ).grid(row=5, column=0, sticky="W", pady=2)
        self.entry_tel = tk.Entry(
            self.frame_input, 
            width=30, 
            font=("Segoe UI", 11), 
            textvariable=self.var_tel,
            bg=FORM_BG, 
            fg="#000000", 
            relief=tk.FLAT, 
            highlightthickness=1, 
            highlightbackground=ORANGE_ACCENT
        )
        self.entry_tel.grid(row=5, column=1, pady=2, sticky="EW")

        # Alamat dengan styling yang diperbaiki
        tk.Label(
            self.frame_input, 
            text="Alamat:", 
            font=("Segoe UI", 11), 
            bg=FORM_BG, 
            fg="#000000"
        ).grid(row=6, column=0, sticky="NW", pady=2)

        self.frame_input.grid_rowconfigure(6, weight=1)  # Baris alamat bisa expand vertikal

        self.frame_alamat = tk.Frame(
            self.frame_input, 
            relief=tk.SUNKEN, 
            borderwidth=1, 
            bg=FORM_BG, 
            highlightbackground=ORANGE_ACCENT, 
            highlightthickness=1
        )
        self.scrollbar_alamat = tk.Scrollbar(master=self.frame_alamat)
        self.scrollbar_alamat.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_alamat = tk.Text(
            master=self.frame_alamat, 
            height=5, 
            width=28, 
            font=("Segoe UI", 11), 
            bg=FORM_BG, 
            fg="#000000", 
            relief=tk.FLAT, 
            highlightthickness=1, 
            highlightbackground=ORANGE_ACCENT
        )
        self.text_alamat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar_alamat.config(command=self.text_alamat.yview)
        self.text_alamat.config(yscrollcommand=self.scrollbar_alamat.set)
        self.frame_alamat.grid(row=6, column=1, pady=2, sticky="NSEW")

        # Jenis Kelamin
        tk.Label(
            self.frame_input, 
            text="Jenis Kelamin:", 
            font=("Segoe UI", 11), 
            bg=FORM_BG, 
            fg="#000000"
        ).grid(row=7, column=0, sticky="W", pady=2)
        self.frame_jk = tk.Frame(master=self.frame_input, bg=FORM_BG)
        self.frame_jk.grid(row=7, column=1, sticky="W")
        self.radio_pria = tk.Radiobutton(
            master=self.frame_jk, 
            text="Pria", 
            variable=self.var_jk, 
            value="Pria", 
            bg=FORM_BG, 
            fg="#000000", 
            selectcolor=ORANGE_ACCENT, 
            font=("Segoe UI", 10)
        )
        self.radio_pria.pack(side=tk.LEFT, padx=2)
        self.radio_wanita = tk.Radiobutton(
            master=self.frame_jk, 
            text="Wanita", 
            variable=self.var_jk, 
            value="Wanita", 
            bg=FORM_BG, 
            fg="#000000", 
            selectcolor=ORANGE_ACCENT, 
            font=("Segoe UI", 10)
        )
        self.radio_wanita.pack(side=tk.LEFT, padx=2)

        # Checkbox persetujuan
        self.check_setuju = tk.Checkbutton(
            master=self.frame_input,
            text="Saya menyetujui pengumpulan data ini.",
            variable=self.var_setuju,
            font=("Segoe UI", 10),
            command=self.validate_form,
            bg=FORM_BG,
            fg="#000000",
            selectcolor=ORANGE_ACCENT
        )
        self.check_setuju.grid(row=8, column=0, columnspan=2, pady=10, sticky="W")

        # Tombol submit dengan styling sesuai referensi
        self.btn_submit = tk.Button(
            master=self.frame_biodata, 
            text="Submit Biodata", 
            font=("Segoe UI", 12, "bold"),
            command=self.submit_data,
            state=tk.DISABLED,
            bg=ORANGE_ACCENT,
            fg="#ffffff",
            activebackground="#CE8245",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0,
            cursor="hand2"
        )
        self.btn_submit.grid(row=2, column=0, columnspan=2, pady=20, sticky="EW")

        # Label hasil
        self.label_hasil = tk.Label(
            master=self.frame_biodata, 
            text="", 
            font=("Segoe UI", 12, "italic"), 
            justify=tk.LEFT, 
            bg=BG_LIGHT, 
            fg="#000000"
        )
        self.label_hasil.grid(row=7, column=0, columnspan=2, sticky="W", padx=10)

        # Configure column weight untuk main frame
        self.frame_biodata.columnconfigure(1, weight=1)

        # Events dan bindings
        self.btn_submit.bind("<Enter>", self.on_enter)
        self.btn_submit.bind("<Leave>", self.on_leave)
        self.entry_nama.bind("<Return>", self.submit_shortcut)
        self.entry_nim.bind("<Return>", self.submit_shortcut)
        self.combo_fakultas.bind("<Return>", self.submit_shortcut)
        self.combo_jurusan.bind("<Return>", self.submit_shortcut)
        self.entry_email.bind("<Return>", self.submit_shortcut)
        self.entry_tel.bind("<Return>", self.submit_shortcut)
        self.text_alamat.bind("<Return>", self.submit_shortcut)

        # Trace untuk validasi real-time
        self.var_nama.trace_add("write", self.validate_form)
        self.var_nim.trace_add("write", self.validate_form)
        self.var_fakultas.trace_add("write", self.validate_form)
        self.var_prodi.trace_add("write", self.validate_form)
        self.var_email.trace_add("write", self.validate_form)
        self.var_tel.trace_add("write", self.validate_form)

    def _update_jurusan_options(self, event=None):
        """Update opsi jurusan berdasarkan fakultas yang dipilih"""
        fakultas_terpilih = self.var_fakultas.get()
        
        if fakultas_terpilih in jurusan_per_fakultas:
            # Update nilai combobox jurusan
            jurusan_list = jurusan_per_fakultas[fakultas_terpilih]
            self.combo_jurusan['values'] = jurusan_list
            self.combo_jurusan.set("Pilih Jurusan...")
            self.combo_jurusan.config(state="readonly")
        else:
            # Reset jika tidak ada fakultas yang dipilih
            self.combo_jurusan['values'] = []
            self.combo_jurusan.set("Pilih Fakultas terlebih dahulu")
            self.combo_jurusan.config(state="disabled")

        # Bind untuk real-time validation
        self.var_setuju.trace_add("write", self.validate_form)

        # Event bindings tambahan untuk combobox
        self.combo_fakultas.bind("<Return>", self.submit_shortcut)
        self.combo_jurusan.bind("<Return>", self.submit_shortcut)
        self.frame_biodata.bind("<Configure>", lambda e: self._update_form_label_wrap())
        self.frame_input.bind("<Configure>", lambda e: self._update_form_label_wrap())

        # Trace validasi
        self.var_nama.trace_add("write", self.validate_form)
        self.var_nim.trace_add("write", self.validate_form)
        self.var_fakultas.trace_add("write", self.validate_form)
        self.var_prodi.trace_add("write", self.validate_form)
        self.var_fakultas.trace_add("write", self._update_prodi_options)
        # Inisialisasi Prodi awal
        self._update_prodi_options()
        self.var_email.trace_add("write", self.validate_form)
        self.var_tel.trace_add("write", self.validate_form)
        self.var_tgl.trace_add("write", self.validate_form)

    # ---------------- Menu ----------------
    def _buat_menu(self):
        # Top bar Menubutton
        self.menu_topbar = tk.Frame(self, bg=BG_LIGHT)
        self.menu_button = tk.Menubutton(
            self.menu_topbar,
            text="Menu",
            relief=tk.RAISED,
            bg="white",
            activebackground=ACCENT_GOLD,
        )
        self.menu_button.pack(side=tk.LEFT, padx=8, pady=4)

        self.dropdown_menu = tk.Menu(self.menu_button, tearoff=0)
        self.dropdown_menu.add_command(label="Simpan Hasil", command=self.simpan_hasil)
        self.dropdown_menu.add_separator()
        self.dropdown_menu.add_command(label="Logout", command=self._logout)
        self.dropdown_menu.add_separator()
        self.dropdown_menu.add_command(label="Keluar", command=self.keluar_aplikasi)
        self.menu_button.config(menu=self.dropdown_menu)
        self.menu_button.bind("<Enter>", self._post_menu) # Hover untuk menampilkan opsi

    def _update_title_with_user(self):
        if self.current_user:
            self.title(f"Aplikasi Biodata Mahasiswa - User: {self.current_user}")
        else:
            self.title("Aplikasi Biodata Mahasiswa")

    # ---------------- Util & Events ----------------
    def _pindah_ke(self, frame_tujuan):
        if self.frame_aktif is not None:
            self.frame_aktif.pack_forget()
        if hasattr(self, 'menu_topbar'):
            if frame_tujuan == self.frame_login:
                self.menu_topbar.pack_forget()
            else:
                self.menu_topbar.pack(side=tk.TOP, fill=tk.X)
        self.frame_aktif = frame_tujuan
        self.frame_aktif.pack(fill=tk.BOTH, expand=True)

    def _post_menu(self, event=None):
        try:
            x = self.menu_button.winfo_rootx()
            y = self.menu_button.winfo_rooty() + self.menu_button.winfo_height()
            self.dropdown_menu.post(x, y)
        except Exception:
            pass

    def _update_prodi_options(self, *args):
        try:
            fak = self.var_fakultas.get()
            menu = self.option_prodi["menu"]
            menu.delete(0, "end")
            prodi_list = jurusan_per_fakultas.get(fak, [])
            if not prodi_list:
                self.var_prodi.set("Pilih Prodi...")
                menu.add_command(label="Pilih Prodi...", command=lambda v="Pilih Prodi...": self.var_prodi.set(v))
            else:
                # Set default ke item pertama
                self.var_prodi.set(prodi_list[0])
                for p in prodi_list:
                    menu.add_command(label=p, command=lambda v=p: self.var_prodi.set(v))
        except Exception:
            pass

    def validate_form(self, *args):
        nama = self.var_nama.get().strip()
        nim = self.var_nim.get().strip()
        fakultas = self.var_fakultas.get().strip()
        prodi = self.var_prodi.get().strip()
        alamat = self.text_alamat.get("1.0", tk.END).strip()
        setuju = self.var_setuju.get() == 1

        # Validasi yang lebih sederhana sesuai referensi
        nama_valid = nama != ""
        nim_valid = nim != ""
        fakultas_valid = fakultas not in ("", "Pilih Fakultas...")
        prodi_valid = prodi not in ("", "Pilih Jurusan...", "Pilih Fakultas terlebih dahulu")
        alamat_valid = alamat != ""

        if nama_valid and nim_valid and fakultas_valid and prodi_valid and alamat_valid and setuju:
            self.btn_submit.config(state=tk.NORMAL, bg=ORANGE_ACCENT, fg="white", cursor="hand2")
        else:
            disabled_bg = "#d3d3d3"
            self.btn_submit.config(state=tk.DISABLED, bg=disabled_bg, fg="#6b6b6b", cursor="arrow")

    def submit_data(self):
        try:
            if self.var_setuju.get() == 0:
                messagebox.showwarning("Peringatan", "Anda harus menyetujui pengumpulan data!")
                return

            nama = self.entry_nama.get()
            nim = self.entry_nim.get()
            fakultas = self.var_fakultas.get()
            prodi = self.var_prodi.get()  # Menggunakan var_prodi untuk jurusan
            alamat = self.text_alamat.get("1.0", tk.END).strip()
            jenis_kelamin = self.var_jk.get()

            if not nama or not nim or not fakultas or not prodi or not alamat:
                messagebox.showwarning("Input Kosong", "Semua field harus diisi!")
                return

            hasil = f"Nama: {nama}\nNIM: {nim}\nFakultas: {fakultas}\nJurusan: {prodi}\nAlamat: {alamat}\nJenis Kelamin: {jenis_kelamin}" 

            # Tampilkan hasil di label
            self.label_hasil.config(text=f"BIODATA TERSIMPAN:\n\n{hasil}")

            messagebox.showinfo("Data Tersimpan", hasil)
            logging.info(f"Data biodata berhasil disimpan untuk: {nama} ({nim})")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
            logging.error(f"Error saat submit data: {str(e)}")

    def simpan_hasil(self):
        try:
            hasil_tersimpan = self.label_hasil.cget("text")
            if not hasil_tersimpan or "BIODATA TERSIMPAN" not in hasil_tersimpan:
                messagebox.showwarning("Peringatan", "Tidak ada data untuk disimpan. Mohon submit terlebih dahulu.")
                return

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"biodata_{(self.current_user or 'anon')}_{timestamp}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"Data disimpan oleh: {self.current_user or '-'}\n")
                f.write(
                    f"Waktu penyimpanan: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                )
                f.write("-" * 50 + "\n")
                f.write(hasil_tersimpan)

            logging.info(f"Saved biodata file: {filename}")
            messagebox.showinfo("Info", f"Data berhasil disimpan ke file '{filename}'.")
        except PermissionError:
            messagebox.showerror("Error", "Tidak memiliki izin untuk menyimpan file di lokasi ini.")
        except Exception as e:
            logging.error(f"Error saving file: {str(e)}")
            messagebox.showerror("Error", f"Terjadi kesalahan saat menyimpan file:\n{str(e)}")

    def _reset_form_biodata(self):
        self.var_nama.set("")
        self.var_nim.set("")
        self.var_fakultas.set(fakultas_options[0])
        self.var_prodi.set("Pilih Prodi...")
        self.var_email.set("")
        self.var_tel.set("")
        self.var_tgl.set("")
        self.text_alamat.delete("1.0", tk.END)
        self.var_jk.set("Pria")
        self.var_setuju.set(0)
        self.label_hasil.config(text="")
        self.validate_form()

    def _logout(self):
        if not self.current_user:
            self._pindah_ke(self.frame_login)
            return
        ask_yes_no = getattr(messagebox, 'askyesno', None)
        if ask_yes_no is not None:
            confirm = ask_yes_no("Logout", f"Apakah {self.current_user} yakin ingin logout?")
        else:
            confirm = messagebox.askquestion("Logout", f"Apakah {self.current_user} yakin ingin logout?") == 'yes'

        if confirm:
            logging.info(f"User logout: {self.current_user}")
            self.current_user = None
            self._update_title_with_user()
            self._reset_form_biodata()
            self._pindah_ke(self.frame_login)
            self.entry_username.focus_set()

    def keluar_aplikasi(self):
        if messagebox.askokcancel("Keluar", "Apakah Anda yakin ingin keluar dari aplikasi?"):
            logging.info(f"Application closed by user: {self.current_user}")
            self.destroy()

    def on_enter(self, event):
        if self.btn_submit["state"] == tk.NORMAL:
            self.btn_submit.config(bg="#CE8245")

    def on_leave(self, event):
        self.btn_submit.config(bg=ORANGE_ACCENT)

    def submit_shortcut(self, event=None):
        if self.btn_submit["state"] == tk.NORMAL:
            self.submit_data()
            return "break"

    # ---------------- Helpers ----------------
    def _update_form_label_wrap(self):
        """Sesuaikan wraplength label di kolom kiri form sesuai lebar frame."""
        try:
            col0_width = max(80, int(self.frame_input.winfo_width() * 0.35))
            for w in self.frame_input.winfo_children():
                if isinstance(w, tk.Label):
                    info = w.grid_info()
                    if info and int(info.get("column", 1)) == 0 and int(info.get("columnspan", 1)) == 1:
                        w.configure(wraplength=col0_width, justify=tk.LEFT, anchor="w")
        except Exception:
            pass

    def _update_login_label_wrap(self):
        """Sesuaikan wraplabel login (kolom label kiri) sesuai lebar frame login."""
        try:
            target = getattr(self, "frame_login_card", self.frame_login)
            col0_width = max(80, int(target.winfo_width() * 0.35))
            for w in target.winfo_children():
                if isinstance(w, tk.Label):
                    info = w.grid_info()
                    if info and int(info.get("column", 1)) == 0 and int(info.get("columnspan", 1)) == 1:
                        w.configure(wraplength=col0_width, justify=tk.LEFT, anchor="w")
        except Exception:
            pass
    def _toggle_password_visibility(self):
        self._password_visible = not self._password_visible
        if self._password_visible:
            self.entry_password.config(show="")
            self.btn_toggle_pwd.config(text="Hide")
        else:
            self.entry_password.config(show="*")
            self.btn_toggle_pwd.config(text="Show")

    def _load_prefs(self):
        try:
            if os.path.exists(self._prefs_path):
                with open(self._prefs_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        return data
        except Exception:
            pass
        return {}

    def _save_prefs(self):
        try:
            with open(self._prefs_path, "w", encoding="utf-8") as f:
                json.dump(self.prefs, f, ensure_ascii=False, indent=2)
        except Exception:
            pass


if __name__ == "__main__":
    app = AplikasiBiodata()
    app.mainloop()