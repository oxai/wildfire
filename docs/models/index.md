## Model

Initially, we approached the problem of wildfire identification using neural networks trained on positive and negative examples of wildfire. 
As stated in the [Challenges section](https://oxai.github.io/wildfire/challenges/), this turned out to be a complicated problem than we initially anticipated due to the lack of trustworthy ground truths. Here we briefly outline what our approach was nevertheless.

The task differs slightly from standard image recognition, as unlike normal images, satellite images have varying channels instead of three. Each channel introduces some additional information, e.g. infrared is correlated with temperature etc. Unfortunately, this also makes it difficult to visualise the channels in a meaningful way without introducing some handcrafted features e.g. weighted combinations of bands.

We created a small dataset of Sentinel 2 satellite images that are collected using MODIS Fire Archive as the source of fire records (latitude, longitude, timestamp). We defined positive examples to be images at that location taken within four days of MODIS Fire Archive recording the fire (because Sentinel 2 only visits a location once every 3-5 days), with a threshold of the confidence level. 

Jan was in charge of developing a prototype of a wildfire classifier. He prepared classes for datasets and data loaders, and compared various neural network architectures. 
We were not able to leverage the benefits of pre-trained models, such as ResNet16, ResNet50, ResNet101, even after adjusting the first convolutional filter for a ten band input and retraining. This is to be expected since satellite images have significantly different features to images in ImageNet. A simple convolutional neural network with only 2-4 layers worked significantly better on the small dataset that we created, yielding a validation accuracy of over 90%. 

As we have noted in the [Challenges section](https://oxai.github.io/wildfire/challenges/), however, this experiment is incomplete due to the lack of ground truths. The validation dataset we created still relies on the MODIS fire detection algorithm, which is a handcrafted heuristic that performs reasonably well, but could also be detecting false positives and have false negatives. The neural network would have just learnt to reverse engineer the algorithm, rather than learn the true underlying distribution. While it may be possible for experts to go through the fire records flagged by MODIS Fire Archive and identify the true positives, which was indeed a direction that we initially pursued, we would not be able to recover the false negatives.   

The training pipeline can be found in the [models directory](https://github.com/oxai/wildfire/tree/master/models) of the repository. 
There are training scripts written by Jan, based on the fastai library. 
Further improvements may be made by:
- Ensembling/Stacking
- Using more augmentations
- Taking advantage of the tabular data
- Getting a more reliable dataset

---
Written by Jan Malinowski, edited by Shu Ishida