# ui/base_widget.py
"""
Base widget cho các thuật toán tìm kiếm chuỗi
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Protocol, Any
from config import COLORS, ALGORITHM_CONFIG


class AlgorithmProtocol(Protocol):
    """Protocol cho các thuật toán"""
    
    def reset(self, text: str, pattern: str) -> None: ...
    def step_once(self) -> tuple[str, bool]: ...
    def can_continue(self) -> bool: ...
    def get_status(self) -> str: ...
    def get_metrics(self) -> dict: ...
    def get_current_positions(self) -> tuple[int, int]: ...


class BaseAlgorithmWidget(ttk.Frame):
    """
    Base widget cho hiển thị thuật toán tìm kiếm chuỗi
    """
    
    def __init__(self, master, algorithm: AlgorithmProtocol, show_toolbar=True, font_size=18):
        super().__init__(master)
        self.algorithm = algorithm
        self.show_toolbar = show_toolbar
        self.font_size = int(font_size)
        self.autoplay_id = None
        self.autoplay_delay_ms = ALGORITHM_CONFIG["min_delay_ms"]
        
        self._build_ui()
        self._reset_state()
    
    def _build_ui(self):
        """Xây dựng giao diện"""
        # Biến trạng thái
        self.text_var = tk.StringVar(value="abracadabra abracadabra")
        self.pat_var = tk.StringVar(value="abra")
        self.delay_var = tk.IntVar(value=self.autoplay_delay_ms)
        
        # Thanh công cụ (có thể ẩn)
        if self.show_toolbar:
            self._build_toolbar()
        
        # Vùng hiển thị text và pattern
        self._build_display_area()
        
        # Vùng thông tin
        self._build_info_area()
    
    def _build_toolbar(self):
        """Xây dựng thanh công cụ"""
        top = ttk.Frame(self, padding=10)
        top.pack(fill="x")
        
        # Text input
        ttk.Label(top, text="Text:").grid(row=0, column=0, sticky="w")
        ttk.Entry(top, textvariable=self.text_var, width=80).grid(
            row=0, column=1, columnspan=5, sticky="we", pady=2
        )
        
        # Pattern input
        ttk.Label(top, text="Pattern:").grid(row=1, column=0, sticky="w")
        ttk.Entry(top, textvariable=self.pat_var, width=30).grid(
            row=1, column=1, sticky="w", pady=2
        )
        
        # Delay input
        ttk.Label(top, text="Auto (ms):").grid(row=1, column=2, sticky="e")
        ttk.Spinbox(
            top, 
            from_=ALGORITHM_CONFIG["min_delay_ms"], 
            to=ALGORITHM_CONFIG["max_delay_ms"], 
            increment=ALGORITHM_CONFIG["delay_increment"], 
            textvariable=self.delay_var, 
            width=8,
            command=self._update_delay
        ).grid(row=1, column=3, sticky="w")
        
        # Buttons
        btns = ttk.Frame(top)
        btns.grid(row=1, column=4, columnspan=2, sticky="e")
        ttk.Button(btns, text="Reset", command=self.on_reset).grid(row=0, column=0, padx=3)
        ttk.Button(btns, text="Step", command=self.on_step).grid(row=0, column=1, padx=3)
        ttk.Button(btns, text="Auto ▶", command=self.on_auto).grid(row=0, column=2, padx=3)
        ttk.Button(btns, text="Pause ⏸", command=self.on_pause).grid(row=0, column=3, padx=3)
    
    def _build_display_area(self):
        """Xây dựng vùng hiển thị"""
        # Main display frame with premium styling
        mid = ttk.Frame(self, style="Card.TFrame", padding=(15, 8, 15, 3))
        mid.pack(fill="both", expand=True, padx=10, pady=3)
        
        # Text display section
        text_frame = ttk.Frame(mid, style="Info.TFrame", padding=(10, 6, 10, 5))
        text_frame.pack(fill="x", pady=(0, 5))
        
        # Text label
        text_label = ttk.Label(text_frame, text="📝 Text String:", style="Header.TLabel")
        text_label.pack(anchor="w", pady=(0, 3))
        
        # Text box with premium styling - smaller height
        self.text_box = tk.Text(text_frame, height=4, wrap="none", 
                               font=("JetBrains Mono", self.font_size),
                               bg=COLORS["secondary_bg"],
                               fg=COLORS["summary_text"],
                               relief="solid",
                               borderwidth=2,
                               highlightthickness=0)
        self.text_box.pack(fill="x")
        self.text_box.config(state="disabled")
        
        # Pattern display section - no gap
        pattern_frame = ttk.Frame(mid, style="Info.TFrame", padding=(10, 6, 10, 3))
        pattern_frame.pack(fill="x", pady=(0, 0))  # Removed gap
        
        # Pattern label
        pattern_label = ttk.Label(pattern_frame, text="🔍 Search Pattern:", style="Header.TLabel")
        pattern_label.pack(anchor="w", pady=(0, 3))
        
        # Pattern box with premium styling
        self.pat_box = tk.Text(pattern_frame, height=2, wrap="none", 
                              font=("JetBrains Mono", self.font_size),
                              bg=COLORS["secondary_bg"],
                              fg=COLORS["summary_text"],
                              relief="solid",
                              borderwidth=2,
                              highlightthickness=0)
        self.pat_box.pack(fill="x")
        self.pat_box.config(state="disabled")
        
        # Configure tags with premium colors and effects
        for box in (self.text_box, self.pat_box):
            box.tag_configure("cursor", 
                            background=COLORS["cursor"], 
                            foreground="#FFFFFF",
                            relief="raised",
                            borderwidth=1)
            box.tag_configure("match", 
                            background=COLORS["match"], 
                            foreground="#FFFFFF",
                            relief="raised",
                            borderwidth=1)
            box.tag_configure("mismatch", 
                            background=COLORS["mismatch"], 
                            foreground="#FFFFFF",
                            relief="raised",
                            borderwidth=1)
            box.tag_configure("found", 
                            background=COLORS["found"], 
                            foreground="#FFFFFF",
                            relief="raised",
                            borderwidth=1)
    
    def _build_info_area(self):
        """Xây dựng vùng thông tin"""
        # Info frame with compact styling - sát với Search Pattern
        info = ttk.Frame(self, style="Card.TFrame", padding=(12, 3, 12, 6))
        info.pack(fill="x", padx=10, pady=(0, 2))  # Minimal padding
        
        # Status variables
        self.status_var = tk.StringVar()
        self.result_var = tk.StringVar()
        self.summary_var = tk.StringVar()
        
        # Status section - compact
        status_frame = ttk.Frame(info, style="Info.TFrame", padding=(6, 2, 6, 2))
        status_frame.pack(fill="x", pady=(0, 2))
        
        status_label = ttk.Label(status_frame, text="📊 Algorithm Status:", style="Header.TLabel")
        status_label.pack(anchor="w", pady=(0, 1))
        
        ttk.Label(status_frame, textvariable=self.status_var, anchor="w", 
                 font=("Segoe UI", 10, "bold"),
                 foreground=COLORS["status_text"]).pack(fill="x")
        
        # Result section - compact
        result_frame = ttk.Frame(info, style="Info.TFrame", padding=(6, 4, 6, 4))
        result_frame.pack(fill="x", pady=(0, 4))
        
        result_label = ttk.Label(result_frame, text="🎯 Search Results:", style="Header.TLabel")
        result_label.pack(anchor="w", pady=(0, 2))
        
        ttk.Label(result_frame, textvariable=self.result_var, anchor="w", 
                 font=("Segoe UI", 11, "bold"),
                 foreground=COLORS["result_text"]).pack(fill="x")
        
        # Metrics section - compact
        metrics_frame = ttk.Frame(info, style="Info.TFrame", padding=(6, 4, 6, 4))
        metrics_frame.pack(fill="x")
        
        metrics_label = ttk.Label(metrics_frame, text="📈 Performance Metrics:", style="Header.TLabel")
        metrics_label.pack(anchor="w", pady=(0, 2))
        
        ttk.Label(metrics_frame, textvariable=self.summary_var, anchor="w", 
                 font=("Segoe UI", 10),
                 foreground=COLORS["summary_text"]).pack(fill="x")
    
    def _reset_state(self):
        """Khởi tạo lại trạng thái"""
        text = self.text_var.get()
        pattern = self.pat_var.get()
        self.algorithm.reset(text, pattern)
        self._update_delay()
        self._render_boxes()
        self._update_status("Ready. Nhấn Step hoặc Auto.")
        self._update_result()
    
    def _render_boxes(self):
        """Render text và pattern boxes"""
        def set_text(widget, text):
            widget.config(state="normal")
            widget.delete("1.0", "end")
            widget.insert("1.0", text)
            widget.config(state="disabled")
        
        set_text(self.text_box, self.algorithm.T + "\n")
        set_text(self.pat_box, " " * self.algorithm.i + self.algorithm.P + "\n")
        
        # Clear tags
        for box in (self.text_box, self.pat_box):
            box.config(state="normal")
            for tag in ("cursor", "match", "mismatch", "found"):
                box.tag_remove(tag, "1.0", "end")
            box.config(state="disabled")
        
        # Highlight matches
        metrics = self.algorithm.get_metrics()
        for pos in metrics["matches"]:
            self.text_box.tag_add("found", f"1.{pos}", f"1.{pos+self.algorithm.m}")
        
        # Highlight current position
        if self.algorithm.can_continue():
            i, j = self.algorithm.get_current_positions()
            if 0 <= i <= self.algorithm.n - self.algorithm.m and 0 <= j < self.algorithm.m:
                t_col = i + j
                self._tag_span(self.text_box, "cursor", t_col, t_col + 1)
                self._tag_span(self.pat_box, "cursor", i + j, i + j + 1)
    
    def _tag_span(self, widget, tag, start, end):
        """Thêm tag cho một khoảng text"""
        widget.config(state="normal")
        widget.tag_add(tag, f"1.{start}", f"1.{end}")
        widget.config(state="disabled")
    
    def _update_status(self, msg):
        """Cập nhật thông báo trạng thái"""
        status = self.algorithm.get_status()
        self.status_var.set(f"{status} | {msg}")
    
    def _update_result(self):
        """Cập nhật kết quả và metrics"""
        metrics = self.algorithm.get_metrics()
        matches = metrics["matches"]
        self.result_var.set("Found at: " + (", ".join(map(str, matches)) if matches else "(none)"))
        
        self.summary_var.set(
            f"Time: {metrics['time_ms']:.2f} ms | "
            f"Comparisons: {metrics['compares']} | "
            f"Windows: {metrics['windows']} | "
            f"Shifts: {metrics['shifts']} (Σ={metrics['shift_sum']})"
        )
    
    def _update_delay(self):
        """Cập nhật delay cho auto mode"""
        try:
            self.autoplay_delay_ms = int(self.delay_var.get())
        except:
            self.autoplay_delay_ms = ALGORITHM_CONFIG["min_delay_ms"]
    
    def step_once(self):
        """Thực hiện một bước thuật toán"""
        if self.algorithm.T != self.text_var.get() or self.algorithm.P != self.pat_var.get():
            self.on_reset()
        
        msg, can_continue = self.algorithm.step_once()
        self._update_status(msg)
        self._update_result()
        self._render_boxes()
        
        if not can_continue:
            self.on_pause()
    
    def on_step(self):
        """Xử lý nút Step"""
        try:
            self.step_once()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _auto_loop(self):
        """Vòng lặp cho auto mode"""
        self.step_once()
        if self.algorithm.can_continue():
            self.autoplay_id = self.after(self.autoplay_delay_ms, self._auto_loop)
        else:
            self.autoplay_id = None
    
    def on_auto(self):
        """Xử lý nút Auto"""
        self.on_pause()
        if self.algorithm.T != self.text_var.get() or self.algorithm.P != self.pat_var.get():
            self.on_reset()
        self._auto_loop()
    
    def on_pause(self):
        """Xử lý nút Pause"""
        if self.autoplay_id:
            self.after_cancel(self.autoplay_id)
            self.autoplay_id = None
    
    def on_reset(self):
        """Xử lý nút Reset"""
        self.on_pause()
        self._reset_state()
    
    # API cho main
    def public_step(self):
        self.on_step()
    
    def public_auto(self):
        self.on_auto()
    
    def public_pause(self):
        self.on_pause()
    
    def public_reset(self):
        self.on_reset()
    
    def set_inputs(self, text=None, pattern=None):
        if text is not None:
            self.text_var.set(text)
        if pattern is not None:
            self.pat_var.set(pattern)
        self.on_reset()
    
    def get_inputs(self):
        return self.text_var.get(), self.pat_var.get()
    
    def set_speed(self, ms: int):
        self.delay_var.set(ms)
        self._update_delay()
    
    def set_font_size(self, size: int):
        self.font_size = int(size)
        self.text_box.configure(font=("Consolas", self.font_size))
        self.pat_box.configure(font=("Consolas", self.font_size))
