# config/settings.py
"""
Cấu hình chung cho ứng dụng String Search Studio
"""

# Cấu hình giao diện - Modern Design
UI_CONFIG = {
    "window_title": "🔍 String Search Studio — Brute-Force & Boyer–Moore",
    "window_size": "1200x800",
    "min_size": (1200, 800),
    "default_font": "Segoe UI",
    "code_font": "JetBrains Mono",
    "default_font_size": 11,
    "code_font_size": 12,
    "header_font_size": 15,
    "display_font_size": 13,
    "title_font_size": 19,
}

# Cấu hình mặc định
DEFAULT_VALUES = {
    "text": "abracadabra abracadabra",
    "pattern": "abra",
    "auto_delay_ms": 500,
    "zoom_percentage": 125,
}

# Cấu hình màu sắc - Premium UI Theme
COLORS = {
    # Highlight colors - Premium gradient style
    "cursor": "#FF6B35",           # Vibrant orange cursor
    "match": "#00C851",            # Emerald green match
    "mismatch": "#FF4444",         # Bright red mismatch  
    "found": "#33B5E5",            # Sky blue found
    
    # Text colors
    "result_text": "#1B5E20",      # Deep green
    "summary_text": "#37474F",     # Dark blue-gray
    "status_text": "#1565C0",      # Deep blue
    "title_text": "#0D47A1",       # Very dark blue
    
    # Background colors - Modern gradient
    "primary_bg": "#F8F9FA",       # Very light gray
    "secondary_bg": "#FFFFFF",     # Pure white
    "accent_bg": "#E8F4FD",        # Light blue
    "card_bg": "#FFFFFF",          # Card background
    "header_bg": "#F1F8FF",        # Light blue header
    
    # Border colors
    "border_light": "#E1E5E9",     # Light border
    "border_dark": "#90A4AE",      # Medium border
    "border_accent": "#2196F3",    # Blue border
    
    # Button colors - Material Design
    "button_primary": "#2196F3",   # Blue
    "button_success": "#4CAF50",   # Green
    "button_warning": "#FF9800",   # Orange
    "button_danger": "#F44336",    # Red
    "button_info": "#00BCD4",      # Cyan
    
    # Shadow colors
    "shadow_light": "#E0E0E0",     # Light shadow
    "shadow_medium": "#BDBDBD",    # Medium shadow
}

# Cấu hình thuật toán
ALGORITHM_CONFIG = {
    "min_delay_ms": 100,
    "max_delay_ms": 2000,
    "delay_increment": 50,
    "zoom_levels": [100, 125, 150, 175, 200],
}

# Cấu hình theme
THEME_CONFIG = {
    "default_theme": "clam",
    "fallback_theme": "default",
}
