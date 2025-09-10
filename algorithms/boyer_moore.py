# algorithms/boyer_moore.py
"""
Thuật toán Boyer-Moore cho tìm kiếm chuỗi (Bad Character Rule)
"""

import time
from typing import List, Tuple, Dict


def build_last_occurrence_table(pattern: str) -> Dict[str, int]:
    """
    Xây dựng bảng last occurrence cho thuật toán Boyer-Moore
    
    Args:
        pattern: Chuỗi pattern cần tìm
        
    Returns:
        Dict mapping ký tự -> vị trí cuối cùng trong pattern
    """
    last = {}
    for j, char in enumerate(pattern):
        last[char] = j
    return last


class BoyerMooreAlgorithm:
    """
    Thuật toán Boyer-Moore sử dụng Bad Character Rule
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
        
        # Trạng thái thuật toán Boyer-Moore
        self.i = 0  # vị trí đầu cửa sổ trong T
        self.j = self.m - 1  # vị trí ký tự đang so trong P (từ phải sang trái)
        
        # Metrics
        self.compares = 0
        self.windows = 0
        self.new_window = True
        self.shifts = 0
        self.shift_sum = 0
        self.time_ms = 0.0
        
        self.matches = []
        self.last = build_last_occurrence_table(self.P) if self.m > 0 else {}
    
    def can_continue(self) -> bool:
        """Kiểm tra xem có thể tiếp tục thuật toán không"""
        return self.m > 0 and self.i <= self.n - self.m
    
    def step_once(self) -> Tuple[str, bool]:
        """
        Thực hiện một bước của thuật toán Boyer-Moore
        
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
        
        # So sánh ký tự (từ phải sang trái)
        t_char = self.T[self.i + self.j]
        p_char = self.P[self.j]
        self.compares += 1
        
        if t_char == p_char:
            # Khớp ký tự
            if self.j == 0:
                # Tìm thấy pattern
                self.matches.append(self.i)
                self.i += 1
                self.j = self.m - 1
                self.shifts += 1
                self.shift_sum += 1
                self.new_window = True
                self.time_ms += (time.perf_counter() - t0) * 1000.0
                return "Found! Dịch 1 ô.", True
            else:
                self.j -= 1
                self.time_ms += (time.perf_counter() - t0) * 1000.0
                return f"Khớp '{t_char}'. j←{self.j}.", True
        else:
            # Không khớp - áp dụng bad character rule
            lastpos = self.last.get(t_char, -1)
            shift = max(1, self.j - lastpos)
            self.i += shift
            self.j = self.m - 1
            self.shifts += 1
            self.shift_sum += shift
            self.new_window = True
            self.time_ms += (time.perf_counter() - t0) * 1000.0
            return f"Mismatch '{t_char}' vs '{p_char}'. last('{t_char}')={lastpos} ⇒ dịch {shift}.", True
    
    def get_status(self) -> str:
        """Lấy thông tin trạng thái hiện tại"""
        return f"[BM bad-char] i={self.i}, j={self.j}, so sánh={self.compares}"
    
    def get_metrics(self) -> dict:
        """Lấy các metrics của thuật toán"""
        return {
            "compares": self.compares,
            "windows": self.windows,
            "shifts": self.shifts,
            "shift_sum": self.shift_sum,
            "time_ms": self.time_ms,
            "matches": self.matches.copy(),
            "last_table": self.last.copy()
        }
    
    def get_current_positions(self) -> Tuple[int, int]:
        """Lấy vị trí hiện tại của con trỏ"""
        return self.i, self.j
    
    def get_last_table_string(self) -> str:
        """Lấy chuỗi hiển thị bảng last occurrence"""
        if self.m == 0:
            return "last[c] = {}"
        
        # Giữ thứ tự xuất hiện theo P
        ordered_keys = list(dict.fromkeys(self.P))
        mapping = ", ".join(f"{repr(ch)}:{self.last.get(ch, -1)}" for ch in ordered_keys)
        return f"last[c] = {{{mapping}}}"
