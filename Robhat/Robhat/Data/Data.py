import numpy as np
import scipy.stats as stats
# from .. import Dome
# from ..Dome import Macros
# from ..Dome import Control
# from ..Dome import Sensors
# from ..Dome import UI
from collections import OrderedDict
from typing import Union, Text, NewType, List, Tuple, Dict, Generic, TypeVar, Iterable, Callable
import pandas as pd

SciData = NewType("SciData", Union[np.ndarray, pd.core.frame.DataFrame, pd.core.series.Series, List[Union[int, float, bytes]]])
"""NewType: A generic type for loads of data containers that scientific people use."""

def summary(data: SciData, *rest, angular=False, radians=True)->OrderedDict:
    """
    Generate an ordered dictionary of statistics and their values over a dataset
    Args:
        data (SciData): The data to be analyzed
        *rest: ignored.
        angular (bool): Is our data angular data? If so, we'll also provide circular statistics.
        radians (bool): Is our data in radians? If not, use degrees.

    Returns:
        numbers (OrderedDict): a dictionary containing the following statistics:

            - Mean
            - Min
            - Q1
            - Median
            - Q3
            - Max
            - Range
            - IQR
            - STD
            - CircMean (only if `angular=True`)
            - CircSTD (only if `angular=True`)
    """
    numbers = OrderedDict([("Mean", np.mean(data)),
                           ("Min", np.amin(data)),
                           ("Q1",np.percentile(data,25)),
                           ("Median",np.median(data)),
                           ("Q3",np.percentile(data, 75)),
                           ("Max", np.amax(data)),
                           ("Range", np.amax(data)-np.amin(data)),
                           ("IQR", np.percentile(data, 75)-np.percentile(data, 25)),
                           ("STD", np.std(data))])
    if angular:
        kwargs = {'high':2*np.pi, 'low':0} if radians else {'high':360, 'low':0}
        numbers["CircMean"] = stats.circmean(data, **kwargs)
        numbers["CircSTD"] = stats.circvar(data, **kwargs)
    return numbers

def textSummary(data: SciData, angular: bool=False, radians: bool=True) -> Text:
    """
    Uses the information provided by `summary` to create a text block of data.
    Args:
        data (SciData): The dataset to use.
        angular (bool): If our data is angular, then we also provide circular statistics.
        radians (bool): If our data is in degrees, need to pass `radians=False`

    Returns:
        (Text): A formatted string containing all statisical data provided by `summary`.
    """
    strings = []
    if angular:
        strings.append("{0:^20.20s}".format("Data Summary"))
        strings.append('='*20)
        strings += [f"{key+':':<10.12s} {value:>9.3f}" for key, value in summary(data, angular=True, radians=radians).items()]
        strings.append('='*20)
    else:
        strings.append("{0:^20.20s}".format("Data Summary"))
        strings.append('='*20)
        strings += [f"{key+':':<10.12s} {value:>9.3f}" for key, value in summary(data).items()]
        strings.append('='*20)
    return "\n".join(strings)

def boxcar(data: SciData, carlength: int = 5, func: Callable[[SciData],Union[float,int]] = np.mean) -> Tuple[List[Union[float,int]], List[Union[float,int]]]:
    """
    Runs boxcar averaging using `func` with n=carlength sized cars.
    Args:
        data (SciData): The data to process
        carlength (int): How many samples are processed each time we need.
        func (Callable[[SciData], Union[float,int]]): the function we use to process each chunk of data

    Returns:
        averages (List[Union[float, int]]): The running averages of the boxcar routine
        boxes (List[Union[float, int]):  The samples used in each step of the algorithm

    Next Steps:
        Run averages through `func` one more time to get a grand-average.
    """
    boxes = []
    averages = []
    for i in range(carlength-1, len(data)+carlength):
        boxes.append(data[i:i+carlength])
        averages.append(func(boxes[-1]))
    return averages, boxes
