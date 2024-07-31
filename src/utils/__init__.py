import random
import string
import hashlib
import os

def random_hash(len=10):
  random_str = "".join(random.choices(string.ascii_letters + string.digits, k=len))
  hash_obj = hashlib.sha256(random_str.encode("utf-8"))
  return hash_obj.hexdigest()

def get_project_root_path():
  utils_dir = os.path.dirname(os.path.abspath(__file__))
  utils_dir_ar = utils_dir.split(os.path.sep)
  utils_dir_ar.pop()
  utils_dir_ar.pop()
  return "{}".format(os.path.sep).join(utils_dir_ar)
