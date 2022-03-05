from PyQt5 import QtWidgets
import sys
import os
import shutil

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QPushButton

from AppMainWindow import Ui_MainWindow
from SetupAnchors import SetupAnchors
from generator import merging, drawing, filling
from settings_data import CACHE_DIR, DEFAULT_COLORS
from EditColors import EditColors


class AccessoryData:
    def __init__(self, name):
        self.name = name
        self.colors = []
        self.anchors = []

    def set_colors(self, new_colors: list):
        self.colors[:] = new_colors[:]

    def get_colors(self):
        return self.colors[:]

    def set_anchors(self, new_anchors: list):
        self.anchors[:] = new_anchors[:]

    def get_anchors(self):
        return self.anchors[:]

    def __repr__(self):
        return f"($name={self.name} colors={self.colors} anchors={self.anchors}$)"

    def __hash__(self):
        return hash(self.name)


class AppStartWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # uic.loadUi('test.ui', self)
        self.setupUi(self)
        self.layers_list = dict()
        self.accessories_list = dict()
        self.is_exist = dict()
        self.is_exist_accessory = dict()
        self.accessories_data = dict()
        AppStartWindow.create_cache()
        self.src_preview = "preview_for_app.png"
        self.print_image_preview()
        self.build_handlers()
        self.showMaximized()

    def build_handlers(self):
        self.pushButton_add_image.clicked.connect(self.click_add_image)
        # self.pushButton_del_image.clicked.connect(self.click_del_image)
        self.pushButton_preview.clicked.connect(self.print_image_preview)
        self.pushButton_add_accessory.clicked.connect(self.click_add_accessory)

        self.pushButton_folder.clicked.connect(self.select_folder_accessories)
        self.pushButton_generate.clicked.connect(self.generate)

    @staticmethod
    def create_cache():
        try:
            os.mkdir(CACHE_DIR)
        except Exception as e:
            print(e)
        try:
            os.mkdir(f"{CACHE_DIR}/accessories")
        except Exception as e:
            print(e)

    @staticmethod
    def delete_cache():
        try:
            shutil.rmtree(CACHE_DIR)
        except Exception as e:
            print(e)

    def select_folder_accessories(self):
        path_dir = QtWidgets.QFileDialog.getExistingDirectory()
        shutil.copytree(path_dir, f"{CACHE_DIR}/accessories/")

    def generate(self):
        files = os.listdir(CACHE_DIR)
        files.remove("accessories")
        files.remove(self.src_preview)
        lenf = len(files)
        for i, file in enumerate(files):
            new_dir = f"{CACHE_DIR}/{i}"
            os.mkdir(new_dir)
            drawing.generate_colours_objects_png(f"{CACHE_DIR}/{file}", new_dir, [(100, 100, 100), (255, 0, 0), (0, 255, 0), (0, 0, 255)])
        files = os.listdir(f"{CACHE_DIR}/accessories")
        print(files)
        for dir in files:
            print(dir)
            anchors = filling.find_anchors(f"{CACHE_DIR}/accessories/{dir}/{dir}.png")
            print(anchors)
            filling.make_fill(f"{CACHE_DIR}/accessories/{dir}", f"{CACHE_DIR}/accessories/{dir}/{dir}.png",
                              anchors, 10)
        os.mkdir(f"{CACHE_DIR}/result")
        merging.build_all(CACHE_DIR, f"{CACHE_DIR}/accessories", f"{CACHE_DIR}/result", {i: i for i in range(lenf)}, 4)

    def click_move_layer(self):
        direction, pos = self.sender().objectName().split("_")[1:]
        k = 1 if direction == "down" else -1
        pos = int(pos)
        new_pos = pos + k

        if new_pos < 0 or new_pos >= len(self.layers_list):
            return

        self.layers_list[pos], self.layers_list[new_pos] = self.layers_list[new_pos], self.layers_list[pos]

        self.replace_labels(pos, new_pos)

    def replace_labels(self, pos, new_pos):
        text = self.gridLayout_layers_list.itemAtPosition(pos, 0).widget().text()
        self.gridLayout_layers_list.itemAtPosition(pos, 0).widget() \
            .setText(self.gridLayout_layers_list.itemAtPosition(new_pos, 0).widget().text())
        self.gridLayout_layers_list.itemAtPosition(new_pos, 0).widget().setText(text)

    def print_image_preview(self):
        merging.create_empty_layer(src=f"{CACHE_DIR}/{self.src_preview}", size=(1000, 1000))  # bug
        layers = [item[1] for item in sorted(self.layers_list.items(), key=lambda x: x[0])]
        for i in range(len(layers)):
            merging.pre_merge(src1=f"{CACHE_DIR}/{self.src_preview}", src2=f"{CACHE_DIR}/{layers[i]}")

        self.label_image_preview.setPixmap(QPixmap(f"{CACHE_DIR}/{self.src_preview}"))

    def rename(self, name_img: str, dictionary: dict):
        if name_img in dictionary:
            dictionary[name_img] += 1
            splitted = name_img.split(".")
            return f"{'.'.join(splitted[:-1])}({self.is_exist[name_img]}).{splitted[-1]}"
        else:
            dictionary[name_img] = 0
            return name_img

    def click_add_accessory(self):
        img_path = QtWidgets.QFileDialog.getOpenFileName()[0].rstrip("/")
        print(self.accessories_data)
        if img_path:
            try:
                name_img = self.add_something(self.is_exist_accessory, f"{CACHE_DIR}/accessories", self.accessories_list, [
                    (img_path.split("/")[-1], lambda: print("click")),
                    ("edit colors", self.create_edit_colors_widget),
                    ("choose anchors", self.click_choose_anchors),
                    ("del", lambda: None)
                ], self.gridLayout_accessories_list, img_path)
                self.accessories_data[name_img] = AccessoryData(name_img)
                self.accessories_data[name_img].set_colors(DEFAULT_COLORS)
            except Exception as e:
                print(e)

    def create_edit_colors_widget(self):
        pos = int(self.sender().objectName().split("_")[-1])
        name_img = self.gridLayout_accessories_list.itemAtPosition(pos, 0).widget().text()

        self.widget_colors_accessories = EditColors(self, name_img)
        self.widget_colors_accessories.show()

    def click_add_image(self):
        img_path = QtWidgets.QFileDialog.getOpenFileName()[0].rstrip("/")
        self.add_something(self.is_exist, CACHE_DIR, self.layers_list, [
            (img_path.split("/")[-1], lambda: print("click")),
            ("up", self.click_move_layer),
            ("down", self.click_move_layer),
            ("del", self.click_del_image)
        ], self.gridLayout_layers_list, img_path)

    def add_something(self, dictionary: dict, path: str, list_something: dict, list_names_buttons: list[tuple],
                      grid_layer, img_path):
        # img_path = QtWidgets.QFileDialog.getOpenFileName()[0].rstrip("/")
        name_img = img_path.split("/")[-1]
        print(self.gridLayout_layers_list.count())
        # self.gridLayout_layers_list.addWidget(QtWidgets.QLabel(text=name_img), 0, 0)
        if img_path:
            name_img = self.rename(name_img, dictionary)
            try:
                shutil.copy(img_path, f"{path}/{name_img}")
            except Exception as e:
                print(e)
            pos = len(list_something)
            i = 0
            for name, func in list_names_buttons:
                button = QPushButton(name)
                button.setObjectName(f"pb_{name}_{pos}")
                button.clicked.connect(func)
                grid_layer.addWidget(button, pos, i)
                i += 1

            list_something[pos] = name_img
            return name_img

    def click_choose_anchors(self):
        pos = int(self.sender().objectName().split("_")[-1])
        name_img = self.gridLayout_accessories_list.itemAtPosition(pos, 0).widget().text()

        self.widget_choose_anchors = SetupAnchors(self, f"{CACHE_DIR}/accessories/{name_img}", name_img)

        self.widget_choose_anchors.show()

    def click_del_image(self):
        pos = int(self.sender().objectName().split("_")[-1])
        last = len(self.layers_list) - 1
        for i in range(pos + 1, last + 1):
            self.layers_list[i - 1], self.layers_list[i] = self.layers_list[i], self.layers_list[i - 1]
            self.replace_labels(i - 1, i)

        del self.layers_list[last]
        # self.gridLayout_layers_list.removeItem(self.gridLayout_layers_list.itemAt(last))
        for i in range(self.gridLayout_layers_list.columnCount()):
            self.gridLayout_layers_list.itemAtPosition(last, i).widget().deleteLater()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def main():
    app = QtWidgets.QApplication(sys.argv)
    start_window = AppStartWindow()
    start_window.show()
    sys.excepthook = except_hook
    app.exec_()


if __name__ == "__main__":
    main()
    AppStartWindow.delete_cache()
