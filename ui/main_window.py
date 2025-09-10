# main_window.py
import tkinter as tk
from tkinter import ttk
from config import UI_CONFIG, DEFAULT_VALUES, ALGORITHM_CONFIG, THEME_CONFIG, COLORS
from .brute_force_widget import BruteForceWidget
from .boyer_moore_widget import BoyerMooreWidget


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title(UI_CONFIG["window_title"])
        self.geometry(UI_CONFIG["window_size"])
        self.minsize(*UI_CONFIG["min_size"])
        
        self._setup_style()
        self._build_ui()
        
        # Áp dụng zoom mặc định
        self.on_zoom()
        self.center_on_screen()
    
    def _setup_style(self):
        """Thiết lập style cho ứng dụng"""
        try:
            self.call("tk", "scaling", 1.0)
        except Exception:
            pass
        
        style = ttk.Style(self)
        if THEME_CONFIG["default_theme"] in style.theme_names():
            style.theme_use(THEME_CONFIG["default_theme"])
        
        # Configure modern styles with premium theme
        style.configure("TLabel", 
                       font=(UI_CONFIG["default_font"], UI_CONFIG["default_font_size"]),
                       background=COLORS["primary_bg"],
                       foreground=COLORS["summary_text"])
        
        style.configure("TButton", 
                       font=(UI_CONFIG["default_font"], UI_CONFIG["default_font_size"], "bold"), 
                       padding=(16, 10),
                       background=COLORS["button_primary"],
                       foreground="white",
                       borderwidth=0,
                       focuscolor="none")
        
        style.configure("TEntry", 
                       font=(UI_CONFIG["code_font"], UI_CONFIG["code_font_size"]),
                       fieldbackground=COLORS["secondary_bg"],
                       borderwidth=2,
                       relief="solid",
                       bordercolor=COLORS["border_light"])
        
        style.configure("TNotebook.Tab", 
                       padding=(20, 12, 20, 12),
                       font=(UI_CONFIG["default_font"], UI_CONFIG["default_font_size"], "bold"),
                       background=COLORS["header_bg"],
                       foreground=COLORS["status_text"])
        
        style.configure("Header.TLabel", 
                       font=(UI_CONFIG["default_font"], UI_CONFIG["header_font_size"], "bold"),
                       foreground=COLORS["status_text"],
                       background=COLORS["primary_bg"])
        
        style.configure("Title.TLabel",
                       font=(UI_CONFIG["default_font"], UI_CONFIG["title_font_size"], "bold"),
                       foreground=COLORS["title_text"],
                       background=COLORS["primary_bg"])
        
        # Configure frame styles with shadows
        style.configure("Card.TFrame",
                       background=COLORS["card_bg"],
                       relief="solid",
                       borderwidth=1,
                       bordercolor=COLORS["border_light"])
        
        style.configure("Info.TFrame",
                       background=COLORS["accent_bg"],
                       relief="flat")
        
        style.configure("Header.TFrame",
                       background=COLORS["header_bg"],
                       relief="flat")
        
        # Configure button styles
        style.map("TButton",
                 background=[("active", COLORS["button_info"]),
                           ("pressed", COLORS["button_primary"])])
        
        style.map("TNotebook.Tab",
                 background=[("selected", COLORS["secondary_bg"]),
                           ("active", COLORS["accent_bg"])])
    
    def _build_ui(self):
        """Xây dựng giao diện chính"""
        # Header
        self._build_header()
        
        # Control bar
        self._build_control_bar()
        
        # Footer
        self._build_footer()
        
        # Khởi tạo input bar theo tab hiện tại
        t, p = self.current_view().get_inputs()
        self.in_text.set(t)
        self.in_pat.set(p)
    
    def _build_header(self):
        """Xây dựng header với tabs"""
        # Main header frame with compact styling
        header = ttk.Frame(self, style="Header.TFrame", padding=(20, 12, 20, 8))
        header.pack(fill="x", padx=12, pady=(8, 3))
        
        # Title section with gradient effect
        title_frame = ttk.Frame(header, style="Header.TFrame")
        title_frame.pack(fill="x", pady=(0, 6))
        
        # Main title with icon
        title_label = ttk.Label(title_frame, text="🚀 String Search Studio", style="Title.TLabel")
        title_label.pack(side="left")
        
        # Subtitle
        subtitle_label = ttk.Label(title_frame, text="Advanced Algorithm Visualization", 
                                 style="Header.TLabel")
        subtitle_label.pack(side="left", padx=(12, 0))
        
        # Algorithm tabs with premium styling
        self.nb = ttk.Notebook(header, style="TNotebook")
        self.bf_tab = BruteForceWidget(self.nb, show_toolbar=False, font_size=UI_CONFIG["display_font_size"])
        self.bm_tab = BoyerMooreWidget(self.nb, show_toolbar=False, font_size=UI_CONFIG["display_font_size"])
        
        self.nb.add(self.bf_tab, text="🔍 Brute-Force Algorithm")
        self.nb.add(self.bm_tab, text="⚡ Boyer–Moore (Bad-Char Rule)")
        self.nb.pack(fill="both", expand=True, pady=(5, 0))
        
        # Bind tab change event
        self.nb.bind("<<NotebookTabChanged>>", self.on_tab_change)
    
    def _build_control_bar(self):
        """Xây dựng thanh điều khiển"""
        # Control bar frame with compact styling
        bar = ttk.Frame(self, style="Card.TFrame", padding=(15, 8, 15, 8))
        bar.pack(fill="x", padx=10, pady=2)
        
        # Input section
        input_frame = ttk.Frame(bar)
        input_frame.pack(fill="x", pady=(0, 6))
        
        # Text input
        ttk.Label(input_frame, text="📝 Text:", style="Header.TLabel").grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.in_text = tk.StringVar(value=DEFAULT_VALUES["text"])
        text_entry = ttk.Entry(input_frame, textvariable=self.in_text, width=50, font=(UI_CONFIG["code_font"], UI_CONFIG["code_font_size"]))
        text_entry.grid(row=0, column=1, columnspan=3, sticky="we", padx=(0, 20))
        
        # Pattern input
        ttk.Label(input_frame, text="🔍 Pattern:", style="Header.TLabel").grid(row=0, column=4, sticky="w", padx=(0, 10))
        self.in_pat = tk.StringVar(value=DEFAULT_VALUES["pattern"])
        pattern_entry = ttk.Entry(input_frame, textvariable=self.in_pat, width=15, font=(UI_CONFIG["code_font"], UI_CONFIG["code_font_size"]))
        pattern_entry.grid(row=0, column=5, sticky="w", padx=(0, 20))
        
        input_frame.grid_columnconfigure(1, weight=1)
        
        # Control section
        control_frame = ttk.Frame(bar)
        control_frame.pack(fill="x")
        
        # Settings
        settings_frame = ttk.Frame(control_frame)
        settings_frame.pack(side="left", fill="x", expand=True)
        
        ttk.Label(settings_frame, text="⏱️ Auto (ms):", style="Header.TLabel").pack(side="left", padx=(0, 5))
        self.in_ms = tk.IntVar(value=DEFAULT_VALUES["auto_delay_ms"])
        ttk.Spinbox(
            settings_frame, 
            from_=ALGORITHM_CONFIG["min_delay_ms"], 
            to=ALGORITHM_CONFIG["max_delay_ms"], 
            increment=ALGORITHM_CONFIG["delay_increment"], 
            textvariable=self.in_ms, 
            width=8
        ).pack(side="left", padx=(0, 20))
        
        ttk.Label(settings_frame, text="🔍 Zoom:", style="Header.TLabel").pack(side="left", padx=(0, 5))
        self.zoom = tk.IntVar(value=DEFAULT_VALUES["zoom_percentage"])
        z = ttk.Combobox(
            settings_frame,
            values=ALGORITHM_CONFIG["zoom_levels"],
            textvariable=self.zoom,
            state="readonly",
            width=5,
        )
        z.pack(side="left", padx=(0, 20))
        z.bind("<<ComboboxSelected>>", self.on_zoom)
        
        # Buttons with premium styling
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(side="right")
        
        # Apply button (Primary)
        apply_btn = ttk.Button(button_frame, text="✨ Apply", command=self.apply_inputs)
        apply_btn.pack(side="left", padx=3)
        
        # Reset button (Warning)
        reset_btn = ttk.Button(button_frame, text="🔄 Reset", command=self.cmd_reset)
        reset_btn.pack(side="left", padx=3)
        
        # Step button (Info)
        step_btn = ttk.Button(button_frame, text="⏭️ Step", command=self.cmd_step)
        step_btn.pack(side="left", padx=3)
        
        # Auto button (Success)
        auto_btn = ttk.Button(button_frame, text="▶️ Auto", command=self.cmd_auto)
        auto_btn.pack(side="left", padx=3)
        
        # Pause button (Danger)
        pause_btn = ttk.Button(button_frame, text="⏸️ Pause", command=self.cmd_pause)
        pause_btn.pack(side="left", padx=3)
    
    def _build_footer(self):
        """Xây dựng footer"""
        # Footer with compact styling
        foot = ttk.Frame(self, style="Info.TFrame", padding=(15, 6, 15, 8))
        foot.pack(fill="x", padx=12, pady=(3, 8))
        
        # Tip section
        tip_frame = ttk.Frame(foot, style="Info.TFrame")
        tip_frame.pack(fill="x")
        
        tip_label = ttk.Label(tip_frame, 
                             text="💡 Tip: Nhập Text/Pattern ở thanh trên, nhấn Apply để áp dụng cho tab đang chọn.",
                             style="Header.TLabel",
                             foreground=COLORS["status_text"])
        tip_label.pack(anchor="w")
        
        # Version info
        version_frame = ttk.Frame(foot, style="Info.TFrame")
        version_frame.pack(fill="x", pady=(8, 0))
        
        version_label = ttk.Label(version_frame,
                                 text="🚀 String Search Studio v2.0 | Advanced Algorithm Visualization",
                                 font=(UI_CONFIG["default_font"], 9),
                                 foreground=COLORS["summary_text"])
        version_label.pack(anchor="e")
    
    def center_on_screen(self):
        """Căn giữa cửa sổ trên màn hình"""
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        if w <= 1 or h <= 1:
            geo = self.geometry().split("+")[0]
            w, h = map(int, geo.split("x"))
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")
    
    def current_view(self):
        """Lấy widget hiện tại đang được chọn"""
        return self.nb.nametowidget(self.nb.select())
    
    def apply_inputs(self):
        """Áp dụng input từ control bar"""
        view = self.current_view()
        view.set_inputs(self.in_text.get(), self.in_pat.get())
        view.set_speed(int(self.in_ms.get()))
    
    def on_tab_change(self, _event=None):
        """Xử lý khi chuyển tab"""
        # Pause cả hai tab
        try:
            self.bf_tab.public_pause()
        except Exception:
            pass
        try:
            self.bm_tab.public_pause()
        except Exception:
            pass
        
        # Sync input theo tab mới
        v = self.current_view()
        t, p = v.get_inputs()
        self.in_text.set(t)
        self.in_pat.set(p)
    
    def cmd_reset(self):
        """Reset tab hiện tại"""
        self.current_view().public_reset()
    
    def cmd_step(self):
        """Step tab hiện tại"""
        self.current_view().public_step()
    
    def cmd_auto(self):
        """Auto tab hiện tại"""
        self.current_view().set_speed(int(self.in_ms.get()))
        self.current_view().public_auto()
    
    def cmd_pause(self):
        """Pause tab hiện tại"""
        self.current_view().public_pause()
    
    def on_zoom(self, *_):
        """Xử lý zoom"""
        factor = max(1.0, float(self.zoom.get()) / 100.0)
        
        # Phóng control elements
        try:
            self.call("tk", "scaling", factor)
        except Exception:
            pass
        
        # Phóng font size
        new_size = max(14, int(16 * factor))
        self.bf_tab.set_font_size(new_size)
        self.bm_tab.set_font_size(new_size)
