from flask import Blueprint, render_template, request, jsonify
from image_module.imagelib.image_processing import dataset2image
from image_module.services.azureml.batch_processing import init_job_batch, get_job_status
from image_module.utils import static_files
from image_module.services.blob_storage.file_management import save_blob_tofile

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
    dataset = static_files.save_temp_file(IMAGE_MOD.static_folder, request_file)
    image = static_files.get_static_temp_for(IMAGE_MOD.static_folder, 'png')
    dataset2image(dataset.path, image.path, 160)
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
    image = static_files.get_static_temp_for(IMAGE_MOD.static_folder, 'png')
    dataset = static_files.get_static_temp_for(IMAGE_MOD.static_folder, 'csv')
    save_blob_tofile(data['blobUrl'], dataset.path)
    dataset2image(dataset.path, image.path, 160)
    return jsonify(image_url=static_files.get_url_static_for(image.name))
