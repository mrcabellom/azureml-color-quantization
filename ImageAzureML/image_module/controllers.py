from flask import Blueprint, render_template, request, jsonify
from image_module.imagelib.image_processing import *
from image_module.imagelib.image_quantization import ImageQuantization
from image_module.services.azureml.batch_processing import init_job_batch, get_job_status
from image_module.utils import static_files
from image_module.services.blob_storage.file_management import save_blob_tofile
import asyncio

IMAGE_MOD = Blueprint('image',
                      __name__,
                      url_prefix='/image',
                      template_folder='templates',
                      static_folder='static')

@IMAGE_MOD.route('/',)
def index():
    return render_template('uploadSection.html')

@IMAGE_MOD.route('/uploaddataset', methods=['POST'])
def upload_file():
    request_file = request.files['file']
    image = static_files.save_temp_file(IMAGE_MOD.static_folder, request_file)
    dataset = static_files.get_static_temp_for(IMAGE_MOD.static_folder, '.csv')
    image2dataset(dataset.path, image.path)
    return jsonify(image_url=static_files.get_url_static_for(image.name),
                   dataset_name=dataset.name)

@IMAGE_MOD.route('/submitjob', methods=['POST'])
def submit_job():
    data = request.json
    path_dataset = static_files.get_static_path_for(IMAGE_MOD.static_folder, data['datasetName'])
    job_id = init_job_batch(path_dataset, data['centroids'], data['iterations'])
    return jsonify(job_id=job_id)

@IMAGE_MOD.route('/jobstatus', methods=['GET'])
def job_status():
    job_id = request.args.get('jobId')
    result = get_job_status(job_id)
    return result

@IMAGE_MOD.route('/filteredimage', methods=['POST'])
def filtered_image():
    data = request.json
    dataset = static_files.get_static_temp_for(IMAGE_MOD.static_folder, '.csv')
    dataset_cluster = static_files.get_static_temp_for(IMAGE_MOD.static_folder, '.csv')
    original_image_shape = get_image_shape(IMAGE_MOD.static_folder,data['originalFileName'])
    save_blob_tofile(data['blobUrl'], dataset.path)
    save_blob_tofile(data['originalUrl'], dataset_cluster.path)
    iq = ImageQuantization(dataset.path, dataset_cluster.path, original_image_shape)
    images = iq.generate_image_quantization(IMAGE_MOD.static_folder, True)
    return jsonify(images_urls=static_files.get_url_static_for_files(images))
