import tornado.web
import os
import magic_pdf.model as model_config
import zipfile
import shutil

from loguru import logger
from magic_pdf.pipe.UNIPipe import UNIPipe
from magic_pdf.rw.DiskReaderWriter import DiskReaderWriter
from tornado.web import HTTPError
from utils import random_hash, get_project_root_path

model_config.__use_inside_model__ = True

jso_useful_key = {"_pdf_type": "", "model_list": []}
project_root = get_project_root_path()
out_dir = os.path.join(project_root, "outs")

class Pdf2Md(tornado.web.RequestHandler):
  def post(self):
    hash_path = random_hash()
    current_dir = os.path.join(out_dir, hash_path)
    try:
      file = self.request.files["file"][0]
      pdf_bytes = file.body
      filename = file.filename
      
      local_image_dir = os.path.join(current_dir, "images")
      image_dir = str(os.path.basename(local_image_dir))
      image_writer = DiskReaderWriter(local_image_dir)
      pipe = UNIPipe(pdf_bytes, jso_useful_key, image_writer)
      pipe.pipe_classify()
      if model_config.__use_inside_model__:
        pipe.pipe_analyze()
      else:
        raise ValueError("need model list input")
      pipe.pipe_parse()
      md_content = pipe.pipe_mk_markdown(image_dir, drop_mode="none")
      with open("{}".format(os.path.sep).join([current_dir, f"{filename}.md"]), "w", encoding="utf-8") as f:
        f.write(md_content)
      zip_name = os.path.join(out_dir, "{}.zip".format(hash_path))
      with zipfile.ZipFile(zip_name, "w") as zipf:
        for root, dir, files in os.walk(current_dir):
          for file in files:
            file_path = os.path.join(root, file)
            zipf.write(file_path, os.path.relpath(file_path, current_dir))

      with open(zip_name, "rb") as file:
        self.set_header("Content-Type", "application/octet-stream")
        self.set_header("Content-Disposition", "attachment; filename={}.zip".format(hash_path))
        self.write(file.read())
        self.finish()
    except Exception as e:
      logger.exception(e)
      raise HTTPError(500)
    shutil.rmtree(current_dir)
    os.remove(os.path.join(out_dir, "{}.zip".format(hash_path)))
