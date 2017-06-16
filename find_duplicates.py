#!/usr/bin/env python

import os, sys
import imagehash
import argparse
from PIL import Image #update to 3.6.1 to run properly
from PyQt4 import QtGui, QtCore 
from gui_widget import Ui_Window

class FullPaths(argparse.Action):
    """Expand user- and relative-paths"""
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, os.path.abspath(os.path.expanduser(values)))

# code example taken from (with minor changes):
# http://stackoverflow.com/questions/22635675/use-dictionary-for-python-argparse
class DictAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        methods={
          "ahash": imagehash.average_hash,
          "phash": imagehash.phash,
          "dhash": imagehash.dhash,
          "whash-haar": imagehash.whash,
          "whash-db4": lambda img: imagehash.whash(img, mode='db4')
          }
        setattr(namespace, self.dest, methods.get(values))
        
if __name__ == '__main__':

  #descripton
  parser = argparse.ArgumentParser(description='find duplicate images in a specified directory')
  #arguments
  parser.add_argument('path',
                      action=FullPaths,
                      help='path to the directory')

  parser.add_argument('hashing',
                      nargs='?', 
                      action=DictAction, 
                      choices=['ahash','phash','dhash','whash-haar','whash-db4'],
                      default='dhash', 
                      help='method of image hashing')
  args = parser.parse_args()
  #extension names
  ext = [".png", ".jpg", ".jpeg", ".bmp", ".gif"] #file extensions
  images = {} #store every duplicates images in the directory, then group images with similar hash into the same list

  import time

  ##################################
  start = time.time()#start counting
  ##################################

  print("hashing images...")#signal to the console

  for root, dirs, files in os.walk(args.path):
    for file in files:
        if file.endswith(tuple(ext)):
             path_to_file = os.path.join(root, file)
             imghash = args.hashing(Image.open(path_to_file))
             #grouping images with similar hash
             images.setdefault(imghash, []).append(path_to_file)

  print("printing output...")#finish output to console

  img_set = {k: v for k, v in images.items() if v.__len__() > 1}
  
  out = ""
  start_time = time.time()
  
  #print list to console
  for key, img_list in img_set.items():
      out+="\n"
      length = img_list.__len__()
      out+="    hash: {}\n".format(key)
      out+="    {} similar images:\n".format(length)
      div = ["├──"] * (length - 1) + ["└──"]
      for output in list(zip(div, img_list)):
        out+="    {} {}\n".format(*output)

  try:
    _fromUtf8 = QtCore.QString.fromUtf8
  except AttributeError:
    _fromUtf8 = lambda s: s

  #Class for GUI
  class Window(QtGui.QMainWindow, Ui_Window):
    #set item to path file
    path_2_item = {}
    def __init__(self):
      super(Window,self).__init__()
      self.setupUi(self)
      self.listWidget.setViewMode(QtGui.QListView.IconMode)
      self.listWidget.setIconSize(QtCore.QSize(42,48))
      self.home()

    def home(self):
      for key, img_list in img_set.items():
        for i in range(len(img_list)):
          item = QtGui.QListWidgetItem()
          icon = QtGui.QIcon()
          icon.addPixmap(QtGui.QPixmap(_fromUtf8(img_list[i])), QtGui.QIcon.Normal, QtGui.QIcon.Off)
          item.setIcon(icon)
          item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
          item.setText(str(i+1))
          if i != 0:
            item.setCheckState(QtCore.Qt.Checked)
          else:
            item.setCheckState(QtCore.Qt.Unchecked)
          self.path_2_item[str(item)] = img_list[i]
          self.listWidget.addItem(item)
        self.divider()
      
      self.pushButton.clicked.connect(self.delete)
      self.pushButton_2.clicked.connect(QtCore.QCoreApplication.instance().quit)
      self.show()

    def delete(self):
      #BEGIN
      checked_item_index = [] # checked items, first list
      unchecked_item_index = [] # unchecked items and frames, second list
      
      #appending indexes of checked and unchecked items
      for i in range(self.listWidget.count()):
        curr = self.listWidget.item(i)
        if curr.checkState() == QtCore.Qt.Checked:
          checked_item_index.append(i)
        else: unchecked_item_index.append(i)
      #-->testalgo.py
      self.indexing_help(checked_item_index, unchecked_item_index)
      #remove checked items with correct index
      for i in checked_item_index:
        curr = self.listWidget.item(i)
        print(self.path_2_item[str(curr)])
        os.remove(self.path_2_item[str(curr)])
        self.listWidget.takeItem(i)
      #END METHOD
    def indexing_help(self, list1, list2):
      ##BEGIN
      count = 0
      for e in range(len(list1)):
        while count < len(list2):
          if list1[e] < list2[count]:
            list1[e] = count
            break
          else: count = count + 1
        if count == len(list2): list1[e] = count
      #END LOOP

    def divider(self):
      item = QtGui.QListWidgetItem()
      item.setSizeHint(QtCore.QSize(601,5))
      item.setFlags(QtCore.Qt.NoItemFlags)
      self.listWidget.addItem(item)
      frame = QtGui.QFrame()
      frame.setFrameShape(QtGui.QFrame.HLine)
      frame.setFrameShadow(QtGui.QFrame.Raised)
      frame.setLineWidth(2)
      self.listWidget.setItemWidget(item, frame)
      
    def run():
      app = QtGui.QApplication(sys.argv)
      msg_box = QtGui.QMessageBox()
      msg_box.setText("Check for any false positives before deleting!")
      msg_box.setWindowTitle("Warning")
      msg_box.show()
      GUI = Window()
      sys.exit(app.exec_())
      #adds item to ListWidget

  '''
    check if string is empty
    return true if not empty false otherwise
  '''
  def isNotEmpty(s):
    return bool(str(s) and str(s).strip())

  if isNotEmpty(out):
    print(out)
    print()
    print("done in {0:.2f}s".format(time.time() - start))
    Window.run()
  else: 
    print("no duplicates found")
    print("done in {0:.2f}s".format(time.time() - start))
    quit()