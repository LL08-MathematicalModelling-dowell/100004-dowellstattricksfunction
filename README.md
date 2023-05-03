# Documentation for the Stattricks API
### API call

```py
import requests

url = "https://100004.pythonanywhere.com/api"
```

### Payload for the API
#### Request method : POST

```py
{
   "title": "demo-case",
   "Process_id": 12345,
   "processSequenceId": 11,
   "series": 4,
   "seriesvalues":{
       "list1":[3,3,3,7],
       "list2":[11,2,2,4],
       "list3":[9,2,3,3],
       "list4":[1,2,3,4,4]
   }
}
```
```txt
NOTE: 1. The length of each list in the "seriesvalues" dictionary should be greater than or equal to 3
      2. Refer the variable definition section for more clarity on the input variables
```

### Response

```py
{
    "msg": "Successfully generated the results",
    "title": "demo-case",
    "Process_id": 12345,
    "processSequenceId": 11,
    "poison case results": {
        "series": {
            "list1": [
                3,
                3,
                3,
                7
            ],
            "list2": [
                2,
                2,
                4,
                11
            ],
            "list3": [
                2,
                3,
                3,
                9
            ],
            "list4": [
                1,
                2,
                3,
                4,
                4
            ]
        },
        "minimumSeries": 4,
        "maximumSeries": 5,
        "minimumSeriesDatapoint": {
            "list1": 3,
            "list2": 2,
            "list3": 2,
            "list4": 1
        },
        "minimumContinuousDatapoint": 1,
        "mean": {
            "list1": 4.0,
            "list2": 4.75,
            "list3": 4.25,
            "list4": 2.8
        },
        "median": {
            "list1": 3.0,
            "list2": 3.0,
            "list3": 3.0,
            "list4": 3
        },
        "mode": {
            "list1": [
                3
            ],
            "list2": [
                2
            ],
            "list3": [
                3
            ],
            "list4": [
                4
            ]
        },
        "standardDeviation": {
            "list1": 1.7320508075688772,
            "list2": 3.6996621467371855,
            "list3": 2.7726341266023544,
            "list4": 1.16619037896906
        },
        "moment1": {
            "list1": 0.0,
            "list2": 0.0,
            "list3": 0.0,
            "list4": 0.0
        },
        "moment2": {
            "list1": 3.0,
            "list2": 13.6875,
            "list3": 7.6875,
            "list4": 1.3599999999999999
        },
        "moment3": {
            "list1": 6.0,
            "list2": 50.53125,
            "list3": 22.96875,
            "list4": -0.5759999999999993
        },
        "moment4": {
            "list1": 21.0,
            "list2": 410.14453125,
            "list3": 134.89453125,
            "list4": 3.011199999999999
        },
        "normalDistribution": {
            "list1": 2.267949192431123,
            "list2": 1.0503378532628145,
            "list3": 1.4773658733976456,
            "list4": 1.6338096210309399
        },
        "skewness": {
            "list1": 1.1547005383792515,
            "list2": 0.9978697176912956,
            "list3": 1.0776051731391265,
            "list4": -0.36317347441943004
        },
        "kurtosis": {
            "list1": -0.6666666666666665,
            "list2": -0.8107837618064679,
            "list3": -0.7174301011302795,
            "list4": -1.3719723183391006
        },
        "range": {
            "1": [
                3,
                2,
                2,
                1
            ],
            "2": [
                3,
                2,
                3,
                2
            ],
            "3": [
                3,
                4,
                3,
                3
            ]
        },
        "count_val": 5
    },
    "normal case results": {
        "mergedSeries": [
            1,
            2,
            2,
            2,
            2,
            3,
            3,
            3,
            3,
            3,
            3,
            4,
            4,
            4,
            7,
            9,
            11
        ],
        "seriesLength": 17,
        "maxMergedSeries": 11,
        "minMergedSeries": 1,
        "mergedMean": 3.8823529411764706,
        "mergedMedian": 3,
        "mergedMode": [
            3
        ],
        "mergedStdValues": {
            "mergedStdValue": 2.58689805027012,
            "mergedStdValue_-3": -7.760694150810361,
            "mergedStdValue_-2": -5.17379610054024,
            "mergedStdValue_-1": -2.58689805027012,
            "mergedStdValue_3": 7.760694150810361,
            "mergedStdValue_2": 5.17379610054024,
            "mergedStdValue_1": 2.58689805027012
        },
        "mergedRanges": {
            "Range1": [
                2,
                2,
                2,
                2,
                3,
                3,
                3,
                3,
                3,
                3
            ],
            "Range2": [
                1,
                4,
                4,
                4
            ],
            "Range3": []
        },
        "mergedVariance": 6.6920415224913485,
        "mergedMoment1": 0.0,
        "mergedMoment2": 6.6920415224913485,
        "mergedMoment3": 27.65764298799104,
        "mergedMoment4": 204.10648818859923,
        "mergedSkewness": 1.5976337478934297,
        "mergedKurtosis": 1.557635155584121
    },
    "created on": "2023-05-03 13:39:25.883178"
}
```
```py
headers={'content-type': 'application/json'}
try:
    response=requests.post(url,json=data,headers=headers)
    return response.text
except:
    return "Check the input values!"
```
    
### Variable definitions
```txt
title : any title of your choice
processId : a number either random or specific to your project
processSequenceId : a number either random or specific to your project
series : the number of series you wish to pass
seriesvalues : a dictionary with series names as keys and corresponding series as values
```
