import numpy as np
import scipy.stats as stats

def summary(data, *rest, angular=False, radians=True):
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

def textSummary(data, angular=False, radians=True):
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

def boxcar(data, carlength=5, func=np.mean):
    boxes = []
    averages = []
    for i in range(carlength-1, len(data)+carlength):
        boxes.append(data[i:i+carlength])
        averages.append(func(boxes[-1]))
    return averages, boxes
