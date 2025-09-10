# ui/boyer_moore_widget.py
"""
Widget cho thuật toán Boyer-Moore
"""

import tkinter as tk
from tkinter import ttk
from .base_widget import BaseAlgorithmWidget
from algorithms import BoyerMooreAlgorithm
from config import COLORS


class BoyerMooreWidget(BaseAlgorithmWidget):
    """
    Widget hiển thị thuật toán Boyer-Moore
    """
    
    def __init__(self, master, show_toolbar=True, font_size=18):
        algorithm = BoyerMooreAlgorithm()
        self.array_var = None  # Khởi tạo trước khi gọi super()
        super().__init__(master, algorithm, show_toolbar, font_size)
    
    def _build_info_area(self):
        """Override để thêm label hiển thị bảng last occurrence"""
        # Info frame with compact styling - sát với Search Pattern
        info = ttk.Frame(self, style="Card.TFrame", padding=(12, 3, 12, 6))
        info.pack(fill="x", padx=10, pady=(0, 2))  # Minimal padding
        
        # Last occurrence table section - compact
        table_frame = ttk.Frame(info, style="Info.TFrame", padding=(6, 2, 6, 2))
        table_frame.pack(fill="x", pady=(0, 2))
        
        table_label = ttk.Label(table_frame, text="📋 Last Occurrence Table:", style="Header.TLabel")
        table_label.pack(anchor="w", pady=(0, 1))
        
        # Thêm label hiển thị bảng last occurrence với styling đẹp
        self.array_var = tk.StringVar()
        ttk.Label(table_frame, textvariable=self.array_var, anchor="w", 
                 font=("JetBrains Mono", 11, "bold"),
                 foreground=COLORS["status_text"],
                 background=COLORS["accent_bg"]).pack(fill="x")
        
        # Status variables
        self.status_var = tk.StringVar()
        self.result_var = tk.StringVar()
        self.summary_var = tk.StringVar()
        
        # Status section - compact
        status_frame = ttk.Frame(info, style="Info.TFrame", padding=(6, 4, 6, 4))
        status_frame.pack(fill="x", pady=(0, 4))
        
        status_label = ttk.Label(status_frame, text="📊 Algorithm Status:", style="Header.TLabel")
        status_label.pack(anchor="w", pady=(0, 2))
        
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
    
    def _update_result(self):
        """Override để cập nhật cả bảng last occurrence"""
        super()._update_result()
        if hasattr(self, 'array_var') and self.array_var:
            self.array_var.set(self.algorithm.get_last_table_string())
