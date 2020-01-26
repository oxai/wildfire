def stretch(val, minval, maxval): return (val - min) / (max - min)

BLACK = [0.0, 0.0, 0.0]
WHITE = [1.0, 1.0, 1.0]
RED = [0.9, 0.1, 0.1]
YELLOW = [0.9, 0.9, 0.1]
GREEN = [0.1, 0.9, 0.1]

def vis_natural_colors(ee_product, image, vis_params): 
    B02 = get_band(ee_product,image,'B02')
    B03 = get_band(ee_product,image,'B03')
    B04 = get_band(ee_product,image,'B04')
    return [stretch(3.1 * B04,0.05,0.9), stretch(3 * B03,0.05,0.9), stretch(3.0 * B02,0.05,0.9)];

def vis_enhanced_natural_colors(ee_product, image, vis_params): 
    B02 = get_band(ee_product,image,'B02')
    B03 = get_band(ee_product,image,'B03')
    B04 = get_band(ee_product,image,'B04')
    return [stretch((3.1 * B04 + 0.1 * B05),0.05,0.9), stretch((3 * B03 + 0.15 * B08),0.05,0.9), stretch(3 * B02,0.05,0.9)];

def vis_nirswir_color(ee_product, image, vis_params): 
    B02 = get_band(ee_product,image,'B02')
    B08 = get_band(ee_product,image,'B08')
    B12 = get_band(ee_product,image,'B12')
    return [stretch(2.6 * B12,0.05,0.9), stretch(1.9 * B08,0.05,0.9), stretch(2.7 * B02,0.05,0.9)]

def vis_panband(ee_product, image, vis_params): 
    B08 = get_band(ee_product,image,'B08')
    return [stretch(B08,0.01,0.99),stretch(B08,0.01,0.99),stretch(B08,0.01,0.99)]

def vis_natural_nirswirmix(ee_product, image, vis_params): 
    B02 = get_band(ee_product,image,'B02')
    B03 = get_band(ee_product,image,'B03')
    B04 = get_band(ee_product,image,'B04')
    B08 = get_band(ee_product,image,'B08')
    B12 = get_band(ee_product,image,'B12')
    return [stretch((2.1 * B04 + 0.5 * B12),0.01,0.99), stretch((2.2 * B03 + 0.5 * B08),0.01,0.99), stretch(3.2 * B02,0.01,0.99)]

def vis_pan_tinted_green(ee_product, image, vis_params): 
    B08 = get_band(ee_product,image,'B08')
    return [B08 * 0.2, B08, B08 * 0.2]

def vis_fire10vl(ee_product, image, vis_params): 
    B02 = get_band(ee_product,image,'B02')
    B03 = get_band(ee_product,image,'B03')
    B04 = get_band(ee_product,image,'B04')
    B08 = get_band(ee_product,image,'B08')
    B12 = get_band(ee_product,image,'B12')
    return [stretch((2.1 * B04 + 0.5 * B12),0.01,0.99)+1.1, stretch((2.2 * B03 + 0.5 * B08),0.01,0.99), stretch(2.1 * B02,0.01,0.99)]

def vis_fire20vl(ee_product, image, vis_params): 
    B02 = get_band(ee_product,image,'B02')
    B03 = get_band(ee_product,image,'B03')
    B04 = get_band(ee_product,image,'B04')
    B08 = get_band(ee_product,image,'B08')
    B12 = get_band(ee_product,image,'B12')
    return [stretch((2.1 * B04 + 0.5 * B12),0.01,0.99)+1.1, stretch((2.2 * B03 + 0.5 * B08),0.01,0.99)+0.5, stretch(2.1 * B02,0.01,0.99)]

def vis_fire(ee_product,image,vis_params):
    sensitivity = 1.0 # Increase sensitivity for more possible fires and more wrong indications
    B11 = get_band(ee_product,image,'B11')
    B12 = get_band(ee_product,image,'B12')
    some_fire_bool = (B11 + B12) > (1.0 / sensitivity)
    lots_fire_bool = (B11 + B12) > (2.0 / sensitivity)
    some_fire_array = vis_fire10vl(ee_product,image,vis_params)
    lots_fire_array = vis_fire20vl(ee_product,image,vis_params)
    no_fire_array = vis_natural_nirswirmix(ee_product,image,vis_params)
    fire_array = np.where(lot_fire_bool,lot_fire_array,some_fire_array)
    return np.where(some_fire_bool,fire_array,no_fire_array)
