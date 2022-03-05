from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QLabel, QPushButton, QGraphicsView, QGraphicsScene, QGraphicsRectItem,QGraphicsPixmapItem


class SetupAnchors(QtWidgets.QWidget):
    def __init__(self, parent, img_path: str, name_img: str):
        super().__init__()
        self.img_path = img_path
        self.name_img = name_img
        self.points = []
        self.coords = set()
        self.parent = parent

        self.setup_ui(img_path)

    def click_cancel(self):
        if len(self.points) == 0:
            return

        rect, coord = self.points.pop()
        self.scene.removeItem(rect)
        self.coords.remove(coord)

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        pass

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.parent.accessories_data[self.name_img].set_anchors(list(self.coords))

    def scene_mouse_mouse_press(self, a0: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        print(a0.scenePos().toPoint())

        self.set_point(a0.scenePos().toPoint().x(), a0.scenePos().toPoint().y())

    def set_point(self, x, y):
        if (x, y) in self.coords:
            return

        rect = QGraphicsRectItem(x - 1, y - 1, 3, 3)
        rect.setBrush(QColor(255, 0, 0))
        self.coords.add((x, y))
        self.points.append((rect, (x, y)))
        self.scene.addItem(rect)

    def setup_ui(self, img_path):
        self.setObjectName("Form")
        img = QPixmap(img_path)
        w, h = img.size().width(), img.size().height()
        print(w, h)
        self.resize(w + 50, h + 100)

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        label = QLabel("Select the pixels inside the areas you want to paint over")
        self.gridLayout.addWidget(label, 0, 0)
        self.button = QPushButton("Cancel")
        self.button.setObjectName("pb_cancel")
        self.button.clicked.connect(self.click_cancel)
        self.gridLayout.addWidget(self.button, 0, 1)
        self.img_pic = QGraphicsView()
        self.img_pic.setObjectName("picture")
        self.scene = QGraphicsScene()
        self.scene.addItem(QGraphicsPixmapItem(img))
        # self.scene.addPixmap(img)
        self.img_pic.setScene(self.scene)
        self.scene.mousePressEvent = self.scene_mouse_mouse_press
        # self.img_pic.mousePressEvent = self.test


        # scene.removeItem(rect)
        self.gridLayout.addWidget(self.img_pic, 1, 0, -1, -1)
