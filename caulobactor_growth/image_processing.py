# Import statements
import glob
import os

import numpy as np
import pandas as pd

import skimage
import skimage.io
import skimage.filters
import skimage.segmentation
import skimage.morphology
import matplotlib.pyplot as plt

import bebi103

import panel as pn 
pn.extension()

import bokeh
import holoviews as hv
bokeh.io.output_notebook()
hv.extension('bokeh')

def threshold_using_otsu(img):
    '''This function takes in an image and calculates the threshold based
       on the otsu method. It then returns the image with the background
       as 0 and the bacteria as 1.'''
    threshold = skimage.filters.threshold_otsu(img)
    im_filtered = img < threshold
    return im_filtered

def calc_area(im_stack):
    '''This function takes in an image stack and for each image in the stack,
       calculates the area of the bacteria by using thresholding to segment
       the image and then clearing out the borders. Then, the image is summed
       together for the interpixel squared area.
       -------------------------------------------------------------------------
       The function parameter is just an image stack.
       ---------------------------------------------------------------------------
       The function returns a data frame with four columns: area in sq ip distance,
       area in sq μm, the frame number and the time in minutes. '''
    interpixel_dist = 0.052
    data = []
    for i in range(len(im_stack)):
        im_thresh = threshold_using_otsu(im_stack[i])
        im_clear_border = skimage.segmentation.clear_border(im_thresh, buffer_size=5)
        ip_area = np.sum(im_clear_border)
        area = ip_area * interpixel_dist ** 2
        data.append([ip_area, area, i, i])
    
    df = pd.DataFrame(
        data = data,
        columns = ["area (sq ip distance)", "area (sq μm)", "frame", "time (min)"]
    )
    return df