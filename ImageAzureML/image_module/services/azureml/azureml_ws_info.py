class AzureMlWsInfo(object):
    def __init__(self, input_param, output_param, global_parameters):
        self.input = input_param
        self.output = output_param
        self.global_parameters = global_parameters

    def to_dict(self):
        ws_info = {}
        ws_info['Inputs'] = self.input.to_dict()
        ws_info['Outputs'] = self.output.to_dict()
        ws_info['GlobalParameters'] = self.global_parameters
        return ws_info
