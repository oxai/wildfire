## Visualiser/Labeler

This tool allows users to:

* Visualise sattelite images
* Apply metrics to those images (e.g. NBR)
* Generate masks from metrics
* Combine masks between metrics
* Label images with binary masks

The tool was built primarily to compare metrics and find appropriate composite metrics. 
More detailed documentation can be found in the source code.

### Starting the Tool
The tool should be run from the top directory and initialised using the file `GUI_labeler/run_visualiser.py`. With a command of the following form `python -m tools.GUI_labeler.run_visualiser.py -m /UNLABELED_DATA_DIR/` where `DATADIR` specifies the location of their satellite images (stored as `.tif` files).

Flags can be added to choose where to labels and labelled images:
* `-i` / `--inplace`: to save labels with their images in their original location
* `-m DIR` / `--move_to DIR`: to move the labels and existing images to a new directory, which must be specified
* `-c DIR` / `--copy_to DIR`: to copy the labels and existing images to a new directory (leaving the original image in its location)


### Set-up
The range of available metrics should be specified in `GUI_labeler/config.py` and can be selected from dropdowns within the application.

The specified `UNLABELED_DATA_DIR` should contain .tif files which can be downloaded using the *INSERT HERE* tool.

### Layout

**Insert image here**

The layout of the app consists of 3 main components:
1. The toolbar
2. The main panel
3. The metric panels

#### The Metric Panels
There are a few _metric panels_ on the right-hand side. Each of these shows the current image under a different visualisation of a metric. The __drop down menu__, at the top, allows users to change between metrics to visualise. The __threshold slider__, at the right, allows users to choose a threshold value, which is used to turn the metric score of each pixel into a binary value. The __image__ that dominates the visualiser panel uses the visualiser for the metric to render and image and display it to the user. It also visualises the binary mask, taken from the metric and threshold value, and displays it over the visualisation
**insert image here**

#### The Main Panel

The main panel, on the left-hand side, displays an RGB render of the current satellite image. The rendering can also be changed with the **"Visualiser"** dropdown to use one of the metric visualizers. 

The main panel also allows users to combine the masks from the visualiser panels into a single, composite mask. The combination function to be used to generate the mask can be selected with the **"Combination function" dropdown** . For example "AND" computes a bitwise AND operation on each pixel, labelling pixels as positive only if all of the metrics agree. The **"<"** button, between the main panel and the metric panels, combines and renders the masks. This is not computed continuously and so must be pressed to update after changes to the metric masks. Finally, the **"Mask visualiser" dropdown** chooses how to represent the combination of the masks. _This does not affect the composite mask itself_ and so is only to be used for _comparison_ between metrics. 

#### The Tool Bar
The toolbar contains few features but allows you to move between images. The __"Roll"__ button allows you to select an image at random from your unlabeled directory. The __"Save mask"__ button allows you to save the binary mask/label currently in the main panel. 



