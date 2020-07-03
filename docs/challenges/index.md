# Challenges

## Points to consider when applying machine learning techniques to wildfire detection and prediction
Identifying and analysing wildfire using satellite images seems to be a simple and accomplishable task. 
However, it is also a task that has to be approached with caution, especially when it is taken as a machine learning problem.
Unlike problems of classifying cats and dogs, making a false-positive or false-negative fire prediction can have far more significant consequences.
Making future predictions requires even more consideration. 

Here, we list a number of challenges, difficulties and concerns we encountered throughout the project. 
We recognise that this is not a comprehensive list, and some issues may be avoided by having access to data we didn't have. 
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

    Datasets compiled from wildfire records reported by local authorities are limited, and the ones we found either covered only a small region (e.g. Calfire) or was outdated (e.g. FPA FOD). 

    For real-time prediction, factors such as how frequently the data source gets updated with how much delay, what the resolution and coverage are, 
and whether it is feasible to store and process all the data are some of the engineering challenges that need to be considered. 
For instance, Sentinel 2 images are available every 5 days at the equator and every 2-3 days at middle latitudes.

- **Assess the quality and accuracy of datasets before trusting them**

    When we made a comparison between MODIS Fire Archive (detected by remote sensing) and FPA FOD (reported by local authorities), 
we found that they do not seem to align well with each other. The reason for this is unclear.
    
    We recommend validating the quality of any dataset that you plan to use before you start to train a model. Possible methods include cross-referencing datasets with other datasets or visually inspecting satellite images to see if a wildfire is locatable.

### How to set up the problem

- **Beware of biases when prepare the training data**

    Finding easy positive and negative examples of wildfire are easy (a flaming forest patch vs a middle of an ocean). 
Finding hard positive and negative examples are hard (a small fire vs a hot patch of land that is not on fire yet). 
When we do not have reliable ground truths in the first place, it is difficult to acquire hard examples that are correctly labelled.
Similar to cancer detection, frequency of occurrences of fire and non-fire images must be balanced, as well as balancing 
the sample frequency of hard and easy examples. 

- **Identify the metric you need to optimise for**

    The metric you want to optimise over will depend on whether your specific application requires low false-positives or low false-negatives.

### Pitfalls your model may fall into

- **Is your model learning misleading correlations?**

    The model might pick up characteristics related to but not directly corresponding to fire.
In order for the model to learn when there is a fire and when there is not, we should also include the same patch of land before & after the fire. 
Otherwise, the model will just see a burned patch (that is already extinguished, but nevertheless have characteristic features distinct from unburned areas) and shout “fire”.

- **Is human intervention taken into account?**

    For models which forecast, it might not be able to distinguish what will happen without human intervention, and what will happen with intervention.
If the model sees a red truck in the satellite image, it might predict that the fire will not spread. 
If the fire is detected near a urban area, the model may expect that the fire magically disappears.
However, what we want to know is the behaviour of the spread of the fire if humans didn’t intervene, which may not always be the case in your training data.

### Consequences of wrong predictions
It is important to consider the social impact of the model you deploy or the dataset you are going to release.
If your dataset or model is biased or is not accurate, there may be real-world consequences.
Below are some examples of questions that should be considered before deploying your model.

- **What are the consequences of false positives?**

    For detection: if a fire is reported where there isn’t, valuable fire fighting resources may be wasted.

- **What are the consequences of false negatives?**

    For detection: if a fire is not detected by the model, and the authorities trust the prediction, there could be a delay in finding out the fire and extinguishing them.

- **Other types of false predictions**

    For forecasting spread (segmentation): if the forecast is wrong, the consequences of not being able to distribute resources correctly might cause more harm than not having the forecast.
