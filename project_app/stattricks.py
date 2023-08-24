import numpy as np
from collections import Counter
from scipy.stats import kurtosis, moment, skew

def mean(n_num):
    n = len(n_num)
    if n == 0:
        return 0
    else:
        return np.mean(n_num)

def median(n_num):
    n = len(n_num)
    if n == 0:
        return 0
    else:
        return np.median(n_num)

def mode(n_num):
    c = Counter(n_num)
    return [k for k, v in c.items() if v == c.most_common(1)[0][1]]

def variance(data, ddof=0):
    n = len(data)
    if n == 0:
        return 0
    else:
        return np.var(data, ddof=ddof)

def stdev(data):
    var = variance(data)
    return np.sqrt(var)

def assign_range(data_list,mean, sd):
    range1, range2, range3 = [],[],[]

    range1_lower = mean - sd
    range1_upper = mean + sd
    range2_lower = mean - 2*sd
    range2_upper = mean + 2*sd
    range3_lower = mean - 3*sd
    range3_upper = mean + 3*sd

    for obs in data_list:
        if np.any(range1_lower <=obs <= range1_upper):
            if obs not in range1:
                range1.append(obs)

        elif np.any(range2_lower <=obs <= range2_upper):
            if obs not in range2:
                range2.append(obs)

        elif np.any(range3_lower <=obs <= range3_upper):
            if obs not in range3:
                range3.append(obs)

    range1.sort()
    range2.sort()
    range3.sort()

    return range1, range2, range3

def sort_range(ranges):
    range_dict = {}
    for key, lists in ranges.items():
        sublist_lengths = [len(sublist) for sublist in lists]
        range_dict[key] = {
            "range lists": lists,
            "lengths": sublist_lengths,
            "total_length": len(lists)
        }
    return range_dict

