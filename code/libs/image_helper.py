import os
import re
from typing import Union
from werkzeug.datastructures import FileStorage

from flask_uploads import UploadSet, IMAGES

IMAGE_SET = UploadSet("images", IMAGES)  # set name and allowed extensions

def save_image(image: FileStorage, folder:str, name: str = None) -> str:
    return IMAGE_SET.save(image, folder, name)

def get_path(filename:str, folder: str) -> str:
    return IMAGE_SET.path(filename, folder)

def find_image_any_format(filename: str, folder:str) -> Union[str, None]:
    for _format in IMAGES:
        image = "{}.{}".format(filename, _format)
        image_path = IMAGE_SET.path(filename=image, folder=folder)
        if os.path.isfile(image_path):
            return image_path
        
    return None

def _retrieve_filename(file: Union[str, FileStorage]):
    if isinstance(file, FileStorage):
        return file.filename
    return file

def is_filename_safe(file: Union[str, FileStorage]) -> bool:
    filename = _retrieve_filename(file)
    allowed_format = "|".join(IMAGES) #png|svg|jpe...|jpg
    regex = "^[a-zA-Z0-9][a-zA-Z0-9_()-\.({})".format(allowed_format)
    return re.match(regex, filename) is not None

def get_basename(file: Union[str, FileStorage]) -> str:
    filename = _retrieve_filename(file)
    return os.path.split(filename)[1]

def get_extension(file: Union[str, FileStorage]) -> str:
    filename = _retrieve_filename(file)
    return os.path.splitext(filename)[1]
