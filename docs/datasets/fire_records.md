# Ground Truth / Label Datasets

To label sattelite images as positive or negative (containing or not containing a wildfire) we needed a dataset detailing the occurence of wildfires.
At a minimum, such a dataset must give a time and a place at which there is a wildfire, but some datasets include shape files and more.

Below I outline some of the datasets we have considered, and whether or not they were suitable.


## FIRMS / MODIS + VIIRS

FIRMS (or Fire Information Resource Management System) is a NASA service for sharing information about active fire data.
The service uses data from images collected by the instruments: MODIS (Moderate Resolution Imaging Spectroradiometer) and VIIRS (Visible Infrared Imaging Radiometer Suite).

Recent data is displayed on an interactive map: https://firms.modaps.eosdis.nasa.gov/map/
We also requested data from the fire archives, to cross reference against the following source.


[## FPA FOD - 1.88 Million Wildfires - Kaggle.com] (https://www.kaggle.com/rtatman/188-million-us-wildfires)

The Fire Program Analysis fire-occurence database (FPA FOD) records US wildfires from 1992 to 2015 and is [available to download on kaggle.com](https://www.kaggle.com/rtatman/188-million-us-wildfires).

It contains a lot of data about each fire including date of discovery, date of containment, location (lat/long), prediction of fires cause and the size of the fire. 

The original data was collected from a variety of "federal, state, and local" reporting systems within the US. Because of the nature of their collection, we expect the reported wildfires in this database to have a much loewr false positive rate than sattelite and heuristic based methods.


[### Cal Fire]()

The California Department of Forestry and Fire Protection provides a database of fires in California[(find a csv at the bottom of this page)] ().

**Where does the data come from?**

The database gives locations as Zip codes and provides other data (acres burned, cause, fire type).
