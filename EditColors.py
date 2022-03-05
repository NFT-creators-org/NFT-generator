from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QCheckBox

from EditColorsWidget import Ui_Form
from main import DEFAULT_COLORS


class EditColors(QtWidgets.QWidget, Ui_Form):
    def __init__(self, colors: set):
        self.colors = {i: (color, color in colors) for i, color in enumerate(DEFAULT_COLORS)}
        for i in sorted(self.colors):
            checkbox = QCheckBox(f"R:{i[0]} G:{i[1]} B:{i[2]}")
