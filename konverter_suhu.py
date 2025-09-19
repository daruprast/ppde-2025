import tkinter as tk
from tkinter import ttk
import math
from tkinter import font

class KonverterSuhu:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🌡️ Konverter Suhu Universal - Advanced UI")
        self.window.geometry("800x700")
        self.window.configure(bg='#E8F4FD')  # Light blue background
        
        # Custom fonts
        self.title_font = font.Font(family="Segoe UI", size=18, weight="bold")
        self.label_font = font.Font(family="Segoe UI", size=11, weight="bold")
        self.entry_font = font.Font(family="Segoe UI", size=11)
        self.info_font = font.Font(family="Segoe UI", size=9)

        # Color scheme modern
        self.colors = {
            'primary': '#2E86AB',      # Blue
            'secondary': '#A23B72',    # Purple
            'accent': '#F18F01',       # Orange
            'success': '#28A745',      # Green
            'danger': '#DC3545',       # Red
            'bg_light': '#F8F9FA',     # Light gray
            'bg_main': '#E8F4FD',      # Main background
            'text_dark': '#2C3E50',    # Dark text
            'text_light': '#FFFFFF',   # White text
            'shadow': '#00000020'      # Semi-transparent shadow
        }

        # Variabel kontrol
        self.celsius_var = tk.DoubleVar()
        self.fahrenheit_var = tk.DoubleVar()
        self.kelvin_var = tk.DoubleVar()
        self.rankine_var = tk.DoubleVar()

        # Flag untuk mencegah infinite loop saat update
        self.updating = False

        self.buat_interface()
        self.setup_traces()

        self.update_info()
        
    def setup_gradient_background(self):
        """Membuat gradient background dengan canvas"""
        self.bg_canvas = tk.Canvas(self.window, highlightthickness=0)
        self.bg_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Update gradient saat window resize
        self.window.bind('<Configure>', self.update_gradient)
        
    def update_gradient(self, event=None):
        """Update gradient background"""
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        
        self.bg_canvas.delete("gradient")
        
        # Create gradient effect
        for i in range(height):
            ratio = i / height
            # Interpolate between light blue and white
            r = int(173 + (255 - 173) * ratio)
            g = int(216 + (255 - 216) * ratio)
            b = int(230 + (255 - 230) * ratio)
            color = f"#{r:02x}{g:02x}{b:02x}"
            
            self.bg_canvas.create_line(0, i, width, i, fill=color, tags="gradient")
        

    def buat_interface(self):
        # Main scrollable frame
        main_frame = tk.Frame(self.window, bg=self.colors['bg_main'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header dengan design yang lebih menarik
        header_frame = tk.Frame(main_frame, bg=self.colors['bg_main'])
        header_frame.pack(fill='x', pady=(0, 30))
        
        # Title dengan gradient effect menggunakan label
        title_container = tk.Frame(header_frame, bg=self.colors['primary'], relief='flat', bd=0)
        title_container.pack(fill='x', pady=5)
        
        main_title = tk.Label(
            title_container,
            text="🌡️ KONVERTER SUHU UNIVERSAL",
            font=self.title_font,
            fg=self.colors['text_light'],
            bg=self.colors['primary'],
            pady=15
        )
        main_title.pack()
        
        subtitle = tk.Label(
            header_frame,
            text="✨ Advanced Temperature Converter with Smart Information ✨",
            font=self.info_font,
            fg=self.colors['secondary'],
            bg=self.colors['bg_main']
        )
        subtitle.pack(pady=(10, 0))

        # Container untuk input fields
        input_container = tk.Frame(main_frame, bg=self.colors['bg_main'])
        input_container.pack(fill='x', pady=20)

        # Data untuk setiap input field
        fields_data = [
            ("Celsius", "°C", self.celsius_var, self.colors['primary'], "❄️"),
            ("Fahrenheit", "°F", self.fahrenheit_var, self.colors['secondary'], "🌡️"),
            ("Kelvin", "K", self.kelvin_var, self.colors['accent'], "🔬"),
            ("Rankine", "°R", self.rankine_var, self.colors['danger'], "⚗️")
        ]

        # Buat input fields dengan design card
        for i, (name, unit, var, color, icon) in enumerate(fields_data):
            self.create_modern_input_card(input_container, name, unit, var, color, icon, i)

        # Control buttons
        self.create_control_buttons(input_container)

        # Info panel
        self.create_modern_info_panel(main_frame)

    def create_modern_input_card(self, parent, name, unit, variable, color, icon, row):
        """Membuat card input yang modern untuk setiap satuan suhu"""
        # Card container dengan shadow effect
        card_frame = tk.Frame(parent, bg='white', relief='flat', bd=0)
        card_frame.pack(fill='x', pady=8, padx=10)
        
        # Add shadow effect
        shadow_frame = tk.Frame(parent, bg='#E0E0E0', relief='flat', bd=0)
        shadow_frame.pack(fill='x', pady=8, padx=10)
        shadow_frame.place(in_=card_frame, x=3, y=3)
        card_frame.lift()

        # Inner container
        inner_frame = tk.Frame(card_frame, bg='white', padx=20, pady=15)
        inner_frame.pack(fill='x')

        # Icon dan label
        left_frame = tk.Frame(inner_frame, bg='white')
        left_frame.pack(side='left', fill='y')

        icon_label = tk.Label(
            left_frame,
            text=icon,
            font=font.Font(size=20),
            bg='white'
        )
        icon_label.pack(anchor='w')

        name_label = tk.Label(
            left_frame,
            text=f"{name} ({unit})",
            font=self.label_font,
            fg=color,
            bg='white'
        )
        name_label.pack(anchor='w', pady=(5, 0))

        # Entry field dengan styling
        entry_frame = tk.Frame(inner_frame, bg='white')
        entry_frame.pack(side='right', padx=(20, 0))

        entry = tk.Entry(
            entry_frame,
            textvariable=variable,
            font=self.entry_font,
            width=15,
            justify='center',
            relief='flat',
            bd=5,
            bg='#F8F9FA',
            fg=self.colors['text_dark'],
            insertbackground=color
        )
        entry.pack(pady=5)

        # Hover effects
        def on_enter(e):
            entry.configure(bg='#E3F2FD', relief='solid', bd=1)
            
        def on_leave(e):
            entry.configure(bg='#F8F9FA', relief='flat', bd=5)

        entry.bind("<Enter>", on_enter)
        entry.bind("<Leave>", on_leave)

    def create_control_buttons(self, parent):
        """Membuat tombol kontrol dengan design modern"""
        button_frame = tk.Frame(parent, bg=self.colors['bg_main'])
        button_frame.pack(pady=20)

        # Reset button dengan design modern
        reset_btn = tk.Button(
            button_frame,
            text="🔄 RESET ALL",
            command=self.reset_semua,
            font=self.label_font,
            bg=self.colors['accent'],
            fg='white',
            relief='flat',
            bd=0,
            padx=30,
            pady=12,
            cursor='hand2'
        )
        reset_btn.pack(side='left', padx=10)

        # Add hover effect
        def on_reset_enter(e):
            reset_btn.configure(bg='#E17100')
            
        def on_reset_leave(e):
            reset_btn.configure(bg=self.colors['accent'])

        reset_btn.bind("<Enter>", on_reset_enter)
        reset_btn.bind("<Leave>", on_reset_leave)

        # Info button
        info_btn = tk.Button(
            button_frame,
            text="ℹ️ REFRESH INFO",
            command=self.update_info,
            font=self.label_font,
            bg=self.colors['primary'],
            fg='white',
            relief='flat',
            bd=0,
            padx=30,
            pady=12,
            cursor='hand2'
        )
        info_btn.pack(side='left', padx=10)

        # Add hover effect
        def on_info_enter(e):
            info_btn.configure(bg='#1E5F7F')
            
        def on_info_leave(e):
            info_btn.configure(bg=self.colors['primary'])

        info_btn.bind("<Enter>", on_info_enter)
        info_btn.bind("<Leave>", on_info_leave)

    def create_modern_info_panel(self, parent):
        """Membuat panel informasi dengan design modern"""
        # Info container dengan design card
        info_container = tk.Frame(parent, bg='white', relief='flat', bd=0)
        info_container.pack(fill='both', expand=True, pady=20, padx=40)

        # Shadow effect
        shadow_container = tk.Frame(parent, bg='#E0E0E0', relief='flat', bd=0)
        shadow_container.pack(fill='both', expand=True, pady=20, padx=40)
        shadow_container.place(in_=info_container, x=5, y=5)
        info_container.lift()

        # Header panel info
        info_header = tk.Frame(info_container, bg=self.colors['primary'], height=50)
        info_header.pack(fill='x')
        info_header.pack_propagate(False)

        header_label = tk.Label(
            info_header,
            text="📊 INFORMASI SUHU & KONTEKS ILMIAH",
            font=self.label_font,
            fg='white',
            bg=self.colors['primary']
        )
        header_label.pack(expand=True)

        # Content area dengan scrollbar
        content_frame = tk.Frame(info_container, bg='white')
        content_frame.pack(fill='both', expand=True, padx=0, pady=0)

        # Scrollbar dengan custom styling
        scrollbar = tk.Scrollbar(content_frame, bg='#F0F0F0', troughcolor='white')
        scrollbar.pack(side='right', fill='y', padx=(0, 5), pady=5)

        # Text widget dengan styling modern
        self.info_text = tk.Text(
            content_frame,
            wrap='word',
            font=self.info_font,
            bg='#FAFAFA',
            fg=self.colors['text_dark'],
            yscrollcommand=scrollbar.set,
            state='disabled',
            relief='flat',
            bd=0,
            padx=20,
            pady=15,
            selectbackground=self.colors['primary'],
            selectforeground='white'
        )
        self.info_text.pack(side='left', fill='both', expand=True, padx=(5, 0), pady=5)
        scrollbar.config(command=self.info_text.yview)
    
    def setup_traces(self):
        """Setup trace untuk semua variabel"""
        self.celsius_var.trace_add("write", self.from_celsius)
        self.fahrenheit_var.trace_add("write", self.from_fahrenheit)
        self.kelvin_var.trace_add("write", self.from_kelvin)
        self.rankine_var.trace_add("write", self.from_rankine)
    
    def from_celsius(self, *args):
        """Konversi dari Celsius ke skala lain"""
        if self.updating:
            return

        try:
            celsius = self.celsius_var.get()
            self.updating = True

            # Konversi ke Fahrenheit
            fahrenheit = (celsius * 9/5) + 32
            self.fahrenheit_var.set(round(fahrenheit, 2))

            # Konversi ke Kelvin
            kelvin = celsius + 273.15
            self.kelvin_var.set(round(kelvin, 2))

            # Konversi ke Rankine
            rankine = (celsius + 273.15) * 9/5
            self.rankine_var.set(round(rankine, 2))

            self.updating = False

            self.update_info()

        except tk.TclError:
            # Terjadi saat input tidak valid (kosong atau bukan angka)
            pass
        except Exception as e:
            self.updating = False

    def from_fahrenheit(self, *args):
        """Konversi dari Fahrenheit ke skala lain"""
        if self.updating:
            return

        try:
            fahrenheit = self.fahrenheit_var.get()
            self.updating = True

            # Konversi ke Celsius
            celsius = (fahrenheit - 32) * 5/9
            self.celsius_var.set(round(celsius, 2))

            # Konversi ke Kelvin
            kelvin = celsius + 273.15
            self.kelvin_var.set(round(kelvin, 2))

            # Konversi ke Rankine
            rankine = fahrenheit + 459.67
            self.rankine_var.set(round(rankine, 2))

            self.updating = False

            self.update_info()

        except tk.TclError:
            pass
        except Exception as e:
            self.updating = False

    def from_kelvin(self, *args):
        """Konversi dari Kelvin ke skala lain"""
        if self.updating:
            return

        try:
            kelvin = self.kelvin_var.get()
            self.updating = True

            # Konversi ke Celsius
            celsius = kelvin - 273.15
            self.celsius_var.set(round(celsius, 2))

            # Konversi ke Fahrenheit
            fahrenheit = (celsius * 9/5) + 32
            self.fahrenheit_var.set(round(fahrenheit, 2))

            # Konversi ke Rankine
            rankine = kelvin * 9/5
            self.rankine_var.set(round(rankine, 2))

            self.updating = False

            self.update_info()

        except tk.TclError:
            pass
        except Exception as e:
            self.updating = False

    def from_rankine(self, *args):
        """Konversi dari Rankine ke skala lain"""
        if self.updating:
            return

        try:
            rankine = self.rankine_var.get()
            self.updating = True

            # Konversi ke Kelvin
            kelvin = rankine * 5/9
            self.kelvin_var.set(round(kelvin, 2))

            # Konversi ke Celsius
            celsius = kelvin - 273.15
            self.celsius_var.set(round(celsius, 2))

            # Konversi ke Fahrenheit
            fahrenheit = rankine - 459.67
            self.fahrenheit_var.set(round(fahrenheit, 2))

            self.updating = False

            self.update_info()

        except tk.TclError:
            pass
        except Exception as e:
            self.updating = False
    
    def reset_all(self):
        """Reset semua field"""
        self.updating = True
        self.celsius_var.set(0)
        self.fahrenheit_var.set(0)
        self.kelvin_var.set(0)
        self.rankine_var.set(0)
        self.updating = False
        self.update_info()

    def update_info(self):
        """Update informasi tambahan dengan konteks suhu yang berguna"""
        try:
            celsius = self.celsius_var.get()
            fahrenheit = self.fahrenheit_var.get()

            # Informasi dasar
            info_text = f"🌡️ INFORMASI SUHU 🌡️\n"
            info_text += f"Celsius: {celsius:.1f}°C | Fahrenheit: {fahrenheit:.1f}°F\n\n"

            # Konteks suhu berdasarkan nilai Celsius
            if celsius <= -273.15:
                info_text += "❄️ SUHU ABSOLUT NOL - Tidak mungkin lebih dingin!"
                info_text += "\n• Semua molekul berhenti bergerak"
            elif celsius < -40:
                info_text += "🥶 EKSTREM DINGIN - Berbahaya untuk manusia!"
                info_text += "\n• Lebih dingin dari kutub utara di musim dingin"
            elif celsius < -18:
                info_text += "❄️ SANGAT DINGIN - Freezer rumah tangga"
                info_text += "\n• Suhu penyimpanan makanan beku"
            elif celsius < 0:
                info_text += "🧊 BEKU - Air berubah menjadi es"
                info_text += "\n• Di bawah titik beku air"
            elif celsius == 0:
                info_text += "🧊 TITIK BEKU AIR"
                info_text += "\n• Air mulai membeku pada tekanan normal"
            elif celsius < 10:
                info_text += "🥶 DINGIN - Perlu jaket tebal"
                info_text += "\n• Cuaca musim dingin yang sejuk"
            elif celsius < 20:
                info_text += "😊 SEJUK - Cuaca yang nyaman"
                info_text += "\n• Ideal untuk aktivitas outdoor"
            elif celsius < 25:
                info_text += "🌤️ HANGAT - Suhu ruangan yang nyaman"
                info_text += "\n• Suhu ideal untuk bekerja dan belajar"
            elif celsius < 30:
                info_text += "☀️ PANAS - Cuaca musim panas"
                info_text += "\n• Mulai terasa panas, butuh ventilasi"
            elif celsius < 37:
                info_text += "🔥 SANGAT PANAS - Suhu tubuh manusia normal: 37°C"
                info_text += "\n• Batas aman untuk aktivitas outdoor"
            elif celsius < 40:
                info_text += "🌡️ DEMAM TINGGI jika suhu tubuh"
                info_text += "\n• Berbahaya untuk kesehatan manusia"
            elif celsius < 50:
                info_text += "🔥 PANAS EKSTREM - Suhu gurun"
                info_text += "\n• Suhu tertinggi yang pernah tercatat di bumi: 54°C"
            elif celsius < 60:
                info_text += "♨️ AIR PANAS - Untuk mandi yang nyaman"
                info_text += "\n• Suhu air panas biasanya 40-60°C"
            elif celsius < 100:
                info_text += "🔥 SANGAT PANAS - Berbahaya untuk sentuhan"
                info_text += "\n• Air mulai menguap dengan cepat"
            elif celsius == 100:
                info_text += "💨 TITIK DIDIH AIR"
                info_text += "\n• Air berubah menjadi uap pada tekanan normal"
            elif celsius < 200:
                info_text += "🔥 SUPER PANAS - Suhu oven"
                info_text += "\n• Untuk memasak dan memanggang"
            else:
                info_text += "🔥 EKSTREM PANAS - Suhu industri"
                info_text += "\n• Digunakan dalam proses manufaktur"

            # Tambahan fakta menarik
            info_text += "\n\n📊 FAKTA MENARIK:"
            if celsius == 0:
                info_text += "\n• Air laut membeku pada -2°C karena kandungan garam"
            elif celsius == 37:
                info_text += "\n• Suhu tubuh manusia normal adalah 37°C"
            elif celsius == 100:
                info_text += "\n• Di puncak gunung, air mendidih pada suhu lebih rendah"
            elif abs(celsius - (-40)) < 1:
                info_text += "\n• -40°C = -40°F (satu-satunya titik yang sama!)"

            self.info_text.config(state=tk.NORMAL)
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, info_text)
            self.info_text.config(state=tk.DISABLED)

        except:
            self.info_text.config(state=tk.NORMAL)
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, "🌡️ Masukkan nilai suhu yang valid untuk melihat informasi")
            self.info_text.config(state=tk.DISABLED)

    def reset_semua(self):
        """Reset semua input field ke nilai 0 dengan animasi"""
        self.updating = True
        
        # Animate reset dengan smooth transition
        self.animate_reset()
        
        self.celsius_var.set(0.0)
        self.fahrenheit_var.set(32.0)
        self.kelvin_var.set(273.15)
        self.rankine_var.set(491.67)
        self.updating = False
        self.update_info()
        
        # Flash effect untuk memberikan feedback visual
        self.flash_reset_feedback()

    def animate_reset(self):
        """Animasi visual saat reset"""
        # Temporary visual feedback
        pass

    def flash_reset_feedback(self):
        """Flash effect untuk reset feedback"""
        original_bg = self.window.cget('bg')
        
        def flash_white():
            # Flash effect implementation bisa ditambahkan di sini
            pass

    def add_temperature_scale_indicator(self):
        """Menambahkan indikator skala suhu visual"""
        # Bisa ditambahkan thermometer visual indicator
        pass

    def jalankan(self):
        """Method untuk menjalankan aplikasi"""
        self.window.mainloop()
    
if __name__ == "__main__":
    app = KonverterSuhu()
    app.jalankan()
        
        