def dowellstattricks(seriesvalues):

    # series = {}
    seriesVariance = {}
    seriesValuesMean = {}
    seriesValuesMedian = {}
    seriesValuesMode = {}
    moment1 = {}
    moment2 = {}
    moment3 = {}
    moment4 = {}
    stdValue = {}
    skewness = {}
    kurtosisValues = {}
    minimumSeriesDatapoint = {}
    normalDistribution = {}
    continousDatapoints = []
    seriesLengths = []
    count = 0
    ranges = {"Range 1":[],"Range 2":[],"Range 3":[]}

    standardDeviation = {}

    for i, series_data in seriesvalues.items():

        seriesValuesMean[i] = mean(series_data)
        seriesValuesMedian[i] = median(series_data)
        seriesValuesMode[i] = mode(series_data)
        stdValue[i] = stdev(series_data)
        standardDeviation[i] = stdev(series_data)
        seriesVariance[i] = variance(series_data)
        range1, range2, range3 = assign_range(series_data, seriesValuesMean[i], stdValue[i])
        ranges["Range 1"].append(range1)
        ranges["Range 2"].append(range2)
        ranges["Range 3"].append(range3)

        count_val = count + len(series_data)
        normalDistribution[i] = seriesValuesMean[i] - stdValue[i]
        moment1[i] = moment(series_data, moment=1)
        moment2[i] = moment(series_data, moment=2)
        moment3[i] = moment(series_data, moment=3)
        moment4[i] = moment(series_data, moment=4)
        skewness[i] = skew(series_data)
        kurtosisValues[i] = kurtosis(series_data)
        minimumSeriesDatapoint[i] = np.min(series_data)
        continousDatapoints.extend(series_data)
        seriesLengths.append(len(series_data))
    minimumContinuousDatapoint = np.min(continousDatapoints)
    minimumSeries = np.min(seriesLengths)
    maximumSeries = np.max(seriesLengths)
    list_ranges = sort_range(ranges)

    for key in seriesvalues:
        if seriesvalues[key] is not None:
            seriesvalues[key] = seriesvalues[key].tolist()

    print("Seriesvalues------------------>",seriesvalues)
    qrImageData = {
        "series": seriesvalues,
        "minimumSeries": minimumSeries,
        "maximumSeries": maximumSeries,
        "minimumSeriesDatapoint": minimumSeriesDatapoint,
        "minimumContinuousDatapoint": minimumContinuousDatapoint,
        "mean": seriesValuesMean,
        "median": seriesValuesMedian,
        "mode": seriesValuesMode,
        "standardDeviation": stdValue,
        "moment1": moment1,
        "moment2": moment2,
        "moment3": moment3,
        "moment4": moment4,
        "normalDistribution": normalDistribution,
        "skewness": skewness,
        "kurtosis": kurtosisValues,
        "list-wise ranges": list_ranges,
        # "standardDeviation": standardDeviation,
        "count_val": count_val,
    }
    print("QR IMAGE SUCCESS")
    mergedResult = np.concatenate(list(seriesvalues.values()))
    Range_data = {"Range1": [], "Range2": [], "Range3": []}
    count = len(mergedResult)
    maxMergedResult = np.max(mergedResult)
    minMergedResult = np.min(mergedResult)
    mergedMean = np.mean(mergedResult)
    mergedMedian = np.median(mergedResult)
    mergedMode = mode(mergedResult)
    mergedStdValue = np.std(mergedResult)
    mergedRange1, mergedRange2, mergedRange3 = assign_range(mergedResult, mergedMean, mergedStdValue)
    Range_data["Range1"].append(mergedRange1)
    Range_data["Range2"].append(mergedRange2)
    Range_data["Range3"].append(mergedRange3)
    mergedRanges = sort_range(Range_data)
    # mergedStdValue__3 = mergedStdValue * -3
    # mergedStdValue__2 = mergedStdValue * -2
    # mergedStdValue__1 = mergedStdValue * -1
    # mergedStdValue_3 = mergedStdValue * 3
    # mergedStdValue_2 = mergedStdValue * 2
    # mergedStdValue_1 = mergedStdValue * 1

    # mergedRange1 = mergedResult[(mergedStdValue - 1 <= mergedResult) & (mergedResult <= mergedStdValue + 1)]
    # mergedRange2 = mergedResult[(mergedStdValue - 2 <= mergedResult) & (mergedResult <= mergedStdValue + 2)]
    # mergedRange3 = mergedResult[(mergedStdValue - 3 <= mergedResult) & (mergedResult <= mergedStdValue + 3)]

    mergedVariance = np.var(mergedResult)
    mergedMoment1 = moment(mergedResult, moment=1)
    mergedMoment2 = moment(mergedResult, moment=2)
    mergedMoment3 = moment(mergedResult, moment=3)
    mergedMoment4 = moment(mergedResult, moment=4)
    mergedSkewness = skew(mergedResult)
    mergedKurtosis = kurtosis(mergedResult)

    combinedObservations = {
        "mergedSeries": mergedResult,
        "seriesLength": count,
        "maxMergedSeries": maxMergedResult,
        "minMergedSeries": minMergedResult,
        "mergedMean": mergedMean,
        "mergedMedian": mergedMedian,
        "mergedMode": mergedMode,
        # "mergedStdValues": {
        #     "mergedStdValue": mergedStdValue,
        #     "mergedStdValue_-3": mergedStdValue__3,
        #     "mergedStdValue_-2": mergedStdValue__2,
        #     "mergedStdValue_-1": mergedStdValue__1,
        #     "mergedStdValue_3": mergedStdValue_3,
        #     "mergedStdValue_2": mergedStdValue_2,
        #     "mergedStdValue_1": mergedStdValue_1,
        # },
        "mergedRanges": mergedRanges,
        "mergedVariance": mergedVariance,
        "mergedMoment1": mergedMoment1,
        "mergedMoment2": mergedMoment2,
        "mergedMoment3": mergedMoment3,
        "mergedMoment4": mergedMoment4,
        "mergedSkewness": mergedSkewness,
        "mergedKurtosis": mergedKurtosis
    }

    return qrImageData, combinedObservations