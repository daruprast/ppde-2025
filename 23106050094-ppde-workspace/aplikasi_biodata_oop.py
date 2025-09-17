# Nama : Syafiq Rustiawanto
# NIM : 23106050094
# Matkul : Pemrograman Platform Desktop dan Embedded
# Materi : OOP GUI

import tkinter as tk
from tkinter import messagebox
import datetime
import logging

# Setup logging
logging.basicConfig(
	filename='aplikasi_biodata.log',
	level=logging.INFO,
	format='%(asctime)s - %(levelname)s - %(message)s',
	datefmt='%Y-%m-%d %H:%M:%S'
)


class AplikasiBiodata(tk.Tk):
	"""Aplikasi Biodata Mahasiswa dengan OOP, Login, Validasi, Simpan, dan Logging."""

	def __init__(self):
		super().__init__()

		# Konfigurasi window utama
		self.title("Aplikasi Biodata Mahasiswa")
		self.geometry("600x700")
		self.resizable(True, True)
		self.configure(bg="lightblue")

		# Database user sederhana
		self.users_db = {
			"admin": "123",
			"user1": "password1",
			"mahasiswa": "123456",
			# User khusus sesuai instruksi: nama(NIM)
			"syafiq(23106050094)": "23106050094",
		}

		# Status login dan manajemen frame
		self.current_user = None
		self.frame_aktif = None

		# Buat tampilan
		self._buat_tampilan_login()
		self._buat_tampilan_biodata()

		# Tampilkan login di awal
		self._pindah_ke(self.frame_login)

		# Log aplikasi start
		logging.info("Aplikasi dimulai")

	# --- Pembuatan Tampilan ---
	def _buat_tampilan_biodata(self):
		# --- Variabel Kontrol Tkinter ---
		self.var_nama = tk.StringVar()
		self.var_nim = tk.StringVar()
		self.var_jurusan = tk.StringVar()
		self.var_jk = tk.StringVar(value="Pria")
		self.var_setuju = tk.IntVar()

		# Validasi real-time
		self.var_nama.trace_add("write", self.validate_form)
		self.var_nim.trace_add("write", self.validate_form)
		self.var_jurusan.trace_add("write", self.validate_form)

		# --- Frame Biodata ---
		self.frame_biodata = tk.Frame(master=self, padx=20, pady=20, bg=self["bg"])
		self.frame_biodata.columnconfigure(0, weight=1)
		self.frame_biodata.columnconfigure(1, weight=1)

		# Judul
		self.label_judul = tk.Label(
			master=self.frame_biodata,
			text="FORM BIODATA MAHASISWA",
			font=("Arial", 18, "bold"),
			bg=self["bg"],
		)
		self.label_judul.grid(row=0, column=0, columnspan=2, pady=(10, 20))

		# Frame input dengan border
		self.frame_input = tk.Frame(
			master=self.frame_biodata, relief=tk.GROOVE, borderwidth=2, padx=12, pady=12
		)
		self.frame_input.grid(row=1, column=0, columnspan=2, sticky="NSEW")
		self.frame_input.columnconfigure(1, weight=1)
		self.frame_biodata.rowconfigure(1, weight=1)

		# Input Nama
		self.label_nama = tk.Label(self.frame_input, text="Nama Lengkap:", font=("Arial", 12))
		self.label_nama.grid(row=0, column=0, sticky="W", pady=4)
		self.entry_nama = tk.Entry(self.frame_input, width=35, font=("Arial", 12), textvariable=self.var_nama)
		self.entry_nama.grid(row=0, column=1, pady=4, sticky="EW")

		# Input NIM
		self.label_nim = tk.Label(self.frame_input, text="NIM:", font=("Arial", 12))
		self.label_nim.grid(row=1, column=0, sticky="W", pady=4)
		self.entry_nim = tk.Entry(self.frame_input, width=35, font=("Arial", 12), textvariable=self.var_nim)
		self.entry_nim.grid(row=1, column=1, pady=4, sticky="EW")

		# Input Jurusan
		self.label_jurusan = tk.Label(self.frame_input, text="Jurusan:", font=("Arial", 12))
		self.label_jurusan.grid(row=2, column=0, sticky="W", pady=4)
		self.entry_jurusan = tk.Entry(self.frame_input, width=35, font=("Arial", 12), textvariable=self.var_jurusan)
		self.entry_jurusan.grid(row=2, column=1, pady=4, sticky="EW")

		# Input alamat (Text + Scrollbar)
		self.label_alamat = tk.Label(self.frame_input, text="Alamat:", font=("Arial", 12))
		self.label_alamat.grid(row=3, column=0, sticky="NW", pady=4)
		self.frame_alamat = tk.Frame(self.frame_input, relief=tk.SUNKEN, borderwidth=1)
		self.frame_alamat.grid(row=3, column=1, pady=4, sticky="NSEW")
		self.frame_input.rowconfigure(3, weight=1)

		self.scrollbar_alamat = tk.Scrollbar(master=self.frame_alamat)
		self.scrollbar_alamat.pack(side=tk.RIGHT, fill=tk.Y)
		self.text_alamat = tk.Text(master=self.frame_alamat, height=5, width=32, font=("Arial", 12))
		self.text_alamat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		self.scrollbar_alamat.config(command=self.text_alamat.yview)
		self.text_alamat.config(yscrollcommand=self.scrollbar_alamat.set)

		# Jenis Kelamin
		self.label_jk = tk.Label(self.frame_input, text="Jenis Kelamin:", font=("Arial", 12))
		self.label_jk.grid(row=4, column=0, sticky="W", pady=4)
		self.frame_jk = tk.Frame(self.frame_input)
		self.frame_jk.grid(row=4, column=1, sticky="W")
		self.radio_pria = tk.Radiobutton(self.frame_jk, text="Pria", variable=self.var_jk, value="Pria")
		self.radio_pria.pack(side=tk.LEFT, padx=(0, 10))
		self.radio_wanita = tk.Radiobutton(self.frame_jk, text="Wanita", variable=self.var_jk, value="Wanita")
		self.radio_wanita.pack(side=tk.LEFT)

		# Checkbox persetujuan
		self.check_setuju = tk.Checkbutton(
			master=self.frame_input,
			text="Saya menyetujui pengumpulan data ini.",
			variable=self.var_setuju,
			font=("Arial", 10),
			command=self.validate_form,
		)
		self.check_setuju.grid(row=5, column=0, columnspan=2, pady=10, sticky="W")

		# Tombol submit
		self.btn_submit = tk.Button(
			master=self.frame_biodata,
			text="Submit Biodata",
			font=("Arial", 12, "bold"),
			command=self.submit_data,
			state=tk.DISABLED,
		)
		self.btn_submit.grid(row=6, column=0, columnspan=2, pady=20, sticky="EW")

		# Event bindings
		self.btn_submit.bind("<Enter>", self.on_enter)
		self.btn_submit.bind("<Leave>", self.on_leave)
		self.entry_nama.bind("<Return>", self.submit_shortcut)
		self.entry_nim.bind("<Return>", self.submit_shortcut)
		self.entry_jurusan.bind("<Return>", self.submit_shortcut)
		self.text_alamat.bind("<Return>", self.submit_shortcut)

		# Label hasil
		self.label_hasil = tk.Label(
			master=self.frame_biodata,
			text="",
			font=("Arial", 12, "italic"),
			justify=tk.LEFT,
			bg=self["bg"],
		)
		self.label_hasil.grid(row=7, column=0, columnspan=2, sticky="W", padx=5)

		# Buat menu (akan terlihat saat tampilan biodata aktif)
		self._buat_menu()

	def _buat_tampilan_login(self):
		self.frame_login = tk.Frame(master=self, padx=20, pady=100, bg=self["bg"]) 
		self.frame_login.grid_columnconfigure(0, weight=1)
		self.frame_login.grid_columnconfigure(1, weight=1)

		# Judul Login
		tk.Label(
			self.frame_login, text="HALAMAN LOGIN", font=("Arial", 16, "bold"), bg=self["bg"]
		).grid(row=0, column=0, columnspan=2, pady=20)

		# Input Username
		tk.Label(self.frame_login, text="Username:", font=("Arial", 12), bg=self["bg"]).grid(
			row=1, column=0, sticky="W", pady=5
		)
		self.entry_username = tk.Entry(self.frame_login, font=("Arial", 12))
		self.entry_username.grid(row=1, column=1, pady=5, sticky="EW")

		# Input Password
		tk.Label(self.frame_login, text="Password:", font=("Arial", 12), bg=self["bg"]).grid(
			row=2, column=0, sticky="W", pady=5
		)
		self.entry_password = tk.Entry(self.frame_login, font=("Arial", 12), show="*")
		self.entry_password.grid(row=2, column=1, pady=5, sticky="EW")

		# Tombol Login
		self.btn_login = tk.Button(
			self.frame_login, text="Login", font=("Arial", 12, "bold"), command=self._coba_login
		)
		self.btn_login.grid(row=3, column=0, columnspan=2, pady=20, sticky="EW")

		# Keyboard shortcuts untuk login
		self.entry_username.bind("<Return>", lambda e: self.entry_password.focus_set())
		self.entry_password.bind("<Return>", lambda e: self._coba_login())

		# Info user
		info_label = tk.Label(
			self.frame_login,
			text=(
				"Info: Username yang tersedia:\n"
				"admin (password: 123)\n"
				"user1 (password: password1)\n"
				"mahasiswa (password: 123456)\n"
				"syafiq(23106050094) (password: 23106050094)"
			),
			font=("Arial", 9),
			fg="gray",
			justify=tk.LEFT,
			bg=self["bg"],
		)
		info_label.grid(row=4, column=0, columnspan=2, pady=10)

	# --- Navigasi antar tampilan ---
	def _pindah_ke(self, frame_tujuan):
		if self.frame_aktif is not None:
			self.frame_aktif.pack_forget()
		self.frame_aktif = frame_tujuan
		self.frame_aktif.pack(fill=tk.BOTH, expand=True)

		# Kelola menu dan fokus otomatis
		if frame_tujuan == self.frame_login:
			self._hapus_menu()
			self.after(100, lambda: self.entry_username.focus_set())
		elif frame_tujuan == self.frame_biodata:
			# pastikan menu tampil
			self._buat_menu()
			self.after(100, lambda: self.entry_nama.focus_set())

	# --- Menu bar ---
	def _buat_menu(self):
		menu_bar = tk.Menu(master=self)
		self.config(menu=menu_bar)

		file_menu = tk.Menu(master=menu_bar, tearoff=0)
		file_menu.add_command(label="Simpan Hasil", command=self.simpan_hasil)
		file_menu.add_separator()
		file_menu.add_command(label="Logout", command=self._logout)
		file_menu.add_separator()
		file_menu.add_command(label="Keluar", command=self.keluar_aplikasi)

		menu_bar.add_cascade(label="File", menu=file_menu)

	def _hapus_menu(self):
		"""Menghapus menu bar dari window."""
		empty_menu = tk.Menu(self)
		self.config(menu=empty_menu)

	# --- Method Callback dan Logika ---
	def validate_form(self, *args):
		nama_valid = self.var_nama.get().strip() != ""
		nim_valid = self.var_nim.get().strip() != ""
		jurusan_valid = self.var_jurusan.get().strip() != ""
		setuju_valid = self.var_setuju.get() == 1
		if nama_valid and nim_valid and jurusan_valid and setuju_valid:
			self.btn_submit.config(state=tk.NORMAL)
		else:
			self.btn_submit.config(state=tk.DISABLED)

	def submit_data(self):
		"""Submit data biodata dengan validasi lengkap dan logging."""
		try:
			# Cek checkbox
			if self.var_setuju.get() == 0:
				messagebox.showwarning("Peringatan", "Anda harus menyetujui pengumpulan data!")
				return

			# Ambil data dari form
			nama = self.entry_nama.get().strip()
			nim = self.entry_nim.get().strip()
			jurusan = self.entry_jurusan.get().strip()
			alamat = self.text_alamat.get("1.0", tk.END).strip()
			jenis_kelamin = self.var_jk.get()

			# Validasi dasar
			if not nama or not nim or not jurusan:
				messagebox.showwarning("Input Kosong", "Nama, NIM, dan Jurusan harus diisi!")
				return

			# Validasi format NIM (angka dan minimal 8 digit)
			if not nim.isdigit() or len(nim) < 8:
				messagebox.showwarning("Format NIM Salah", "NIM harus berupa angka minimal 8 digit!")
				self.entry_nim.focus_set()
				return

			# Validasi nama (tidak boleh hanya angka)
			if nama.isdigit():
				messagebox.showwarning("Format Nama Salah", "Nama tidak boleh hanya berupa angka!")
				self.entry_nama.focus_set()
				return

			# Tampilkan hasil
			hasil = (
				f"Nama: {nama}\n"
				f"NIM: {nim}\n"
				f"Jurusan: {jurusan}\n"
				f"Alamat: {alamat}\n"
				f"Jenis Kelamin: {jenis_kelamin}"
			)
			messagebox.showinfo("Data Tersimpan", hasil)

			# Tampilkan di label dengan info user
			hasil_lengkap = f"BIODATA TERSIMPAN:\nDiinput oleh: {self.current_user}\n\n{hasil}"
			self.label_hasil.config(text=hasil_lengkap)

			# Logging sukses
			logging.info(f"Data submitted by user: {self.current_user} - NIM: {nim}")

		except Exception as e:
			logging.error(f"Error in submit_data by {self.current_user}: {str(e)}")
			messagebox.showerror("Error", f"Terjadi kesalahan saat memproses data:\n{str(e)}")

	def simpan_hasil(self):
		"""Simpan hasil biodata ke file dengan error handling."""
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
				file.write(
					f"Waktu penyimpanan: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
				)
				file.write("-" * 50 + "\n")
				file.write(hasil_tersimpan)

			messagebox.showinfo("Info", f"Data berhasil disimpan ke file '{filename}'.")
			logging.info(f"File saved by {self.current_user}: {filename}")

		except PermissionError:
			messagebox.showerror("Error", "Tidak memiliki izin untuk menyimpan file di lokasi ini.")
		except Exception as e:
			messagebox.showerror("Error", f"Terjadi kesalahan saat menyimpan file:\n{str(e)}")

	def on_enter(self, event):
		if self.btn_submit['state'] == tk.NORMAL:
			self.btn_submit.config(bg="lightblue")

	def on_leave(self, event):
		self.btn_submit.config(bg="SystemButtonFace")

	def submit_shortcut(self, event=None):
		if self.btn_submit['state'] == tk.NORMAL:
			self.submit_data()

	def _coba_login(self):
		"""Method untuk memproses attempt login dengan logging."""
		username = self.entry_username.get().strip()
		password = self.entry_password.get()

		# Log attempt
		logging.info(f"Login attempt for username: {username}")

		# Validasi input kosong
		if not username or not password:
			logging.warning(f"Empty credentials attempt for username: {username}")
			messagebox.showwarning("Login Gagal", "Username dan Password tidak boleh kosong.")
			self.entry_username.focus_set()
			return

		# Validasi panjang minimum username
		if len(username) < 3:
			logging.warning(f"Username too short: {username}")
			messagebox.showwarning("Login Gagal", "Username minimal 3 karakter.")
			self.entry_username.focus_set()
			return

		# Cek kredensial
		if username in self.users_db and self.users_db[username] == password:
			self.current_user = username
			logging.info(f"Successful login for user: {username}")
			messagebox.showinfo("Login Berhasil", f"Selamat Datang, {username}!")
			self._reset_form_biodata()
			self._update_title_with_user()
			self._pindah_ke(self.frame_biodata)
			# Bersihkan field login
			self.entry_username.delete(0, tk.END)
			self.entry_password.delete(0, tk.END)
		else:
			logging.warning(f"Failed login attempt for username: {username}")
			messagebox.showerror("Login Gagal", "Username atau Password salah.")
			self.entry_password.delete(0, tk.END)
			self.entry_username.focus_set()

	def _reset_form_biodata(self):
		"""Reset semua field di form biodata."""
		self.var_nama.set("")
		self.var_nim.set("")
		self.var_jurusan.set("")
		self.text_alamat.delete("1.0", tk.END)
		self.var_jk.set("Pria")
		self.var_setuju.set(0)
		self.label_hasil.config(text="")

	def _update_title_with_user(self):
		"""Update judul window dengan nama user yang login."""
		if self.current_user:
			self.title(f"Aplikasi Biodata Mahasiswa - User: {self.current_user}")
		else:
			self.title("Aplikasi Biodata Mahasiswa")

	def _logout(self):
		"""Method untuk logout dengan logging"""
		if messagebox.askyesno("Logout", f"Apakah {self.current_user} yakin ingin logout?"):
			logging.info(f"User logout: {self.current_user}")
			# Reset status user
			self.current_user = None
			# Hapus menu
			self._hapus_menu()
			# Update title
			self._update_title_with_user()
			# Bersihkan field login
			self.entry_username.delete(0, tk.END)
			self.entry_password.delete(0, tk.END)
			# Reset form biodata
			self._reset_form_biodata()
			# Kembali ke halaman login
			self._pindah_ke(self.frame_login)
			# Fokus ke username
			self.entry_username.focus_set()

	def keluar_aplikasi(self):
		"""Keluar dari aplikasi dengan konfirmasi dan logging."""
		if messagebox.askokcancel("Keluar", "Apakah Anda yakin ingin keluar dari aplikasi?"):
			logging.info(f"Application closed by user: {self.current_user}")
			self.destroy()


if __name__ == "__main__":
	app = AplikasiBiodata()
	app.mainloop()

