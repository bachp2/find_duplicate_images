#!/usr/bin/env python
import os
import imagehash
import argparse
from PIL import Image #update to 3.6.1 to run properly

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

  parser.add_argument('--hashing',
                      nargs='?', 
                      action=DictAction, 
                      choices=['ahash','phash','dhash','whash-haar','whash-db4'],
                      default=imagehash.dhash, 
                      help='method of image hashing')

  args = parser.parse_args()

  ext = [".png", ".jpg", ".jpeg", ".bmp", ".gif"] #file extensions
  images = {} #store every images of directory, group images with similar hash into the same list

  import time
  start_time = time.time()
  print("hasing images...")#signal to the console

  for root, dirs, files in os.walk(args.path):
    for file in files:
        if file.endswith(tuple(ext)):
             path_to_file = os.path.join(root, file)
             imghash = args.hashing(Image.open(path_to_file))
             #grouping images with similar hash
             images.setdefault(imghash, []).append(path_to_file)

  print("done in {0:.2f}s\nprinting output...".format(time.time() - start_time))#finish output to console

  for key, img_list in images.items():
    if img_list.__len__() > 1:
      print()
      length = img_list.__len__()
      print("    hash: {}".format(key))
      print("    {} similar images:".format(length))
      div = ["├──"] * (length - 1) + ["└──"]
      for output in list(zip(div, img_list)):
        print("    {} {}".format(*output))
