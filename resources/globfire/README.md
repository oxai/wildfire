## GlobFire Data Loader

#### Citation for the GlobFire data source
Artés Vivancos, Tomàs; San-Miguel-Ayanz, Jesús (2018): Global Wildfire Database for GWIS. PANGAEA, https://doi.org/10.1594/PANGAEA.895835, 
	Supplement to: Artés Vivancos, Tomàs; Oom, Duarte; de Rigo, Daniele; Houston Durrant, Tracy; Maianti, Pieralberto; Libertá, Giorgio; San-Miguel-Ayanz, Jesús (2019): A global wildfire dataset for the analysis of fire regimes and fire behaviour. Scientific Data, 6(1), https://doi.org/10.1038/s41597-019-0312-2


## Setup

To use the GlobFire downloader, download shape files containing GlobFire records for a given year and month from the urls listed in

`resources/globfire/data_dir/Artes-Vivancos_San-Miguel_2018/datasets/ESRI-GIS_GWIS_wildfire.tab`

Place the unzipped shape file folders under `resources/globfire/data_dir/MODIS_BA_GLOBAL` so that the `GlobFireDataLoader` will be able to find them.

## Download satellite images corresponding to GlobFire records
```python resources/globfire/data_loader.py sentinel 2 l1c -z 13 -min <min fire duration to download> -max <max fire duration to download> --dir <directory to store the downloaded images> -lim```

If you want to download evolution of the fire, remove the `-lim` option.

## Show the downloaded images
```python resources/globfire/show_fires.py sentinel 2 l1c <directory containing the downloaded tiff files>```
