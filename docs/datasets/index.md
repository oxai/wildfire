# Ground Truth / Label Datasets

To label satellite images as positive or negative (containing or not containing a wildfire) we needed a dataset detailing the occurrence of wildfires.
At a minimum, such a dataset must give a time and a place at which there is a wildfire, but some datasets include shape files and more.

Below I outline some of the datasets we have considered, and whether or not they were suitable.


## FIRMS / MODIS + VIIRS

FIRMS (or Fire Information Resource Management System) is a NASA service for sharing information about active fire data.
The service uses data from images collected by the instruments: MODIS (Moderate Resolution Imaging Spectroradiometer) and VIIRS (Visible Infrared Imaging Radiometer Suite).

Recent data is displayed on an interactive map: https://firms.modaps.eosdis.nasa.gov/map/
We also requested data from the fire archives, to cross reference against the following source.


## FPA FOD - 1.88 Million Wildfires - Kaggle.com https://www.kaggle.com/rtatman/188-million-us-wildfires

The Fire Program Analysis fire-occurrence database (FPA FOD) records US wildfires from 1992 to 2015 and is [available to download on kaggle.com](https://www.kaggle.com/rtatman/188-million-us-wildfires).

It contains a lot of data about each fire including date of discovery, date of containment, location (lat/long), prediction of fires cause and the size of the fire. 

The original data was collected from a variety of "federal, state, and local" reporting systems within the US. Because of the nature of their collection, we expect the reported wildfires in this database to have a much loewr false positive rate than sattelite and heuristic based methods.


### Cal Fire

The California Department of Forestry and Fire Protection provides a database of fires in California.

The database gives locations as Zip codes and provides other data (acres burned, cause, fire type).

A dataset is available [here](https://www.fire.ca.gov/incidents/) but more detailed data can be acquired by contacting the authors.

**Remote Sensing Datasets**
Remote sensings datasets are those formed by automatically processing satellite images to detect fires. The two most commonly used algorithms for automatically detection are called MODIS and VIIRS algorithms, named after the satellite instruments on which they were designed to work. (See (/wildfire/satellites).) The MODIS instrument (and, hence, algorithm) is much older and served as the basis for many following developments in heuristic-based fire detection, including VIIRS. Both are based on successively applying a number of heuristics to various bands to classify the type of land under each pixel. The list of possible output classes are shown in the following tables:


**MODIS classes**

|Pixel	Class | Definition |
|------------|-------------------|
|0 |    not processed   |
|1 |    cloud           |
|2 |    fire            |
|3 |    non-fire        |
|3 |    unknown         |


**VIIRS classes**

|Pixel	Class | Definition |
|--------------|-----------------|
|0 |    not	processed                   |
|1 |    bowtie deletion                 |
|2 |    sun	glint                       |
|3 |    water                           |
|4 |    cloud                           |
|5 |    land                            |
|6 |    unclassified                    |
|7 |    low	confidence fire	pixel       |
|8 |    nominal	confidence fire	pixel   |
|9 |    high confidence	fire pixel      |


Generally, these heuristics work by converting the information in a satellite image back into physical quantities, e.g. reflectance, and then thresholding this quantity. The pixel values in the satellite image (which are sometimes called digital numbers in geography literature) were originally calculated as by well-known analytic functions of a scalar physical quantity, so they can be recovered by inverting these functions. For example, one step in the VIIRS algorithm is to compute the reflectance corresponding to the I5 band, then use this reflectance to compute an estimate of brightness temperature, and if this estimate is over 285K, then classify as an area obscured by cloud. The details of which value to threshold and exactly what thresholds to use have been a subject of study since the introduction of these algorithms. Detailed information on MODIS and VIIRS algorithms can be found through the following links: [MODIS](https://modis.gsfc.nasa.gov/data/atbd/atbd_mod08.pdf) and [VIIRS](https://viirsland.gsfc.nasa.gov/PDF/VIIRS_activefire_375m_ATBD.pdf).

**GlobFire**

GlobFire begins with the MODIS detection algorithm and then applies a second step of clustering high-confidence fire pixels. This clustering stage takes place of a number of successive time steps, with each time-step corresponding to a set of satellite images taken at the same time on the same day. It also uses the concept of a fire event, defined as a set of fire-classified pixels that are touching spatially and separated by no more than 5 days temporally. At each time-step, an r-tree is computed for all fire events (a type of 2d hierarchical clustering). Then a distance matrix is computed, specifying the distance from each fire-event at this time-step with each fire-event of the previous time-step. After all time-steps, all of these distance matrix are combined into a single distance matrix, which specifies the distance between all pairs of fire-events that are one time step apart. This distance matrix is then fed to a clustering algorithm (DBSCAN), and the resulting clusters are stored as wildfires in the GlobFire dataset. The paper describing the dataset is available [here](https://www.nature.com/articles/s41597-019-0312-2).
