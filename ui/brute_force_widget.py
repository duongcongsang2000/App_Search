# ui/brute_force_widget.py
from .base_widget import BaseAlgorithmWidget
from algorithms import BruteForceAlgorithm

class BruteForceWidget(BaseAlgorithmWidget):
    
    def __init__(self, master, show_toolbar=True, font_size=18):
        algorithm = BruteForceAlgorithm()
        super().__init__(master, algorithm, show_toolbar, font_size)