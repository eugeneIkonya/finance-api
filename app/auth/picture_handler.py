import os
from PIL import Image
from flask import current_app, url_for

def add_profile_pic(pic_upload,username):
    filename = pic_upload.filename
    extension = filename.split('.')[-1]
    storage_filename = str(username)+'pic.'+extension
    filepath = os.path.join(current_app.root_path, 'static/images/profile_pictures',storage_filename)

    output_size = (200,200)

    picture = Image.open(pic_upload)
    picture.thumbnail(output_size)
    picture.save(filepath)

    return storage_filename