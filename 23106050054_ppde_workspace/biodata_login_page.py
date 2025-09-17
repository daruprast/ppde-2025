import tkinter as tk
from tkinter import messagebox

# Membuat kelas utama aplikasi yang mewarisi dari tk.Tk
class AplikasiBiodata(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikasi Biodata Mahasiswa")
        self.geometry("600x700")
        self.resizable(True, True)

        # Database user sederhana
        self.users_db = {
            "admin": "123",
            "user1": "password1",
            "mahasiswa": "123456"
        }

        # Status login
        self.current_user = None
        self.frame_aktif = None

        # Buat tampilan
        self._buat_tampilan_login()
        self._buat_tampilan_biodata()

        # Tampilkan frame login di awal
        self._pindah_ke(self.frame_login)

    def _pindah_ke(self, frame_tujuan):
        if self.frame_aktif is not None:
            self.frame_aktif.pack_forget()
        self.frame_aktif = frame_tujuan
        self.frame_aktif.pack(fill=tk.BOTH, expand=True)

        if frame_tujuan == self.frame_login:
            self.after(100, lambda: self.entry_username.focus_set())
        elif frame_tujuan == self.frame_biodata:
            self.after(100, lambda: self.entry_nama.focus_set())

    def _coba_login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get()

        if not username or not password:
            messagebox.showwarning("Login Gagal", "Username dan Password tidak boleh kosong.")
            return

        if len(username) < 3:
            messagebox.showwarning("Login Gagal", "Username minimal 3 karakter.")
            return

        if username in self.users_db and self.users_db[username] == password:
            self.current_user = username
            messagebox.showinfo("Login Berhasil", f"Selamat Datang, {username}!")
            self._reset_form_biodata()
            self._update_title_with_user()
            self._pindah_ke(self.frame_biodata)
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
        else:
            messagebox.showerror("Login Gagal", "Username atau Password salah.")
            self.entry_password.delete(0, tk.END)
            self.entry_username.focus_set()

    def _buat_tampilan_login(self):
        self.frame_login = tk.Frame(master=self, padx=20, pady=100)
        self.frame_login.grid_columnconfigure(0, weight=1)
        self.frame_login.grid_columnconfigure(1, weight=1)

        tk.Label(self.frame_login, text="HALAMAN LOGIN", font=("Arial", 16, "bold")).grid(
            row=0, column=0, columnspan=2, pady=20
        )

        tk.Label(self.frame_login, text="Username:", font=("Arial", 12)).grid(row=1, column=0, sticky="W", pady=5)
        self.entry_username = tk.Entry(self.frame_login, font=("Arial", 12))
        self.entry_username.grid(row=1, column=1, pady=5, sticky="EW")

        tk.Label(self.frame_login, text="Password:", font=("Arial", 12)).grid(row=2, column=0, sticky="W", pady=5)
        self.entry_password = tk.Entry(self.frame_login, font=("Arial", 12), show="*")
        self.entry_password.grid(row=2, column=1, pady=5, sticky="EW")

        self.btn_login = tk.Button(
            self.frame_login, text="Login", font=("Arial", 12, "bold"), command=self._coba_login
        )
        self.btn_login.grid(row=3, column=0, columnspan=2, pady=20, sticky="EW")

        self.entry_username.bind("<Return>", lambda e: self.entry_password.focus_set())
        self.entry_password.bind("<Return>", lambda e: self._coba_login())

        info_label = tk.Label(
            self.frame_login,
            text="Info: Username yang tersedia:\nadmin (123)\nuser1 (password1)\nmahasiswa (123456)",
            font=("Arial", 9), fg="gray", justify=tk.LEFT
        )
        info_label.grid(row=4, column=0, columnspan=2, pady=10)

    def _buat_tampilan_biodata(self):
        self.var_nama = tk.StringVar()
        self.var_nim = tk.StringVar()
        self.var_jurusan = tk.StringVar()
        self.var_jk = tk.StringVar(value="Pria")
        self.var_setuju = tk.IntVar()

        self.frame_biodata = tk.Frame(master=self, padx=20, pady=20, bg="lavender")
        self.frame_biodata.columnconfigure(1, weight=1)

        self.var_nama.trace_add("write", self.validate_form)
        self.var_nim.trace_add("write", self.validate_form)
        self.var_jurusan.trace_add("write", self.validate_form)

        tk.Label(self.frame_biodata, text="FORM BIODATA MAHASISWA", font=("Arial", 16, "bold")).grid(
            row=0, column=0, columnspan=2, pady=20
        )

        self.frame_input = tk.Frame(self.frame_biodata, relief=tk.GROOVE, borderwidth=2, padx=10, pady=10)

        tk.Label(self.frame_input, text="Nama Lengkap:", font=("Arial", 12)).grid(row=0, column=0, sticky="W", pady=2)
        self.entry_nama = tk.Entry(self.frame_input, width=30, font=("Arial", 12), textvariable=self.var_nama)
        self.entry_nama.grid(row=0, column=1, pady=2)

        tk.Label(self.frame_input, text="NIM:", font=("Arial", 12)).grid(row=1, column=0, sticky="W", pady=2)
        self.entry_nim = tk.Entry(self.frame_input, width=30, font=("Arial", 12), textvariable=self.var_nim)
        self.entry_nim.grid(row=1, column=1, pady=2)

        tk.Label(self.frame_input, text="Jurusan:", font=("Arial", 12)).grid(row=2, column=0, sticky="W", pady=2)
        self.entry_jurusan = tk.Entry(self.frame_input, width=30, font=("Arial", 12), textvariable=self.var_jurusan)
        self.entry_jurusan.grid(row=2, column=1, pady=2)

        tk.Label(self.frame_input, text="Alamat:", font=("Arial", 12)).grid(row=3, column=0, sticky="NW", pady=2)
        self.frame_alamat = tk.Frame(self.frame_input, relief=tk.SUNKEN, borderwidth=1)
        self.scrollbar_alamat = tk.Scrollbar(self.frame_alamat)
        self.scrollbar_alamat.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_alamat = tk.Text(self.frame_alamat, height=5, width=28, font=("Arial", 12))
        self.text_alamat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar_alamat.config(command=self.text_alamat.yview)
        self.text_alamat.config(yscrollcommand=self.scrollbar_alamat.set)
        self.frame_alamat.grid(row=3, column=1, pady=2)

        tk.Label(self.frame_input, text="Jenis Kelamin:", font=("Arial", 12)).grid(row=4, column=0, sticky="W", pady=2)
        self.frame_jk = tk.Frame(self.frame_input)
        self.frame_jk.grid(row=4, column=1, sticky="W")
        tk.Radiobutton(self.frame_jk, text="Pria", variable=self.var_jk, value="Pria").pack(side=tk.LEFT)
        tk.Radiobutton(self.frame_jk, text="Wanita", variable=self.var_jk, value="Wanita").pack(side=tk.LEFT)

        self.check_setuju = tk.Checkbutton(
            self.frame_input, text="Saya menyetujui pengumpulan data ini.",
            variable=self.var_setuju, font=("Arial", 10), command=self.validate_form
        )
        self.check_setuju.grid(row=5, column=0, columnspan=2, pady=10, sticky="W")

        self.frame_input.grid(row=1, column=0, columnspan=2, sticky="EW")

        self.btn_submit = tk.Button(
            self.frame_biodata, text="Submit Biodata", font=("Arial", 12, "bold"),
            command=self.submit_data, state=tk.DISABLED
        )
        self.btn_submit.grid(row=6, column=0, columnspan=2, pady=20, sticky="EW")

        self.btn_submit.bind("<Enter>", self.on_enter)
        self.btn_submit.bind("<Leave>", self.on_leave)

        self.entry_nama.bind("<Return>", self.submit_shortcut)
        self.entry_nim.bind("<Return>", self.submit_shortcut)
        self.entry_jurusan.bind("<Return>", self.submit_shortcut)

        self.label_hasil = tk.Label(self.frame_biodata, text="", font=("Arial", 12, "italic"), justify=tk.LEFT)
        self.label_hasil.grid(row=7, column=0, columnspan=2, sticky="W", padx=10)

        self._buat_menu()

    def _buat_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)

        file_menu = tk.Menu(master=menu_bar, tearoff=0)
        file_menu.add_command(label="Simpan Hasil", command=self.simpan_hasil)
        file_menu.add_command(label="Logout", command=self._logout)
        file_menu.add_separator()
        file_menu.add_command(label="Keluar", command=self.keluar_aplikasi)

        menu_bar.add_cascade(label="File", menu=file_menu)

    def _hapus_menu(self):
        empty_menu = tk.Menu(self)
        self.config(menu=empty_menu)

    def _reset_form_biodata(self):
        self.var_nama.set("")
        self.var_nim.set("")
        self.var_jurusan.set("")
        self.text_alamat.delete("1.0", tk.END)
        self.var_jk.set("Pria")
        self.var_setuju.set(0)
        self.label_hasil.config(text="")

    def _update_title_with_user(self):
        if self.current_user:
            self.title(f"Aplikasi Biodata Mahasiswa - User: {self.current_user}")
        else:
            self.title("Aplikasi Biodata Mahasiswa")

    def _logout(self):
        if messagebox.askyesno("Logout", f"Apakah {self.current_user} yakin ingin logout?"):
            self.current_user = None
            self._hapus_menu()
            self._update_title_with_user()
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            self._reset_form_biodata()
            self._pindah_ke(self.frame_login)
            self.entry_username.focus_set()

    def submit_data(self):
        if self.var_setuju.get() == 0:
            messagebox.showwarning("Peringatan", "Anda harus menyetujui pengumpulan data!")
            return

        nama = self.entry_nama.get()
        nim = self.entry_nim.get()
        jurusan = self.entry_jurusan.get()
        alamat = self.text_alamat.get("1.0", tk.END).strip()
        jenis_kelamin = self.var_jk.get()

        if not nama or not nim or not jurusan:
            messagebox.showwarning("Input Kosong", "Semua field harus diisi!")
            return

        hasil = f"Nama: {nama}\nNIM: {nim}\nJurusan: {jurusan}\nAlamat: {alamat}\nJenis Kelamin: {jenis_kelamin}"
        messagebox.showinfo("Data Tersimpan", hasil)
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
            self.btn_submit.config(bg="lavender")

    def on_leave(self, event):
        self.btn_submit.config(bg="SystemButtonFace")

    def submit_shortcut(self, event=None):
        if self.btn_submit['state'] == tk.NORMAL:
            self.submit_data()

    def simpan_hasil(self):
        hasil_tersimpan = self.label_hasil.cget("text")
        if not hasil_tersimpan or "BIODATA TERSIMPAN" not in hasil_tersimpan:
            messagebox.showwarning("Peringatan", "Tidak ada data untuk disimpan. Mohon submit terlebih dahulu.")
            return
        with open("biodata_tersimpan.txt", "w") as file:
            file.write(hasil_tersimpan)
        messagebox.showinfo("Info", "Data berhasil disimpan ke file 'biodata_tersimpan.txt'.")

    def keluar_aplikasi(self):
        if messagebox.askokcancel("Keluar", "Apakah Anda yakin ingin keluar dari aplikasi?"):
            self.destroy()


if __name__ == "__main__":
    app = AplikasiBiodata()
    app.mainloop()
