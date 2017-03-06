import urllib2
import json
from flask import current_app as app
from azure.storage.blob.blockblobservice import BlockBlobService

def save_blob_tofile(blob_url, filename):
    print 'Reading the result from ' + blob_url
    try:
        response = urllib2.urlopen(blob_url)
    except urllib2.HTTPError, error:
        return json.loads(error.read())
    with open(filename, 'wb') as write_file:
        write_file.write(response.read())
    return filename

def upload_file_toblob(input_file, input_blob_name):

    blob_service = BlockBlobService(
        account_name=app.config['STORAGE_ACCOUNT_NAME'],
        account_key=app.config['STORAGE_ACCOUNT_KEY']
    )
    print 'Uploading the input to blob storage...'
    blob_service.create_blob_from_path(
        app.config['STORAGE_CONTAINER_NAME'],
        input_blob_name,
        input_file
    )
