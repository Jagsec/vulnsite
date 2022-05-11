# This file has all the functions related to file uploading for profile images and challenge files

from werkzeug.utils import secure_filename
from os import path, remove
from interface import app

#This functions is used mainly for uploading files for challenges
def fileUpload(form_field, file_path):
    file = form_field.data
    filename = secure_filename(file.filename)
    file_dir = path.join(path.dirname(app.instance_path), 'interface/static/', file_path, filename)
    file.save(file_dir) 
    return file_path + filename

#This functions is used to edit a challenge file or profile picture since it has to erase an existing file
def editUpload(form_field, model_field, file_path):
    file = form_field.data
    filename = secure_filename(file.filename)
    file_dir = path.join(path.dirname(app.instance_path), 'interface/static/', file_path, filename)
    if model_field:
        rm_dir = path.join(path.dirname(app.instance_path), 'interface/static/', str(model_field))
        remove(rm_dir)
    file.save(file_dir)
    return file_path + filename

#This function is used to delete files without replacing them
def removeFile(model_field):
    rm_dir = path.join(path.dirname(app.instance_path), 'interface/static/', str(model_field))
    remove(rm_dir)
    return None 

