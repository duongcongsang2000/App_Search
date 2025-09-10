# ui/__init__.py
"""
Package giao diện cho ứng dụng String Search Studio
"""

from .main_window import MainWindow
from .brute_force_widget import BruteForceWidget
from .boyer_moore_widget import BoyerMooreWidget
from .base_widget import BaseAlgorithmWidget

__all__ = ['MainWindow', 'BruteForceWidget', 'BoyerMooreWidget', 'BaseAlgorithmWidget']
