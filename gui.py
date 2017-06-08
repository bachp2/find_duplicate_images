import sys
from PyQt4 import QtGui, QtCore

class Window(QtGui.QMainWindow):
	def __init__(self):
		super(Window,self).__init__()
		self.resize(500,350)
		self.setWindowTitle("find-image-duplicates")
		self.setWindowIcon(QtGui.QIcon('logo.png'))
		list = QtGui.QListView(self)
	def home(self):
		btn = QtGui.QPushButton("Delete", self)
		btn.clicked.connect(self.delete)
		btn.resize(btn.sizeHint())
		btn.move(400,300)
		self.show()
	def delete(self):
		print("checked!!")

def run():
	app = QtGui.QApplication(sys.argv)
	GUI = Window()
	GUI.show()
	sys.exit(app.exec_())