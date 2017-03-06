from PIL import Image
import numpy as np
import pandas as pd

def image2dataset(path):
    image = Image.open(path)
    width, height = image.size
    if width != height:
        raise ValueError('The height and width are not equals')
    array_data = np.asarray(list(image.getdata()))
    x_p = np.arange(width)
    x_array, y_array = np.meshgrid(x_p, x_p)
    n_cc = np.c_[x_array.ravel(), y_array.ravel()]
    n_image = np.append(n_cc, array_data, axis=1)
    df_image = pd.DataFrame(
        n_image,
        columns=['X', 'Y', 'R', 'G', 'B']
    ).sort(['X', 'Y'])
    df_image.reset_index(drop=True, inplace=True)
    return df_image

def dataset2image(path_dataset, path_image, image_size):
    dataframe = pd.read_csv(path_dataset)
    rgb = np.array(dataframe[['R', 'G', 'B']], dtype='uint8')
    rgb = rgb.reshape(image_size, image_size, 3)
    img = Image.fromarray(rgb)
    img = img.transpose(Image.ROTATE_270)
    img.save(path_image)
