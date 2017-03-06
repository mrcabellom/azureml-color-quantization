from flask import current_app as app
from image_module.services.blob_storage.azure_blob_connection import AzureBlobConnection

class AzureMlFileParam(object):

    def __init__(self, alias_parameter, file_name):
        self.name_parameter = alias_parameter
        self.file_name = file_name
        self.relative_location = '/{0}/{1}'.format(
            app.config['STORAGE_CONTAINER_NAME'],
            self.file_name
        )

    def to_dict(self):
        result_dict = {}
        result_dict[self.name_parameter] = self.__get_serialize_info()
        return result_dict

    def __get_serialize_info(self):
        return {
            'ConnectionString': AzureBlobConnection.get_connection_string(),
            'RelativeLocation': self.relative_location
        }
