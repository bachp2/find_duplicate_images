#!/usr/bin/env python

import os, sys
import imagehash
import argparse
from PIL import Image #update to 3.6.1 to run properly
from PyQt4 import QtGui, QtCore 
from gui_widget import Ui_Window
from itertools import repeat
from multiprocessing import Pool, freeze_support, Manager, Lock

class FullPaths(argparse.Action):
    """Expand user- and relative-paths"""
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, os.path.abspath(os.path.expanduser(values)))

#----------------------------------------------------------------------------------------

#Class for GUI
class Window(QtGui.QMainWindow, Ui_Window):
  try:
    _fromUtf8 = QtCore.QString.fromUtf8
  except AttributeError:
    _fromUtf8 = lambda s: s

  #sets item to path file
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

  #divider line between each group of images
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
  
  #execute function
  def run():
    app = QtGui.QApplication(sys.argv)
    #message box shows warning
    msg_box = QtGui.QMessageBox()
    msg_box.setText("Check for any false positives before deleting!")
    msg_box.setWindowTitle("Warning")
    msg_box.show()
    
    GUI = Window()
    sys.exit(app.exec_())
      #adds item to ListWidget

#----------------------------------------------------------------------------------------
 
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
        

#----------------------------------------------------------------------------------------

'''
  check if string is empty
  return true if not empty false otherwise
'''
def isNotEmpty(s):
  return bool(str(s) and str(s).strip())

def dict_get(dict, *args):
  dict.get(*args)

lock = Lock()

def hashing_image(path_to_file, func, dict):
    imghash = func(Image.open(path_to_file))
    #print(imghash)
    with lock:
      #dict.setdefault(imghash, []).append(path_to_file)
      dict[str(imghash)] = dict.get(str(imghash), []) + [path_to_file]
    #@test print(images)
    return dict


if __name__ == '__main__':
  
  freeze_support()
  pool = Pool()

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

  parser.add_argument('-r','--recursive', action='store_true',help='recursive search through sub-directories')

  args = parser.parse_args()
  #extension names
  ext = [".png", ".jpg", ".jpeg", ".bmp", ".gif"] #file extensions
  
  temp_list = []
  
  import time

  ##################################
  start = time.time()#start counting
  ##################################
  

  print("hashing images...")#signal to the console

  for root, dirs, files in os.walk(args.path):
    for file in files:
        if file.endswith(tuple(ext)):
          path_to_file = os.path.join(root, file)
          temp_list.append(path_to_file)
         #imghash = args.hashing(Image.open(path_to_file))
         #grouping images with similar hash
         #images.setdefault(imghash, []).append(path_to_file)
    if not args.recursive: break
    #stop if there is no recursive search argument

  #images = {}
  manager = Manager()
  images = manager.dict(lock=True) #store every duplicates images in the directory, then group images with similar hash into the same list
  pool.starmap(hashing_image, zip( temp_list, repeat(args.hashing), repeat(images) ) )
  pool.close()
  pool.join()
  
  print("printing output...")#finishes output to console

  #print(temp_list)
  #print(images)
  
  for k, v in images.items():
    if type(v) is not bool:
      if v.__len__() > 1:
        print(v)

  img_set = {k: v for k, v in images.items() if type(v) is not bool and v.__len__() > 1}
  #print(img_set)
  out = ""
  
  #prints list to console
  for key, img_list in img_set.items():
      out+="\n"
      length = img_list.__len__()
      out+="    hash: {}\n".format(key)
      out+="    {} similar images:\n".format(length)
      div = ["├──"] * (length - 1) + ["└──"]
      for output in list(zip(div, img_list)):
        out+="    {} {}\n".format(*output)

  if isNotEmpty(out):
    print(out)
    print()
    print("done in {0:.2f}s".format(time.time() - start))
    Window.run()
  else: 
    print("no duplicates found")
    print("done in {0:.2f}s".format(time.time() - start))
    quit()
