import tkinter as tk
from tkinter import colorchooser, messagebox, filedialog

class PaintApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Paint App - Event Handling Demo")
        self.window.geometry("800x600")

        # Variabel untuk painting
        self.last_x = None
        self.last_y = None
        self.pen_color = "black"
        self.pen_size = 2
        self.is_drawing = False

        self.buat_interface()
        self.bind_events()

    def buat_interface(self):
        # Frame untuk toolbar (kiri dan kanan)
        toolbar = tk.Frame(self.window, bg="lightgray", height=50)
        toolbar.pack(fill=tk.X, side=tk.TOP)
        toolbar.pack_propagate(False)

        left_tools = tk.Frame(toolbar, bg="lightgray")
        left_tools.pack(side=tk.LEFT, padx=5)
        right_tools = tk.Frame(toolbar, bg="lightgray")
        right_tools.pack(side=tk.RIGHT, padx=5)

        # Tombol pilih warna
        btn_color = tk.Button(
            left_tools,
            text="🎨 Warna",
            command=self.pilih_warna,
            bg="lightblue"
        )
        btn_color.pack(side=tk.LEFT, padx=4, pady=5)

        # Preview warna & ukuran pen (kotak kecil)
        self.preview_canvas = tk.Canvas(left_tools, width=44, height=24, bg="white", highlightthickness=1)
        self.preview_canvas.pack(side=tk.LEFT, padx=4, pady=5)
        # gambar preview awal
        self._update_preview()

        # Label dan slider untuk ukuran pen
        tk.Label(left_tools, text="Ukuran:", bg="lightgray").pack(side=tk.LEFT, padx=6)
        self.size_var = tk.IntVar(value=self.pen_size)
        size_scale = tk.Scale(
            left_tools,
            from_=1,
            to=20,
            orient=tk.HORIZONTAL,
            variable=self.size_var,
            command=self.ubah_ukuran,
            length=120
        )
        size_scale.pack(side=tk.LEFT, padx=4)

        # Tombol clear
        btn_clear = tk.Button(
            left_tools,
            text="Clear",
            command=self.clear_canvas,
            bg="red",
            fg="white"
        )
        btn_clear.pack(side=tk.LEFT, padx=6)

        # Tombol save (PostScript)
        btn_save = tk.Button(
            left_tools,
            text="Save",
            command=self.save_image,
            bg="green",
            fg="white"
        )
        btn_save.pack(side=tk.LEFT, padx=4)

        # Info di kanan: warna & ukuran (tetap)
        self.info_label = tk.Label(
            right_tools,
            text=f"Warna: {self.pen_color} | Ukuran: {self.pen_size}",
            bg="lightgray"
        )
        self.info_label.pack(side=tk.RIGHT, padx=10, pady=5)

        # Canvas menggambar
        self.canvas = tk.Canvas(
            self.window,
            bg="white",
            cursor="crosshair"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Status bar di bawah (untuk posisi mouse, hint)
        self.statusbar = tk.Label(self.window, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

    def _update_preview(self):
        """Gambar preview pen di preview_canvas"""
        if not hasattr(self, "preview_canvas"):
            return
        self.preview_canvas.delete("all")
        w = int(self.preview_canvas.winfo_reqwidth())
        h = int(self.preview_canvas.winfo_reqheight())
        # kotak warna
        self.preview_canvas.create_rectangle(2, 2, 20, h-2, fill=self.pen_color, outline="black")
        # lingkaran ukuran pen (skalakan agar muat)
        cx = 32
        cy = h // 2
        r = max(1, min(8, self.pen_size))
        self.preview_canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=self.pen_color, outline="black")

    def pilih_warna(self):
        """Event handler untuk memilih warna"""
        color = colorchooser.askcolor(title="Pilih Warna Pen")
        if color[1]:  # Jika user tidak cancel
            self.pen_color = color[1]
            self.update_info()
            self._update_preview()

    def ubah_ukuran(self, value):
        """Event handler untuk mengubah ukuran pen"""
        try:
            self.pen_size = int(value)
        except Exception:
            self.pen_size = 2
        self.update_info()
        self._update_preview()

    def clear_canvas(self):
        """Event handler untuk membersihkan canvas"""
        if messagebox.askyesno("Konfirmasi", "Hapus semua gambar?"):
            self.canvas.delete("all")

    def update_info(self):
        """Method untuk update info di toolbar"""
        self.info_label.config(
            text=f"Warna: {self.pen_color} | Ukuran: {self.pen_size}"
        )

    def bind_events(self):
        """Method untuk binding semua events"""
        # Mouse events untuk menggambar
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)

        # Mouse events untuk info posisi
        self.canvas.bind("<Motion>", self.show_position)

        # Keyboard events
        self.window.bind("<Control-s>", self.save_image)
        self.window.bind("<Control-o>", self.open_image)
        self.window.bind("<Control-n>", self.new_canvas)

        # Window events
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_draw(self, event):
        """Event handler saat mulai menggambar (mouse press)"""
        self.last_x = event.x
        self.last_y = event.y
        self.is_drawing = True

    def draw(self, event):
        """Event handler saat menggambar (mouse drag)"""
        if self.is_drawing and self.last_x is not None and self.last_y is not None:
            # Gambar garis dari posisi terakhir ke posisi sekarang
            self.canvas.create_line(
                self.last_x, self.last_y,
                event.x, event.y,
                width=self.pen_size,
                fill=self.pen_color,
                capstyle=tk.ROUND,
                smooth=tk.TRUE
            )
            self.last_x = event.x
            self.last_y = event.y

    def stop_draw(self, event):
        """Event handler saat berhenti menggambar (mouse release)"""
        self.is_drawing = False
        self.last_x = None
        self.last_y = None

    def show_position(self, event):
        """Event handler untuk menampilkan posisi mouse di statusbar"""
        self.statusbar.config(text=f"Posisi: ({event.x}, {event.y})  |  Warna: {self.pen_color}  Ukuran: {self.pen_size}")
        
        """Event handler untuk menampilkan posisi mouse"""
        if hasattr(self, 'pos_label'):
            self.pos_label.destroy()

        self.pos_label = tk.Label(
            self.window,
            text=f"Posisi: ({event.x}, {event.y})",
            bg="yellow"
        )
        self.pos_label.place(x=event.x + 10, y=event.y + 10)

        # Hapus label setelah 1 detik
        self.window.after(1000, lambda: self.pos_label.destroy() if hasattr(self, 'pos_label') else None)

    def save_image(self, event=None):
        """Event handler untuk save (Ctrl+S) — tanpa Pillow: simpan PostScript (.ps)"""
        # Default extension adalah .ps karena kita tidak mengonversi ke PNG di sini
        filename = filedialog.asksaveasfilename(
            defaultextension=".ps",
            filetypes=[("PostScript files", "*.ps"), ("All files", "*.*")]
        )
        if filename:
            try:
                # Simpan canvas sebagai PostScript
                self.canvas.postscript(file=filename)
                messagebox.showinfo("Info", f"Gambar disimpan sebagai {filename}\n(Format: PostScript)")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menyimpan file: {e}")

    def open_image(self, event=None):
        """Event handler untuk open (Ctrl+O) — placeholder"""
        messagebox.showinfo("Info", "Fitur buka gambar belum diimplementasi (memerlukan Pillow atau konversi).")

    def new_canvas(self, event=None):
        """Event handler untuk canvas baru (Ctrl+N)"""
        if messagebox.askyesno("Canvas Baru", "Buat canvas baru? Gambar saat ini akan hilang."):
            self.canvas.delete("all")

    def on_closing(self):
        """Event handler saat jendela akan ditutup"""
        if messagebox.askokcancel("Keluar", "Yakin ingin keluar? Gambar yang belum disimpan akan hilang."):
            self.window.destroy()

    def jalankan(self):
        """Method untuk menjalankan aplikasi"""
        self.window.mainloop()

# Untuk menjalankan aplikasi
if __name__ == "__main__":
    app = PaintApp()
    app.jalankan()
