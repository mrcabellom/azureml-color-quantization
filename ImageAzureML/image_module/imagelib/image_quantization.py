import pandas as pd
from image_module.imagelib.image_processing import dataset2image
from image_module.utils import static_files

class ImageQuantization():

    def __init__(self, dataframe_path, dataframe_path_original, image_shape):
        self.__image_shape = image_shape
        self.__dataframe_path = dataframe_path
        self.__dataframe_image = pd.read_csv(dataframe_path_original)

    def generate_image_quantization(self, folder, color_quantization=False):
        image_files = []
        image = static_files.get_static_temp_for(folder, '.png')
        dataset2image(self.__dataframe_path, image.path, self.__image_shape)
        image_files.append(image)
        if color_quantization:
            labels = self.__dataframe_image['Assignments'].values
            max_clusters= labels.max()
            for x in range(0, max_clusters + 1):
                cq = self.__dataframe_image.copy()
                cq.iloc[labels !=x,:] = 0
                image_cq = static_files.get_static_temp_for(folder, '.png')
                dataset2image(cq, image_cq.path, self.__image_shape)
                image_files.append(image_cq)
        return image_files
