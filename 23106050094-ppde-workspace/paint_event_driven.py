"""
Aplikasi Paint Sederhana (Event-Driven, Tkinter)

Fitur:
- Menggambar garis bebas dengan mouse (drag)
- Pilih warna (color chooser)
- Atur ukuran kuas (1-30)
- Tombol Clear (hapus kanvas)
- Simpan ke file PostScript (.ps) via menu File > Save As...
- Shortcuts: Ctrl+N (Clear), Ctrl+S (Save), Ctrl+Q (Quit)

Catatan: Format .ps dapat dikonversi ke PNG/JPG menggunakan alat eksternal (mis. Ghostscript) jika diperlukan.
"""

import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox


class PaintApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Paint Event-Driven")
        self.geometry("800x600")

        self.current_color = "#000000"
        self.brush_size = tk.IntVar(value=4)
        self._last_x: int | None = None
        self._last_y: int | None = None

        self._build_ui()
        self._bind_events()

    def _build_ui(self) -> None:
        # Menu
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New (Clear)", accelerator="Ctrl+N", command=self.clear_canvas)
        file_menu.add_command(label="Save As...", accelerator="Ctrl+S", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", accelerator="Ctrl+Q", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menubar)

        # Toolbar
        toolbar = ttk.Frame(self, padding=6)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        color_btn = ttk.Button(toolbar, text="Pilih Warna", command=self.choose_color)
        color_btn.pack(side=tk.LEFT)

        ttk.Label(toolbar, text="Ukuran Kuas:").pack(side=tk.LEFT, padx=(12, 6))
        size_spin = ttk.Spinbox(toolbar, from_=1, to=30, width=5, textvariable=self.brush_size)
        size_spin.pack(side=tk.LEFT)

        clear_btn = ttk.Button(toolbar, text="Clear", command=self.clear_canvas)
        clear_btn.pack(side=tk.LEFT, padx=(12, 0))

        # Kanvas
        self.canvas = tk.Canvas(self, bg="#ffffff")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Status bar
        self.status_var = tk.StringVar(value="Siap menggambar")
        status = ttk.Label(self, textvariable=self.status_var, anchor="w")
        status.pack(side=tk.BOTTOM, fill=tk.X)

    def _bind_events(self) -> None:
        # Mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        # Keyboard shortcuts
        self.bind("<Control-n>", lambda e: self.clear_canvas())
        self.bind("<Control-s>", lambda e: self.save_as())
        self.bind("<Control-q>", lambda e: self.quit())

        # Show mouse position
        self.canvas.bind("<Motion>", self.on_motion)

    # Event handlers
    def on_press(self, event: tk.Event) -> None:
        self._last_x, self._last_y = event.x, event.y
        self.status_var.set(f"Mulai: ({event.x}, {event.y})")

    def on_drag(self, event: tk.Event) -> None:
        if self._last_x is None or self._last_y is None:
            return
        x, y = event.x, event.y
        size = max(1, int(self.brush_size.get()))
        self.canvas.create_line(self._last_x, self._last_y, x, y, fill=self.current_color, width=size, capstyle=tk.ROUND, smooth=True)
        self._last_x, self._last_y = x, y
        self.status_var.set(f"Menggambar: ({x}, {y}) | warna {self.current_color} | size {size}")

    def on_release(self, event: tk.Event) -> None:
        self._last_x, self._last_y = None, None
        self.status_var.set("Siap menggambar")

    def on_motion(self, event: tk.Event) -> None:
        self.status_var.set(f"Posisi: ({event.x}, {event.y})")

    def choose_color(self) -> None:
        color = colorchooser.askcolor(title="Pilih warna garis", color=self.current_color)
        if color and color[1]:
            self.current_color = color[1]
            self.status_var.set(f"Warna dipilih: {self.current_color}")

    def clear_canvas(self) -> None:
        self.canvas.delete("all")
        self.status_var.set("Kanvas dibersihkan")

    def save_as(self) -> None:
        try:
            filename = filedialog.asksaveasfilename(
                title="Simpan sebagai",
                defaultextension=".ps",
                filetypes=[("PostScript", "*.ps"), ("Semua file", "*.*")],
            )
            if not filename:
                return
            # PostScript: cocok untuk vektor/kanvas sederhana
            self.canvas.postscript(file=filename, colormode="color")
            messagebox.showinfo("Simpan", f"Berhasil menyimpan ke: {filename}")
        except Exception as e:
            messagebox.showerror("Gagal menyimpan", str(e))


if __name__ == "__main__":
    app = PaintApp()
    app.mainloop()
