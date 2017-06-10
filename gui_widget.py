# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\gui_widget.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Window(object):
    def setupUi(self, Window):
        Window.setObjectName(_fromUtf8("Window"))
        Window.resize(484, 340)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Window.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(Window)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.listWidget = QtGui.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(40, 20, 391, 241))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(270, 270, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(360, 270, 75, 23))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        Window.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 484, 18))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        Window.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(Window)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        Window.setStatusBar(self.statusbar)

        self.retranslateUi(Window)
        QtCore.QMetaObject.connectSlotsByName(Window)

    def retranslateUi(self, Window):
        Window.setWindowTitle(_translate("Window", "find-duplicates", None))
        self.pushButton.setText(_translate("Window", "Bulk Delete!", None))
        self.pushButton_2.setText(_translate("Window", "Quit", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Window = QtGui.QMainWindow()
    ui = Ui_Window()
    ui.setupUi(Window)
    Window.show()
    sys.exit(app.exec_())

