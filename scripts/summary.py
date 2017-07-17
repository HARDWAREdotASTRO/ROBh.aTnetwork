import numpy as np
from collections import OrderedDict
def summary(data):
    numbers = OrderedDict([("Mean", np.mean(data)),("Min", np.amin(data)),("Q1",np.percentile(data,25)),("Median",np.median(data)),("Q3",np.percentile(data, 75)), ("Max", np.amax(data)), ("IQR", np.percentile(data, 75)-np.percentile(data, 25)), ("STD", np.std(data))])
    return numbers