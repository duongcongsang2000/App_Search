# algorithms/brute_force.py
"""
Thuật toán Brute Force cho tìm kiếm chuỗi
"""

import time
from typing import List, Tuple


class BruteForceAlgorithm:
    """
    Thuật toán Brute Force để tìm kiếm pattern trong text
    """
    
    def __init__(self):
        self.reset()
    
    def reset(self, text: str = "", pattern: str = ""):
        """
        Khởi tạo lại trạng thái thuật toán
        
        Args:
            text: Chuỗi text để tìm kiếm
            pattern: Pattern cần tìm
        """
        self.T = text
        self.P = pattern
        self.n = len(self.T)
        self.m = len(self.P)
        
        # Trạng thái thuật toán
        self.i = 0  # vị trí đầu cửa sổ trong T
        self.j = 0  # vị trí ký tự đang so trong P (0..m-1)
        
        # Metrics
        self.compares = 0
        self.windows = 0
        self.new_window = True
        self.shifts = 0
        self.shift_sum = 0
        self.time_ms = 0.0
        
        self.matches = []
    
    def can_continue(self) -> bool:
        """Kiểm tra xem có thể tiếp tục thuật toán không"""
        return self.m > 0 and self.i <= self.n - self.m
    
    def step_once(self) -> Tuple[str, bool]:
        """
        Thực hiện một bước của thuật toán
        
        Returns:
            Tuple[str, bool]: (thông báo trạng thái, có thể tiếp tục)
        """
        if not self.can_continue():
            return "Kết thúc.", False
        
        t0 = time.perf_counter()
        
        # Đếm cửa sổ mới
        if self.new_window:
            self.windows += 1
            self.new_window = False
        
        # So sánh ký tự
        t_char = self.T[self.i + self.j]
        p_char = self.P[self.j]
        self.compares += 1
        
        if t_char == p_char:
            # Khớp ký tự
            self.j += 1
            if self.j == self.m:
                # Tìm thấy pattern
                self.matches.append(self.i)
                self.i += 1
                self.j = 0
                self.shifts += 1
                self.shift_sum += 1
                self.new_window = True
                self.time_ms += (time.perf_counter() - t0) * 1000.0
                return "Tìm thấy mẫu. Trượt 1 ô.", True
            else:
                self.time_ms += (time.perf_counter() - t0) * 1000.0
                return f"Khớp '{t_char}'.", True
        else:
            # Không khớp - trượt cửa sổ
            self.i += 1
            self.j = 0
            self.shifts += 1
            self.shift_sum += 1
            self.new_window = True
            self.time_ms += (time.perf_counter() - t0) * 1000.0
            return f"Mismatch '{t_char}' vs '{p_char}'. Trượt 1 ô.", True
    
    def get_status(self) -> str:
        """Lấy thông tin trạng thái hiện tại"""
        return f"[Brute-Force] i={self.i}, j={self.j}, so sánh={self.compares}"
    
    def get_metrics(self) -> dict:
        """Lấy các metrics của thuật toán"""
        return {
            "compares": self.compares,
            "windows": self.windows,
            "shifts": self.shifts,
            "shift_sum": self.shift_sum,
            "time_ms": self.time_ms,
            "matches": self.matches.copy()
        }
    
    def get_current_positions(self) -> Tuple[int, int]:
        """Lấy vị trí hiện tại của con trỏ"""
        return self.i, self.j
