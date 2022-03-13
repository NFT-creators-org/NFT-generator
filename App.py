import sys
import os
import shutil
import time
from multiprocessing import Process

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QPushButton, QGraphicsScene, QGraphicsPixmapItem

from Ui_AppMainWindow import Ui_MainWindow
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

        self.layers_list = dict()  # {'pos at grid layout': 'name_img'}
        self.layers_preview = dict()  # {'name_img': QGraphicsPixmapItem}
        self.colors_layers = dict()  # {'name': [(r, g, b), ...]}
        self.is_exist = dict()  # {'name_img': 'name(int).png'}

        self.accessories_list = dict()  # {'pos at grid layout': 'name_accessory'}
        self.is_exist_accessory = dict()  # {'name_accessory': 'name(int).png'}
        self.accessories_data = dict()  # {'name': AccessoryData}

        AppStartWindow.create_cache()
        self.src_preview = "preview_for_app.png"
        self.result_folder = "./Result"
        self.scene_preview = QGraphicsScene()
        self.graphicsView_preview.setScene(self.scene_preview)
        # self.print_image_preview()
        self.build_handlers()
        self.showMaximized()

    def build_handlers(self):
        self.pushButton_add_image.clicked.connect(self.click_add_image)
        # self.pushButton_del_image.clicked.connect(self.click_del_image)
        # self.pushButton_preview.clicked.connect(self.print_image_preview)
        self.pushButton_add_accessory.clicked.connect(self.click_add_accessory)

        self.pushButton_folder.clicked.connect(self.select_folder_result)
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

    def select_folder_result(self):
        path_dir = QtWidgets.QFileDialog.getExistingDirectory()
        self.result_folder = path_dir.rstrip("/")
        self.label_folder_name.setText(path_dir)

    def select_folder_accessories(self):
        path_dir = QtWidgets.QFileDialog.getExistingDirectory()
        shutil.copytree(path_dir, f"{CACHE_DIR}/accessories/")

    def generate(self):
        time_start = time.time()
        lenf = len(self.colors_layers)
        processes = []
        for i, file in enumerate(self.colors_layers.keys()):
            new_dir = f"{CACHE_DIR}/{i}"
            try:
                os.mkdir(new_dir)
            except:
                pass
            processes.append(Process(target=drawing.generate_colours_objects_png,
                                args=(f"{CACHE_DIR}/{file}", new_dir, self.colors_layers[file])))
            # drawing.generate_colours_objects_png(f"{CACHE_DIR}/{file}", new_dir, self.colors_layers[file])  # bug - done!

        for i in processes:
            i.start()
        for i in processes:
            i.join()

        time_finish = time.time()
        print("proc gen col: %s", (time_finish - time_start))

        num = 0
        print(f"{self.accessories_data = }")
        processes = []
        for name_img in self.accessories_data:
            accessory = self.accessories_data[name_img]

            try:
                os.mkdir(f"{CACHE_DIR}/accessories/{num}")
            except Exception as e:
                print(e)

            processes.append(Process(target=filling.make_fill,
                                args=(f"{CACHE_DIR}/accessories/{num}",
                                      f"{CACHE_DIR}/accessories/{name_img}",
                                      [[i] for i in accessory.anchors],
                                      self.spinBox_count_images.value(),
                                      accessory.colors)))
            num += 1

            # filling.make_fill(path_out=f"{CACHE_DIR}/accessories/{num}",
            #                   path_standart_pic=f"{CACHE_DIR}/accessories/{name_img}",
            #                   anchors=[[i] for i in accessory.anchors],
            #                   count=self.spinBox_count_images.value(),
            #                   colors=accessory.colors)

        # for dir in files:
        #     print(dir)
        #     anchors = filling.find_anchors(f"{CACHE_DIR}/accessories/{dir}/{dir}.png")
        #     print(anchors)
        #     filling.make_fill(f"{CACHE_DIR}/accessories/{dir}", f"{CACHE_DIR}/accessories/{dir}/{dir}.png",
        #                       anchors, 10)

        for i in processes:
            i.start()
        for i in processes:
            i.join()

        time_finish = time.time()
        print("proc mak fil: %s", (time_finish - time_start))

        try:
            os.mkdir(self.result_folder)
        except:
            pass
        merging.build_all(CACHE_DIR, f"{CACHE_DIR}/accessories", self.result_folder,
                          {i: i for i in range(lenf)}, self.spinBox_count_images.value())

        time_finish = time.time()
        print("process time: %s" % (time_finish - time_start))

    def click_move_layer(self):
        print(self.layers_preview)
        print(self.layers_list)
        print(self.scene_preview)
        direction, pos = self.sender().objectName().split("_")[1:]
        k = 1 if direction == "down" else -1
        pos = int(pos)
        new_pos = pos + k

        if new_pos < 0 or new_pos >= len(self.layers_list):
            return

        self.layers_list[pos], self.layers_list[new_pos] = self.layers_list[new_pos], self.layers_list[pos]
        self.replace_labels(self.gridLayout_layers_list, pos, new_pos)

        self.replace_zth(pos, new_pos)

    def replace_zth(self, pos, new_pos):
        name1 = self.layers_list[pos]
        name2 = self.layers_list[new_pos]
        z = self.layers_preview[name1].zValue()
        self.layers_preview[name1].setZValue(self.layers_preview[name2].zValue())
        self.layers_preview[name2].setZValue(z)

    def replace_labels(self, grid_layout, pos, new_pos):
        text = grid_layout.itemAtPosition(pos, 0).widget().text()
        grid_layout.itemAtPosition(pos, 0).widget() \
            .setText(grid_layout.itemAtPosition(new_pos, 0).widget().text())
        grid_layout.itemAtPosition(new_pos, 0).widget().setText(text)

    def print_image_preview(self):
        merging.create_empty_layer(src=f"{CACHE_DIR}/{self.src_preview}", size=(1000, 1000))  # bug
        layers = [item[1] for item in sorted(self.layers_list.items(), key=lambda x: x[0])]
        for i in range(len(layers)):
            merging.pre_merge(src1=f"{CACHE_DIR}/{self.src_preview}", src2=f"{CACHE_DIR}/{layers[i]}")

        self.label_image_preview.setPixmap(QPixmap(f"{CACHE_DIR}/{self.src_preview}"))  # bug
        # self.graphicsView_preview

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
                name_img = self.add_something(self.is_exist_accessory, f"{CACHE_DIR}/accessories",
                                              self.accessories_list, [
                    (img_path.split("/")[-1], lambda: print("click")),
                    ("edit colors", self.create_edit_colors_widget),
                    ("choose anchors", self.click_choose_anchors),
                    ("del", self.click_del_accessory)
                ], self.gridLayout_accessories_list, img_path)
                self.accessories_data[name_img] = AccessoryData(name_img)
                self.accessories_data[name_img].set_colors(DEFAULT_COLORS)
            except Exception as e:
                print(e)

    def create_edit_colors_widget(self):
        pos = int(self.sender().objectName().split("_")[-1])
        name_img = self.gridLayout_accessories_list.itemAtPosition(pos, 0).widget().text()

        self.widget_colors_accessories = EditColors(self, name_img, is_accessory=True)
        self.widget_colors_accessories.show()

    def edit_colors_image(self):
        pos = int(self.sender().objectName().split("_")[-1])
        name_img = self.gridLayout_layers_list.itemAtPosition(pos, 0).widget().text()

        self.widget_colors_accessories = EditColors(self, name_img, is_accessory=False)
        self.widget_colors_accessories.show()

    def click_add_image(self):
        img_path = QtWidgets.QFileDialog.getOpenFileName()[0].rstrip("/")
        if img_path:
            name_img = self.add_something(self.is_exist, CACHE_DIR,
                                          self.layers_list, [
                (img_path.split("/")[-1], lambda: print("click")),
                ("up", self.click_move_layer),
                ("down", self.click_move_layer),
                ("edit colors", self.edit_colors_image),
                ("del", self.click_del_image)
            ], self.gridLayout_layers_list, img_path)
            pixmap = QGraphicsPixmapItem(QPixmap(img_path))
            pixmap.setZValue(100 - len(self.layers_preview))
            self.scene_preview.addItem(pixmap)
            self.layers_preview[name_img] = pixmap
            self.colors_layers[name_img] = DEFAULT_COLORS[:]

    def add_something(self, dictionary: dict, path: str, list_something: dict, list_names_buttons: list[tuple],
                      grid_layer, img_path):
        # img_path = QtWidgets.QFileDialog.getOpenFileName()[0].rstrip("/")
        name_img = img_path.split("/")[-1]
        name_img_old = name_img
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
                name = name.replace(name_img_old, name_img)
                button = QPushButton(name)
                button.setObjectName(f"pb_{name}_{pos}")
                button.clicked.connect(func)
                grid_layer.addWidget(button, pos, i)
                i += 1

            list_something[pos] = name_img
            return name_img

    def click_del_accessory(self):
        pos = int(self.sender().objectName().split("_")[-1])
        last = len(self.accessories_list) - 1
        for i in range(pos + 1, last + 1):
            self.accessories_list[i - 1], self.accessories_list[i] = self.accessories_list[i], \
                                                                     self.accessories_list[i - 1]
            self.replace_labels(self.gridLayout_accessories_list, i - 1, i)

        del self.accessories_data[self.accessories_list[last]]
        del self.accessories_list[last]

        for i in range(self.gridLayout_accessories_list.columnCount()):
            self.gridLayout_accessories_list.itemAtPosition(last, i).widget().deleteLater()

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
            self.replace_labels(self.gridLayout_layers_list, i - 1, i)
            self.replace_zth(i - 1, i)

        self.scene_preview.removeItem(self.layers_preview[self.layers_list[last]])
        del self.colors_layers[self.layers_list[last]]
        del self.layers_preview[self.layers_list[last]]
        del self.layers_list[last]

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
