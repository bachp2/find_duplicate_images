
import os
import numpy as np
import time     

'''
    Python decorator for measuring the execution time of methods
    I stole it from here : 
        https://www.andreas-jung.com/contents/a-python-decorator-for-measuring-the-execution-time-of-methods
'''
PATH = r'E:\notes_sys\4chan\memes'
ext = {".png":True,".jpg":True,".jpeg":True,".bmp":True,".gif":True} #file extensions

@profile
def os_walk_test1():
    l = []
    i = 0
    ts = time.clock()
    for root, dirs, files in os.walk(PATH):
        for file in files:
            if file.endswith(tuple(ext)):
              path_to_file = os.path.join(root, file)
              l.append(path_to_file)
    te = time.clock()
    print("files: {} {:.2f} millisec".format(i, (te-ts)*1000))

def os_walk_test():
    l = []
    i = 0
    ts = time.clock()
    for root, dirs, files in os.walk(PATH):
         for file in files:
             extension = os.path.splitext(file)[1]
             if extension in ext:
                path = os.path.join(root, file)
                l.append(path)
             i = i + 1
         break
    te = time.clock()
    print("files: {} {:.2f} millisec".format(i, (te-ts)*1000))

def os_scandir_test():
    l = []
    i = 0
    ts = time.clock()
    for entry in os.scandir(PATH):
        extension = os.path.splitext(entry.path)[1]
        if extension in ext:
            l.append(entry.path)
        i = i+1
    te = time.clock()
    print("files: {} {:.2f} millisec".format(i, (te-ts)*1000))
    


os_walk_test1()
os_scandir_test()