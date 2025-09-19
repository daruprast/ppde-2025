import tkinter as tk
from tkinter import messagebox
import datetime
import logging
import csv
import os
import re

# File untuk menyimpan username terakhir
USER_FILE = "last_user.txt"

# Setup logging
logging.basicConfig(
    filename='aplikasi_biodata.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Membuat kelas utama aplikasi yang mewarisi dari tk.Tk
class AplikasiBiodata(tk.Tk):
    # Metode __init__ adalah constructor yang akan dijalankan saat objek dibuat
    def __init__(self):
        # Memanggil constructor dari kelas induk (tk.Tk)
        super().__init__()

        # Mengkonfigurasi window utama
        self.title("Aplikasi Biodata Mahasiswa")
        self.geometry("600x700")
        self.resizable(True, True)
        self.configure(bg="floralwhite")

        # Database user sederhana (dalam aplikasi nyata, ini akan di database)
        self.users_db = {
            "admin": "admin123",
            "arbath": "23106050012",
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

        # Log aplikasi start
        logging.info("Aplikasi dimulai")
        self.bind("<Escape>", lambda e: self._buat_menu())

    # Fungsi untuk validasi form secara real-time
    def submit_data(self):
        """Submit data biodata dengan validasi lengkap"""
        try:
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
            email = self.entry_email.get()
            telp = self.entry_telp.get()
            birth = self.entry_birth.get()

            # Cek field kosong
            if not nama or not nim or not jurusan:
                messagebox.showwarning("Input Kosong", "Semua field harus diisi!")
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
            
            # Validasi format email
            if not self.validate_email(email):
                messagebox.showwarning("Error", "Format email tidak valid!")
                self.entry_email.focus_set()
                return

            # Validasi format telepon
            if not self.validate_telp(telp):
                messagebox.showwarning("Error", "Format telepon tidak valid! Gunakan format Indonesia (misal: 08123456789 atau +628123456789).")
                self.entry_telp.focus_set()
                return

            # Validasi format tanggal lahir
            if not self.validate_birth(birth):
                messagebox.showwarning("Error", "Format tanggal lahir tidak valid! Gunakan format DD/MM/YYYY.")
                self.entry_birth.focus_set()
                return
        
            # Tampilkan hasil
            hasil = f"Nama: {nama}\nNIM: {nim}\nJurusan: {jurusan}\nAlamat: {alamat}\nJenis Kelamin: {jenis_kelamin}\nEmail: {email}\nTelepon: {telp}\nTanggal Lahir: {birth}"
            
            # Simpan ke CSV
            with open("biodata_tersimpan.csv", "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                if file.tell() == 0:
                    writer.writerow(["Nama", "NIM", "Jurusan", "Alamat", "Jenis Kelamin", "Email", "Telepon", "Tanggal Lahir"])
                writer.writerow([nama, nim, jurusan, alamat, jenis_kelamin, email, telp, birth])
            
            messagebox.showinfo("Data Tersimpan", hasil)
            messagebox.showinfo("arbath@teknohole.com", "Data berhasil disimpan ke file 'biodata_tersimpan.csv'.")

            # Tampilkan hasil di label
            hasil_lengkap = f"BIODATA TERSIMPAN:\nDiinput oleh: {self.current_user}\n\n{hasil}"
            self.label_hasil.config(text=hasil_lengkap)

            # Log successful data submission
            logging.info(f"Data submitted by user: {self.current_user} - NIM: {nim}")

        except Exception as e:
            logging.error(f"Error in submit_data by {self.current_user}: {str(e)}")
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

    def validate_email(self, email):
        """Validasi format email"""
        return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

    def validate_telp(self, telp):
        """Validasi format telepon Indonesia"""
        return re.match(r"^(?:\+62|62|0)8\d{8,11}$", telp)

    def validate_birth(self, birth):
        """Validasi format tanggal lahir DD/MM/YYYY"""
        try:
            datetime.datetime.strptime(birth, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    def validate_form(self, *args):
        """Validasi form secara real-time"""
        nama_valid = self.var_nama.get().strip() != ""
        nim_valid = self.var_nim.get().strip() != ""
        jurusan_valid = self.var_jurusan.get().strip() != ""
        setuju_valid = self.var_setuju.get() == 1
        email_valid = self.var_email.get().strip() != ""
        telp_valid = self.var_telp.get().strip() != ""
        birth_valid = self.var_birth.get().strip() != ""

        if nama_valid and nim_valid and jurusan_valid and setuju_valid and email_valid and telp_valid and birth_valid:
            self.btn_submit.config(state=tk.NORMAL)
        else:
            self.btn_submit.config(state=tk.DISABLED)

    def on_enter(self, event):
        """Event handler untuk mouse enter pada tombol"""
        if self.btn_submit['state'] == tk.NORMAL:
            self.btn_submit.config(bg="yellow")

    def on_leave(self, event):
        """Event handler untuk mouse leave pada tombol"""
        self.btn_submit.config(bg="floralwhite")

    def submit_shortcut(self, event=None):
        """Shortcut keyboard untuk submit"""
        if self.btn_submit['state'] == tk.NORMAL:
            self.btn_submit.config(bg="yellow")
            self.submit_data()

    # Method navigasi antar frame
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

    def _buat_menu(self):
        """Membuat menu bar untuk aplikasi"""
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)

        home_menu = tk.Menu(master=menu_bar, tearoff=0)
        home_menu.add_command(label="Logout", command=self._logout)
        home_menu.add_separator()
        home_menu.add_command(label="Keluar", command=self._keluar_aplikasi)

        file_menu = tk.Menu(master=menu_bar, tearoff=0)
        file_menu.add_command(label="Simpan", command=self.simpan_hasil)
        file_menu.add_separator()
        file_menu.add_command(label="Simpan Sebagai", command=self.simpan_hasil)

        edit_menu = tk.Menu(master=menu_bar, tearoff=0)
        edit_menu.add_command(label="Reset Form", command=self._reset_form_biodata)
        edit_menu.add_separator()
        edit_menu.add_command(label="Hapus Menu", command=self._hapus_menu)
        edit_menu.add_separator()
        edit_menu.add_command(label="Tampilkan Menu <Esc>", command=self._buat_menu)
        
        menu_bar.add_cascade(label="Home", menu=home_menu)
        menu_bar.add_cascade(label="File", menu=file_menu)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

    def _hapus_menu(self):
        """Menghapus menu bar dari window"""
        empty_menu = tk.Menu(self)
        self.config(menu=empty_menu)

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
            logging.info(f"Data saved to file: {filename} by user: {self.current_user}")

        except PermissionError:
            messagebox.showerror("Error", "Tidak memiliki izin untuk menyimpan file di lokasi ini.")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat menyimpan file:\n{str(e)}")

    def _keluar_aplikasi(self):
        """Keluar dari aplikasi dengan konfirmasi"""
        if messagebox.askokcancel("Keluar", "Apakah Anda yakin ingin keluar dari aplikasi?"):
            logging.info(f"Application closed by user: {self.current_user}")
            self.destroy()

    def _coba_login(self):
        """Method untuk memproses attempt login"""
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
            messagebox.showinfo("Login Berhasil", f"Selamat Datang, {username}!")
            self._reset_form_biodata()
            self._update_title_with_user()
            self._pindah_ke(self.frame_biodata)
            # Bersihkan field login setelah berhasil
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
        else:
            logging.warning(f"Failed login attempt for username: {username}")
            messagebox.showerror("Login Gagal", "Username atau Password salah.")
            # Bersihkan password dan focus ke username
            self.entry_password.delete(0, tk.END)
            self.entry_username.focus_set()

        # Simpan username & password terakhir jika checkbox di-check
        if self.remember_var.get():
            with open(USER_FILE, "w") as f:
                f.write(f"{username}\n{password}")
        else:
            if os.path.exists(USER_FILE):
                os.remove(USER_FILE)

    def _reset_form_biodata(self):
        """Reset semua field di form biodata"""
        self.var_nama.set("")
        self.var_nim.set("")
        self.var_jurusan.set("")
        self.text_alamat.delete("1.0", tk.END)
        self.var_jk.set("Laki-Laki")
        self.var_email.set("")
        self.var_telp.set("")
        self.var_birth.set("")
        self.var_setuju.set(0)
        self.label_hasil.config(text="")

    def _update_title_with_user(self):
        """Update judul window dengan nama user yang login"""
        if self.current_user:
            self.title(f"Aplikasi Biodata Mahasiswa - User: {self.current_user}")
        else:
            self.title("Aplikasi Biodata Mahasiswa")
            
    # Method untuk toggle show/hide password
    def toggle_password(self):
        """Tampilkan atau sembunyikan password"""
        if self.show_password:
            self.entry_password.config(show="*")
            self.toggle_btn.config(text="Show")
        else:
            self.entry_password.config(show="")
            self.toggle_btn.config(text="Hide")
        self.show_password = not self.show_password

    def load_username(self):
        """Muat data username & password terakhir"""
        if os.path.exists(USER_FILE):
            try:
                with open(USER_FILE, "r") as f:
                    lines = f.readlines()
                    if len(lines) >= 2:
                        self.entry_username.insert(0, lines[0].strip())
                        self.entry_password.insert(0, lines[1].strip())
                        self.remember_var.set(True)
            except Exception as e:
                logging.error(f"Error loading saved credentials: {str(e)}")

    # Halaman login
    def _buat_tampilan_login(self):
        """Membuat tampilan halaman login"""
        self.frame_login = tk.Frame(master=self, padx=20, pady=100)
        self.frame_login.configure(bg="lightblue")

        # Konfigurasi grid untuk frame login agar terpusat
        self.frame_login.grid_columnconfigure(0, weight=1)
        self.frame_login.grid_columnconfigure(1, weight=1)

        # Judul Login
        tk.Label(
            self.frame_login, 
            text="HALAMAN LOGIN", 
            font=("Arial", 16, "bold"),
            bg="lightblue"
        ).grid(row=0, column=0, columnspan=2, pady=20)

        # Input Username
        tk.Label(
            self.frame_login, 
            text="Username:", 
            font=("Arial", 12),
            bg="lightblue"
        ).grid(row=1, column=0, sticky="W", pady=5)

        self.entry_username = tk.Entry(self.frame_login, font=("Arial", 12))
        self.entry_username.grid(row=1, column=1, pady=5, sticky="EW")

        # Input Password
        tk.Label(
            self.frame_login, 
            text="Password:", 
            font=("Arial", 12),
            bg="lightblue"
        ).grid(row=2, column=0, sticky="W", pady=5)

        self.entry_password = tk.Entry(
            self.frame_login, 
            font=("Arial", 12), 
            show="*"
        )
        self.entry_password.grid(row=2, column=1, pady=5, sticky="EW")

        # Tombol show/hide password
        self.show_password = False
        self.toggle_btn = tk.Button(
            self.frame_login,
            text="Show",
            command=self.toggle_password
        )
        self.toggle_btn.grid(row=2, column=2, padx=5)

        # Checkbox Remember Me
        self.remember_var = tk.BooleanVar()
        tk.Checkbutton(
            self.frame_login,
            text="Remember Me",
            variable=self.remember_var,
            bg="lightblue",
            font=("Arial", 10)
        ).grid(row=3, column=0, columnspan=1, pady=20, sticky="W")

        # Load username terakhir jika ada
        self.load_username()

        # Tombol Login
        self.btn_login = tk.Button(
            self.frame_login, 
            text="Login", 
            font=("Arial", 12, "bold"),
            bg="floralwhite",
            command=self._coba_login
        )
        self.btn_login.grid(row=4, column=0, columnspan=3, pady=5, sticky="EW")

        # Event bindings untuk hover dan keyboard shortcuts
        self.btn_login.bind("<Enter>", lambda e: self.btn_login.config(bg="yellow"))
        self.btn_login.bind("<Leave>", lambda e: self.btn_login.config(bg="floralwhite"))

        # Keyboard shortcuts untuk login
        self.entry_username.bind("<Return>", lambda e: self.entry_password.focus_set())
        self.entry_password.bind("<Return>", lambda e: self._coba_login())

    # Halaman isi form
    def _buat_tampilan_biodata(self):
        """Membuat tampilan halaman biodata"""
        # --- Variabel Kontrol Tkinter ---
        self.var_nama = tk.StringVar()
        self.var_nim = tk.StringVar()
        self.var_jurusan = tk.StringVar()
        self.var_jk = tk.StringVar(value="Laki-Laki")
        self.var_email = tk.StringVar()
        self.var_telp = tk.StringVar()
        self.var_birth = tk.StringVar()
        self.var_setuju = tk.IntVar()

        # Aktifkan trace untuk validasi real-time
        self.var_nama.trace_add("write", self.validate_form)
        self.var_nim.trace_add("write", self.validate_form)
        self.var_jurusan.trace_add("write", self.validate_form)
        self.var_email.trace_add("write", self.validate_form)
        self.var_telp.trace_add("write", self.validate_form)
        self.var_birth.trace_add("write", self.validate_form)

        # --- Frame Biodata ---
        self.frame_biodata = tk.Frame(master=self, padx=20, pady=20)
        self.frame_biodata.columnconfigure(1, weight=1)
        self.frame_biodata.configure(bg="lightblue")

        # Judul
        self.label_judul = tk.Label(
            master=self.frame_biodata, 
            text="FORM BIODATA MAHASISWA", 
            font=("Arial", 16, "bold"),
            bg="lightblue"
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

        # Input Email
        self.label_email = tk.Label(
            master=self.frame_input, 
            text="Email:", 
            font=("Arial", 12)
        )
        self.label_email.grid(row=4, column=0, sticky="W", pady=2)
        self.entry_email = tk.Entry(
            master=self.frame_input, 
            width=30, 
            font=("Arial", 12), 
            textvariable=self.var_email
        )
        self.entry_email.grid(row=4, column=1, pady=2)

        # Input Telepon
        self.label_telp = tk.Label(
            master=self.frame_input, 
            text="Telepon:", 
            font=("Arial", 12)
        )
        self.label_telp.grid(row=5, column=0, sticky="W", pady=2)
        self.entry_telp = tk.Entry(
            master=self.frame_input, 
            width=30, 
            font=("Arial", 12), 
            textvariable=self.var_telp
        )
        self.entry_telp.grid(row=5, column=1, pady=2)

        # Input Tanggal Lahir
        self.label_birth = tk.Label(
            master=self.frame_input, 
            text="Tanggal Lahir (DD/MM/YYYY):", 
            font=("Arial", 12)
        )
        self.label_birth.grid(row=6, column=0, sticky="W", pady=2)
        self.entry_birth = tk.Entry(
            master=self.frame_input, 
            width=30, 
            font=("Arial", 12), 
            textvariable=self.var_birth
        )
        self.entry_birth.grid(row=6, column=1, pady=2)

        # Jenis kelamin
        self.label_jk = tk.Label(
            master=self.frame_input, 
            text="Jenis Kelamin:", 
            font=("Arial", 12)
        )
        self.label_jk.grid(row=7, column=0, sticky="W", pady=2)

        self.frame_jk = tk.Frame(master=self.frame_input)
        self.frame_jk.grid(row=7, column=1, sticky="W")

        self.radio_pria = tk.Radiobutton(
            master=self.frame_jk, 
            text="L", 
            variable=self.var_jk, 
            value="Laki-Laki"
        )
        self.radio_pria.pack(side=tk.LEFT)
        self.radio_wanita = tk.Radiobutton(
            master=self.frame_jk, 
            text="P", 
            variable=self.var_jk, 
            value="Perempuan"
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
        self.check_setuju.grid(row=8, column=0, columnspan=2, pady=10, sticky="W")

        self.frame_input.grid(row=1, column=0, columnspan=2, sticky="EW")

        # Tombol submit
        self.btn_submit = tk.Button(
            master=self.frame_biodata, 
            text="Submit Biodata", 
            font=("Arial", 12, "bold"),
            command=self.submit_data,
            state=tk.DISABLED
        )
        self.btn_submit.grid(row=2, column=0, columnspan=2, pady=20, sticky="EW")

        # Event bindings untuk hover dan keyboard shortcuts
        self.btn_submit.bind("<Enter>", self.on_enter)
        self.btn_submit.bind("<Leave>", self.on_leave)

        # Keyboard shortcuts
        self.entry_nama.bind("<Return>", lambda e: self.entry_nim.focus_set())
        self.entry_nim.bind("<Return>", lambda e: self.entry_jurusan.focus_set())
        self.entry_jurusan.bind("<Return>", lambda e: self.text_alamat.focus_set())
        self.entry_email.bind("<Return>", lambda e: self.entry_telp.focus_set())
        self.entry_telp.bind("<Return>", lambda e: self.entry_birth.focus_set())
        self.entry_birth.bind("<Return>", self.submit_shortcut)
        self.text_alamat.bind("<Return>", lambda e: self.entry_email.focus_set())

        # Label hasil
        self.label_hasil = tk.Label(
            master=self.frame_biodata, 
            text="", 
            font=("Arial", 12, "italic"), 
            justify=tk.LEFT,
            bg="lightblue"
        )
        self.label_hasil.grid(row=3, column=0, columnspan=2, sticky="W", padx=10)

        # Membuat menu
        self._buat_menu()

    def _logout(self):
        """Method untuk logout dan kembali ke halaman login"""
        if messagebox.askyesno("Logout", f"Apakah {self.current_user} yakin ingin logout?"):
            logging.info(f"User logout: {self.current_user}")
            # Reset status user
            self.current_user = None
            # Update title
            self._update_title_with_user()
            # Bersihkan field login
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            # Reset form biodata
            self._reset_form_biodata()
            # Kembali ke halaman login
            self._pindah_ke(self.frame_login)
            # Focus ke username field
            self.entry_username.focus_set()


# Blok berikut hanya akan dieksekusi jika file ini dijalankan secara langsung
if __name__ == "__main__":
    # Membuat instance dari kelas aplikasi kita
    app = AplikasiBiodata()
    # Menjalankan mainloop dari instance tersebut
    app.mainloop()