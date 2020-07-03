# Challenges

## Points to consider when applying machine learning techniques to wildfire detection and prediction
Identifying and analysing wildfire using satellite images seems to be a simple and accomplishable task. 
However, it is also a task that has to be approached with caution, especially when it is taken as a machine learning problem.
Unlike problems of classifying cats and dogs, making a false-positive or false-negative fire prediction can have far more significant consequences.
Making future predictions requires even more consideration. 

Here, we list a number of challenges, difficulties and concerns we encountered throughout the project. 
We recognise that this is not a comprehensive list, and some concerns could be relieved by comprehensive data collection. 
We do not wish to discourage any future data-driven approaches to wildfire detection and prediction - on the contrary, 
we wish to encourage continual awareness and investigation into this serious issue. 
However, we also believe in the importance of delivering accurate data and predictions to the public. 
While we fell short of accomplishing that ultimate goal,
we hope that any future endeavours will be mindful about the impact and potential risk of their research outcome, 
and hope that this page may serve as a starting point for such future pursuits.

### Quality and availability of data source
- **Consider what kind of data is available**

    One of the biggest challenges we faced during the project was finding ground truth training data. 
There are seemingly many wildfire datasets out there (see [list of public wildfire datasets](/wildfire/datasets)).
However, we soon discovered that many of the datasets (e.g. MODIS Fire Archive) themselves use remote sensing to identify wildfire, and are derived datasets rather than ground truths.
If you directly train a wildfire detection model on these datasets, it will most likely learn to approximate the algorithm (band combinations) used to derive these datasets, rather than learning to detect wildfire.

    Datasets compiled from wildfire records reported by local authorities are limited, and the ones we found either covered only a small region (e.g. Calfire) or was outdated (FPA FOD). 


- **Assess the quality and accuracy of datasets before trusting them**

    When we made a comparison between MODIS Fire Archive (detected by remote sensing) and FPA FOD (reported by local authorities), 
we found that they do not seem to align well with each other. The reason for this is unclear.
    
    We recommend validating the quality of any dataset that you plan to use before you start to train a model. Possible methods include cross-referencing datasets with other datasets or visually inspecting satellite images to see if a wildfire is locatable.


## Why we should 