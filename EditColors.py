from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QCheckBox

from EditColorsWidget import Ui_Form
from settings_data import DEFAULT_COLORS


class EditColors(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent, name_img: str, is_accessory: bool):
        try:
            super().__init__()
            self.setupUi(self)
            self.parent = parent
            self.name_img = name_img
            self.is_accessory = is_accessory
            if is_accessory:
                colors = set(parent.accessories_data[name_img].colors)
            else:
                colors = set(parent.colors_layers[name_img])
            self.colors = {i: [color, color in colors] for i, color in enumerate(DEFAULT_COLORS)}
            for i in sorted(self.colors):
                color, flag = self.colors[i]
                checkbox = QCheckBox(f"R:{color[0]} G:{color[1]} B:{color[2]}")
                checkbox.setObjectName(f"checkbox_{i}")
                checkbox.clicked.connect(self.click_checkbox)
                checkbox.setChecked(flag)
                self.gridLayout_checkboxes_list.addWidget(checkbox, i, 0)
        except Exception as e:
            print(e)

    def click_checkbox(self):
        row = int(self.sender().objectName().split("_")[-1])
        self.colors[row][1] = not self.colors[row][1]

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        result_colors = [self.colors[i][0] for i in self.colors if self.colors[i][1]]
        if self.is_accessory:
            self.parent.accessories_data[self.name_img].set_colors(result_colors)
        else:
            self.parent.colors_layers[self.name_img][:] = result_colors[:]
