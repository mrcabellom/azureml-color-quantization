from flask import current_app as app

class AzureBlobConnection(object):

    @staticmethod
    def get_connection_string():
        return 'DefaultEndpointsProtocol=https;AccountName={0};AccountKey={1}'.format(
            app.config['STORAGE_ACCOUNT_NAME'], app.config['STORAGE_ACCOUNT_KEY'])
