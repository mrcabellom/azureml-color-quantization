from collections import namedtuple
import os
import uuid
from flask import url_for

def get_uuid_file_name(extension):
    return '{}{}'.format(uuid.uuid4(), extension)

def save_temp_file(folder, request_file):
    temp_file = get_uuid_file_name(os.path.splitext(request_file.filename)[1])
    save_path = os.path.join(folder, temp_file)
    request_file.save(save_path)
    named_tuple = namedtuple('TempFile', 'name path')
    return named_tuple(name=temp_file, path=save_path)

def get_static_path_for(folder, file_name):
    return os.path.join(folder, file_name)

def get_static_temp_for(folder, extension):
    temp_file = get_uuid_file_name(extension)
    named_tuple = namedtuple('TempFile', 'name path')
    return named_tuple(name=temp_file, path=os.path.join(folder, temp_file))

def get_url_static_for(file_name):
    return url_for('image.static', filename=file_name)

def get_url_static_for_files(temporal_files):
    files = []
    for x in range(0,len(temporal_files)):
        files.append(url_for('image.static', filename=temporal_files[x].name))
    return files
