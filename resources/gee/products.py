EE_PRODUCTS = {
    'landsat': {
        '8': {
            'raw': {
                'display': 'Landsat 8 Raw Scenes',
                'collection': 'LANDSAT/LC08/C01/T1',
                'index': None,
                'bands': ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11'],
                'vis_params': {
                    'bands': ['B4', 'B3', 'B2'],
                    'min': 0.0,
                    'max': 30000.0,
                },
                'start_date': '2013-04-01',
                'end_date': None  # to present
            },
            'surface': {
                'display': 'Surface Reflectance',
                'collection': 'LANDSAT/LC08/C01/T1_SR',
                'index': None,
                'bands': ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11'],
                'vis_params': {
                    'bands': ['B4', 'B3', 'B2'],
                    'min': 0,
                    'max': 3000,
                    'gamma': 1.4,
                },
                'cloud_mask': 'mask_l8_sr',
                'start_date': '2013-04-01',
                'end_date': None  # to present
            },
            'ndvi': {
                'display': '8-day Normalized Difference Vegetation (NDVI)',
                'collection': 'LANDSAT/LC08/C01/T1_8DAY_NDVI',
                'index': 'NDVI',
                'vis_params': {
                    'min': 0.0,
                    'max': 1.0,
                    'palette': [
                        'FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163', '99B718', '74A901',
                        '66A000', '529400', '3E8601', '207401', '056201', '004C00', '023B01',
                        '012E01', '011D01', '011301'
                    ],
                },
                'start_date': '2013-04-01',
                'end_date': None  # to present
            },
            'ndsi': {
                'display': '8-day Normalized Difference Snow Index (NDSI)',
                'collection': 'LANDSAT/LC08/C01/T1_8DAY_NDSI',
                'index': 'NDSI',
                'vis_params': {
                    'palette': ['000088', '0000FF', '8888FF', 'FFFFFF'],
                },
                'start_date': '2013-04-01',
                'end_date': None  # to present
            },
        }
    }
}
