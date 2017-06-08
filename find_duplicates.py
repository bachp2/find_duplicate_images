#!/usr/bin/env python

import os, sys
import imagehash
import argparse
from PIL import Image #update to 3.6.1 to run properly
from PyQt4 import QtGui, QtCore 

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

  parser = argparse.ArgumentParser(description='find duplicate images in a specified directory')

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

  ext = [".png", ".jpg", ".jpeg", ".bmp", ".gif"] #file extensions
  images = {} #store every images of directory, group images with similar hash into the same list

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
  class Window(QtGui.QMainWindow):
  def __init__(self):
    super(Window,self).__init__()
    self.resize(500,350)
    self.setWindowTitle("find-image-duplicates")
    self.setWindowIcon(QtGui.QIcon('logo.png'))
    listWidget = QtGui.QListWidget(self)
    self.listWidget.setViewMode(QtGui.QListView.IconMode)
    
  def home(self):
    #button
    btn = QtGui.QPushButton("bulk delete", self)
    btn.clicked.connect(self.delete)
    btn.resize(btn.sizeHint())
    btn.move(400,300)
    for key, img_list in img_set.items():
      for i in img_list:
        item = QtGui.QListWidgetItem()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(i)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon)
        self.listWidget.addItem(item)
    self.show()
  
  def delete(self):
    print("checked!!")

  def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    GUI.home()
    sys.exit(app.exec_())
    #adds item to ListView

  

  
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
  else: 
    print("no duplicates found")
    print("done in {0:.2f}s".format(time.time() - start))
    quit()

