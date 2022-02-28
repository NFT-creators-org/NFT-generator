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
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
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
        self.pushButton_preview = QtWidgets.QPushButton(self.build_layers)
        self.pushButton_preview.setObjectName("pushButton_preview")
        self.verticalLayout_2.addWidget(self.pushButton_preview)
        self.gridLayout_layers_list = QtWidgets.QGridLayout()
        self.gridLayout_layers_list.setObjectName("gridLayout_layers_list")
        self.verticalLayout_2.addLayout(self.gridLayout_layers_list)
        self.gridLayout_3.addLayout(self.verticalLayout_2, 0, 1, 1, 1)
        self.label_image_preview = QtWidgets.QLabel(self.build_layers)
        self.label_image_preview.setText("")
        self.label_image_preview.setObjectName("label_image_preview")
        self.gridLayout_3.addWidget(self.label_image_preview, 0, 0, 1, 1)
        self.tabWidget.addTab(self.build_layers, "")
        self.tab_accessories = QtWidgets.QWidget()
        self.tab_accessories.setObjectName("tab_accessories")
        self.pushButton_folder = QtWidgets.QPushButton(self.tab_accessories)
        self.pushButton_folder.setGeometry(QtCore.QRect(250, 100, 131, 41))
        self.pushButton_folder.setObjectName("pushButton_folder")
        self.pushButton_generate = QtWidgets.QPushButton(self.tab_accessories)
        self.pushButton_generate.setGeometry(QtCore.QRect(280, 230, 171, 61))
        self.pushButton_generate.setObjectName("pushButton_generate")
        self.tabWidget.addTab(self.tab_accessories, "")
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
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_add_image.setText(_translate("MainWindow", "add image"))
        self.pushButton_preview.setText(_translate("MainWindow", "preview"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.build_layers), _translate("MainWindow", "Build Layers"))
        self.pushButton_folder.setText(_translate("MainWindow", "select folder"))
        self.pushButton_generate.setText(_translate("MainWindow", "generate"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_accessories), _translate("MainWindow", "Accessories"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
