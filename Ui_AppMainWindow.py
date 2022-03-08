# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AppMainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1440, 900)
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")
        self.build_layers = QtWidgets.QWidget()
        self.build_layers.setObjectName("build_layers")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.build_layers)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_add_image = QtWidgets.QPushButton(self.build_layers)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_add_image.sizePolicy().hasHeightForWidth())
        self.pushButton_add_image.setSizePolicy(sizePolicy)
        self.pushButton_add_image.setObjectName("pushButton_add_image")
        self.verticalLayout_2.addWidget(self.pushButton_add_image)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.gridLayout_layers_list = QtWidgets.QGridLayout()
        self.gridLayout_layers_list.setObjectName("gridLayout_layers_list")
        self.verticalLayout_2.addLayout(self.gridLayout_layers_list)
        self.gridLayout_3.addLayout(self.verticalLayout_2, 0, 1, 1, 1)
        self.graphicsView_preview = QtWidgets.QGraphicsView(self.build_layers)
        self.graphicsView_preview.setMaximumSize(QtCore.QSize(1000, 1000))
        self.graphicsView_preview.setObjectName("graphicsView_preview")
        self.gridLayout_3.addWidget(self.graphicsView_preview, 0, 0, 1, 1)
        self.tabWidget.addTab(self.build_layers, "")
        self.tab_accessories = QtWidgets.QWidget()
        self.tab_accessories.setObjectName("tab_accessories")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_accessories)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout_accessories_list = QtWidgets.QGridLayout()
        self.gridLayout_accessories_list.setObjectName("gridLayout_accessories_list")
        self.gridLayout_2.addLayout(self.gridLayout_accessories_list, 2, 0, 1, 1)
        self.pushButton_add_accessory = QtWidgets.QPushButton(self.tab_accessories)
        self.pushButton_add_accessory.setObjectName("pushButton_add_accessory")
        self.gridLayout_2.addWidget(self.pushButton_add_accessory, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab_accessories, "")
        self.tab_generate = QtWidgets.QWidget()
        self.tab_generate.setObjectName("tab_generate")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_generate)
        self.gridLayout_4.setObjectName("gridLayout_4")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem2, 0, 2, 1, 1)
        self.spinBox_count_images = QtWidgets.QSpinBox(self.tab_generate)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.spinBox_count_images.setFont(font)
        self.spinBox_count_images.setMaximum(1000)
        self.spinBox_count_images.setProperty("value", 10)
        self.spinBox_count_images.setObjectName("spinBox_count_images")
        self.gridLayout_4.addWidget(self.spinBox_count_images, 1, 0, 1, 1)
        self.pushButton_generate = QtWidgets.QPushButton(self.tab_generate)
        self.pushButton_generate.setObjectName("pushButton_generate")
        self.gridLayout_4.addWidget(self.pushButton_generate, 2, 0, 1, 1)
        self.pushButton_folder = QtWidgets.QPushButton(self.tab_generate)
        self.pushButton_folder.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_folder.setFont(font)
        self.pushButton_folder.setCheckable(False)
        self.pushButton_folder.setAutoRepeat(False)
        self.pushButton_folder.setObjectName("pushButton_folder")
        self.gridLayout_4.addWidget(self.pushButton_folder, 0, 0, 1, 1)
        self.label_folder_name = QtWidgets.QLabel(self.tab_generate)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_folder_name.setFont(font)
        self.label_folder_name.setStyleSheet("")
        self.label_folder_name.setObjectName("label_folder_name")
        self.gridLayout_4.addWidget(self.label_folder_name, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.tab_generate)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_4.addWidget(self.label_2, 1, 1, 1, 1)
        self.tabWidget.addTab(self.tab_generate, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1440, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Generator NFT"))
        self.pushButton_add_image.setText(_translate("MainWindow", "add image"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.build_layers), _translate("MainWindow", "Build Layers"))
        self.pushButton_add_accessory.setText(_translate("MainWindow", "Add"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_accessories), _translate("MainWindow", "Accessories"))
        self.pushButton_generate.setText(_translate("MainWindow", "generate"))
        self.pushButton_folder.setText(_translate("MainWindow", "select result folder"))
        self.label_folder_name.setText(_translate("MainWindow", "Default: ./Result"))
        self.label_2.setText(_translate("MainWindow", "count generated pictures"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_generate), _translate("MainWindow", "Generate"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
