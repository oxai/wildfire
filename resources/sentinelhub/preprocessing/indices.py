from numpy import divide, nan_to_num


def get_nbr(image):

    B08 = image[:, :, 7]
    B12 = image[:, :, 11]
    img = divide(B08 - B12, B08 + B12)
    img = nan_to_num(img)
    
    return img
