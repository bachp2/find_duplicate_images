import os, imagehash, argparse
from PIL import Image
from collections import namedtuple

# code example taken from (with minor changes):
# http://stackoverflow.com/questions/22635675/use-dictionary-for-python-argparse
class DictAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        methods={
          'ahash': imagehash.average_hash
          'phash': imagehash.phash
          'dhash': imagehash.dhash
          'whash-haar': imagehash.whash
          'whash-db4': lambda img: imagehash.whash(img, mode='db4')
          }
        setattr(namespace, self.dest, methods.get(values))

def rename_duplicate(file_name, index):
  temp = str(file_name).split('.')
  return temp[0] + int(index) + temp[1]
  
if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='find duplicate images in a directory')
  parser.add_argument('path', type=String,
                      help='path to the directory')
  
  parser.add_argument('--hashing', '-h', 
                      action=DictAction, 
                      choices=['ahash','phash','dhash','whash-haar','whash-db4'],
                      default='dhash', 
                      help='method of image hashing')
  args = parser.parse_args()
  ext = [".png", ".jpg", ".jpeg", ".bmp", ".gif"] #file extensions
  images = {}
  for root, dirs, files in os.walk(args.path):
    for file in files:
        if file.endswith(tuple(ext)):
             path_to_file = os.path.join(root, file)
             imghash = args.hashing(Image.open(path_to_file))
             images.setdefault(imghash, []).append(path_to_file)

  for key, img_list in images
    if img_list.__len__() > 1:
      length = img_list.__len__()
      print("    hash: {}".format(key))
      print("    {} similar images:".format(length))
      div = ["├──"] * (length - 1) + ["└──"]
      for output in list(zip(div, img_list)):
        print("    {} {}".format(*output))
