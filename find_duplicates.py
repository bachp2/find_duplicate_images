import os, imagehash, argparse
from PIL import Image
from collections import namedtuple

def rename_duplicate(file_name, index):
  temp = str(file_name).split('.')
  return temp[0] + int(index) + temp[1]
  
if __name__ == '__main__':
  img_struct = namedtuple("img_struct", "root file")
  parser = argparse.ArgumentParser(description='find duplicate images in a directory')
  parser.add_argument('path', type=String,
                      help='path to the directory')
  parser.add_argument('hashing', 
                      methods{
                        'ahash': imagehash.average_hash
                        'phash': imagehash.phash
                        'dhash': imagehash.dhash
                        'whash-haar': imagehash.whash
                        'whash-db4': lambda img: imagehash.whash(img, mode='db4')
                      }, 
                      type=String, 
                      help='method of image hashing')
  args = parser.parse_args()
  ext = [".png", ".jpg", ".jpeg", ".bmp", ".gif"] #file extensions
  images = {}
  for root, dirs, files in os.walk(args.path):
    for file in files:
        if file.endswith(tuple(ext)):
             path_to_file = os.path.join(root, file)
             imghash = args.hashing(Image.open(path_to_file))
             images.setdefault(imghash, []).append(img_struct(root, file))

  for key, img_list in images
    if img_list.__len__() > 1:
      i = 0
      for img in img_list:
        old_name = os.path.join(img.root, img.file)
        new_name = os.path.join(img_list[0].root, rename_duplicate(img_list[0].file, i)
        i += 1
        os.rename(old_name, new_name)
  
