from skimage import io, color
import numpy as np
import pandas as pd
import os

def image2dataset(path_dataset, path_image):
    image = io.imread(path_image)
    if image.shape[-1] == 4:
        image = color.rgba2rgb(image)    
    image_lab = color.rgb2lab(image)
    image_lab = image_lab.reshape((image_lab.shape[0] * image_lab.shape[1], 3))
    df_image_lab = pd.DataFrame(image_lab, columns=['L*','a*', 'b*'])
    df_image_lab.to_csv(path_or_buf=path_dataset, index=False)

def dataset2image(dataset, path_image, image_size):
    dataframe = dataset if isinstance(dataset, pd.DataFrame) else pd.read_csv(dataset)
    image = dataframe.iloc[:,0:3].values.reshape((image_size[0],image_size[1],3))
    image = color.lab2rgb(image)
    io.imsave(path_image,image)

def get_image_shape(folder, image_name):
    read_path = os.path.join(folder, image_name)
    image = io.imread(read_path)
    return image.shape
