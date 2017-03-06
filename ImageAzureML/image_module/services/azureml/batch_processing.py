import urllib2
import json
from flask import current_app as app
from image_module.services.azureml.azureml_ws_info import AzureMlWsInfo
from image_module.services.azureml.azureml_file_param import AzureMlFileParam
from image_module.services.blob_storage.file_management import upload_file_toblob

def init_job_batch(dataset_file, centroids, iterations):
    upload_file_toblob(dataset_file, 'input_imagedatablob.csv')
    input_param = AzureMlFileParam('input_image', 'input_imagedatablob.csv')
    output_param = AzureMlFileParam('output_image', 'output_imagedatablob.csv')
    ws_params = {
        'Number of Centroids': centroids,
        'Iterations': iterations
    }

    azureml_ws = AzureMlWsInfo(input_param, output_param, ws_params)
    body = str.encode(json.dumps(azureml_ws.to_dict()))
    headers = {
        'Content-Type':'application/json',
        'Authorization':('Bearer ' + app.config['API_KEY'])
    }
    print 'Submitting the job...'

    req = urllib2.Request(app.config['URL_BATCH'] + '?api-version=2.0', body, headers)

    try:
        response = urllib2.urlopen(req)
    except urllib2.HTTPError, error:
        return json.loads(error.read())
    print 'Starting the job...'
    result = response.read()
    job_id = result[1:-1]
    req = urllib2.Request(
        app.config['URL_BATCH'] + '/' + job_id + '/start?api-version=2.0',
        str.encode(json.dumps({})),
        headers
    )

    try:
        response = urllib2.urlopen(req)
    except urllib2.HTTPError, error:
        return json.loads(error.read())

    return job_id

def get_job_status(job_id):
    url_status = app.config['URL_BATCH'] + '/' + job_id + '?api-version=2.0'
    print 'Checking the job status...'
    req = urllib2.Request(url_status, headers={'Authorization':('Bearer ' + app.config['API_KEY'])})

    try:
        response = urllib2.urlopen(req)
    except urllib2.HTTPError, error:
        return json.loads(error.read())

    return response.read()
