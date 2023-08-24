from collections import Counter
import math
from scipy.stats import kurtosis,moment,skew
import json
from bson import ObjectId
# from .dowellconnection import dowellconnection

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def mean(n_num):
    n = len(n_num)
    if n==0:
        return 0
    else:
        get_sum = sum(n_num)
        mean = get_sum / n
        return mean

def median(n_num):
    n = len(n_num)
    n_num.sort()
    if n==0:
        return 0
    elif n % 2 == 0:
        median1 = n_num[n//2]
        median2 = n_num[n//2 - 1]
        median = (median1 + median2)/2
        return median
    else:
        median = n_num[n//2]
        return median

def mode(n_num):
    c = Counter(n_num)
    return [k for k, v in c.items() if v == c.most_common(1)[0][1]]

def variance(data, ddof=0):
    n = len(data)
    if n==0:
        return 0
    else:
        mean = sum(data) / n
        return sum((x - mean) ** 2 for x in data) / (n - ddof)

def stdev(data):
    var = variance(data)
    std_dev = math.sqrt(var)
    return std_dev

def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

def normalDistributionFunc(response):
    # response is from the db
    mergedSeries = [val for series in response["seriesvalues"].values() for val in series]
    return mergedSeries

def assign_range(data_list,mean, sd):
    range1, range2, range3 = [],[],[]

    range1_lower = mean - sd
    range1_upper = mean + sd
    range2_lower = mean - 2*sd
    range2_upper = mean + 2*sd
    range3_lower = mean - 3*sd
    range3_upper = mean + 3*sd

    for obs in data_list:
        if range1_lower <=obs <= range1_upper:
            range1.append(obs)

        elif range2_lower <=obs <= range2_upper:
            range2.append(obs)

        elif range3_lower <=obs <= range3_upper:
            range3.append(obs)

    return range1, range2, range3

def dowellstattricks(seriesvalues):

    series={}
    seriesVariance={}
    seriesValuesMean={}
    seriesValuesMedian={}
    seriesValuesMode={}
    moment1={}
    moment2={}
    moment3={}
    moment4={}
    stdValue={}
    skewness={}
    kurtosisValues={}
    minimumSeriesDatapoint={}
    normalDistribution={}
    continousDatapoints=[]
    seriesLenghts=[]
    count=0
    ranges={"Range 1":[],"Range 2":[],"Range 3":[]}
    standardDeviation={}

    for i in seriesvalues:
        temporary3=seriesvalues[i]
        # temporary2=temporary.split(',')
        # temporary3=[int(i) for i in temporary2]
        print(temporary3)
        count_val=count+len(temporary3)
        seriesValuesMean[str(i)]=mean(temporary3)
        seriesValuesMedian[str(i)]=median(temporary3)
        seriesValuesMode[str(i)]=mode(temporary3)
        stdValue[str(i)]=stdev(temporary3)
        standardDeviation[str(i)]=stdev(temporary3)
        range1, range2, range3 = assign_range(seriesvalues[i], seriesValuesMean[str(i)], stdValue[str(i)])
        ranges["Range 1"].append(range1)
        ranges["Range 2"].append(range2)
        ranges["Range 3"].append(range3)
        seriesVariance[str(i)]=variance(temporary3)
        normalDistribution[str(i)]=seriesValuesMean[str(i)]-stdValue[str(i)]
        moment1[str(i)]=moment(temporary3, moment=1)
        moment2[str(i)]=moment(temporary3, moment=2)
        moment3[str(i)]=moment(temporary3, moment=3)
        moment4[str(i)]=moment(temporary3, moment=4)
        skewness[str(i)]=skew(temporary3)
        kurtosisValues[str(i)]=kurtosis(temporary3)
        series[str(i)]=temporary3
        minimumSeriesDatapoint[str(i)]=min(temporary3)
        for j in temporary3:continousDatapoints.append(j)
        seriesLenghts.append(len(temporary3))
    minimumContinuousDatapoint=min(continousDatapoints)
    minimumSeries=min(seriesLenghts)
    maximumSeries=max(seriesLenghts)

    qrImageData={
                "series":series,
                "minimumSeries":minimumSeries,
                "maximumSeries": maximumSeries,
                "minimumSeriesDatapoint":minimumSeriesDatapoint,
                "minimumContinuousDatapoint":minimumContinuousDatapoint,
                "mean":seriesValuesMean,
                "median":seriesValuesMedian,
                "mode":seriesValuesMode,
                "standardDeviation":stdValue,
                "moment1":moment1,
                "moment2":moment2,
                "moment3":moment3,
                "moment4":moment4,
                "normalDistribution":normalDistribution,
                "skewness":skewness,
                "kurtosis":kurtosisValues,
                "list-wise ranges":ranges,
                "standardDeviation":standardDeviation,
                "count_val":count_val,
                }
    inputData={}
    # inputData["Process_id"]=Process_id
    # inputData["title"]=title
    inputData["series"]=series
    inputData["seriesvalues"]=seriesvalues

    # dowellconnection("FB","bangalore","blr","input","input","1234567","ABCDE","insert",inputData,"nil")

    # Combine observations computation
    mergedRange1 = list()
    mergedRange2 = list()
    mergedRange3 = list()

    mergedResult = normalDistributionFunc(inputData)
    count = len(mergedResult)
    maxMergedResult = max(mergedResult)
    minMergedResult = min(mergedResult)
    mergedMean = mean(mergedResult)
    mergedMedian = median(mergedResult)
    mergedMode = mode(mergedResult)
    mergedStdValue = stdev(mergedResult)
    # mergedStdValue__3 indicates standard deviation multiplied by negative 3
    mergedStdValue__3 = mergedStdValue * -3
    mergedStdValue__2 = mergedStdValue * -2
    mergedStdValue__1 = mergedStdValue * -1
    mergedStdValue_3 = mergedStdValue * 3
    mergedStdValue_2 = mergedStdValue * 2
    mergedStdValue_1 = mergedStdValue * 1

    for observation in mergedResult:
        if mergedStdValue - 1 <= observation <= mergedStdValue + 1:
            mergedRange1.append(observation)

        elif mergedStdValue - 2 <= observation <= mergedStdValue + 2:
            mergedRange2.append(observation)

        elif mergedStdValue - 3 <= observation <= mergedStdValue + 3:
            mergedRange3.append(observation)

    mergedVariance = variance(mergedResult)
    mergedMoment1 = moment(mergedResult, moment=1)
    mergedMoment2 = moment(mergedResult, moment=2)
    mergedMoment3 = moment(mergedResult, moment=3)
    mergedMoment4 = moment(mergedResult, moment=4)
    mergedSkewness = skew(mergedResult)
    mergedKurtosis = kurtosis(mergedResult)

    combinedObservations = {
                            "mergedSeries": mergedResult,
                            "seriesLength":count,
                            "maxMergedSeries": maxMergedResult,
                            "minMergedSeries": minMergedResult,
                            "mergedMean": mergedMean,
                            "mergedMedian": mergedMedian,
                            "mergedMode": mergedMode,
                            "mergedStdValues":{"mergedStdValue": mergedStdValue,"mergedStdValue_-3": mergedStdValue__3,"mergedStdValue_-2": mergedStdValue__2,"mergedStdValue_-1": mergedStdValue__1,"mergedStdValue_3": mergedStdValue_3,"mergedStdValue_2": mergedStdValue_2,"mergedStdValue_1": mergedStdValue_1},
                            "mergedRanges": {"Range1": mergedRange1,"Range2": mergedRange2,"Range3": mergedRange3},
                            "mergedVariance": mergedVariance,
                            "mergedMoment1": mergedMoment1,
                            "mergedMoment2": mergedMoment2,
                            "mergedMoment3": mergedMoment3,
                            "mergedMoment4": mergedMoment4,
                            "mergedSkewness": mergedSkewness,
                            "mergedKurtosis": mergedKurtosis
                            }

    return qrImageData, combinedObservations
