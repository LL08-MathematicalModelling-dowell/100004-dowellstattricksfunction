# Documentation for the Stattricks API
### API call

```py
import requests

url = "https://100004.pythonanywhere.com/processapi"
```

### Payload for the API
#### Request method : POST

```py
{
    "title":"spreadsheet-data",    
    "Process_id":9974,
    "processSequenceId":1,
    "seriesvalues":{
         "list1":[3,3,3,2,1,1,2,5,6,15],
         "list2":[11,2,2,4,2,2,5,6,8,9],
         "list3":[9,2,3,3,4,4,4,7,8,9],
         "list4":[1,2,3,4,4,4,4,2,2,8],
         "list5":[1,2,3,4,5,6,7,8,9,10]
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
    "title": "spreadsheet-data",
    "Process_id": "9974",
    "processSequenceId": "1",
    "poison case results": {
        "series": {
            "list1": [
                3,
                3,
                3,
                2,
                1,
                1,
                2,
                5,
                6,
                15
            ],
            "list2": [
                11,
                2,
                2,
                4,
                2,
                2,
                5,
                6,
                8,
                9
            ],
            "list3": [
                9,
                2,
                3,
                3,
                4,
                4,
                4,
                7,
                8,
                9
            ],
            "list4": [
                1,
                2,
                3,
                4,
                4,
                4,
                4,
                2,
                2,
                8
            ],
            "list5": [
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10
            ]
        },
        "minimumSeries": 10,
        "maximumSeries": 10,
        "minimumSeriesDatapoint": {
            "list1": 1,
            "list2": 2,
            "list3": 2,
            "list4": 1,
            "list5": 1
        },
        "minimumContinuousDatapoint": 1,
        "mean": {
            "list1": 4.1,
            "list2": 5.1,
            "list3": 5.3,
            "list4": 3.4,
            "list5": 5.5
        },
        "median": {
            "list1": 3.0,
            "list2": 4.5,
            "list3": 4.0,
            "list4": 3.5,
            "list5": 5.5
        },
        "mode": {
            "list1": [
                3
            ],
            "list2": [
                2
            ],
            "list3": [
                4
            ],
            "list4": [
                4
            ],
            "list5": [
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10
            ]
        },
        "standardDeviation": {
            "list1": 3.935733730830885,
            "list2": 3.1448370387032774,
            "list3": 2.5317977802344322,
            "list4": 1.8547236990991407,
            "list5": 2.8722813232690143
        },
        "moment1": {
            "list1": 0.0,
            "list2": 0.0,
            "list3": 0.0,
            "list4": 0.0,
            "list5": 0.0
        },
        "moment2": {
            "list1": 15.489999999999998,
            "list2": 9.889999999999999,
            "list3": 6.409999999999999,
            "list4": 3.44,
            "list5": 8.25
        },
        "moment3": {
            "list1": 122.05199999999999,
            "list2": 16.93200000000001,
            "list3": 5.904000000000003,
            "list4": 7.607999999999997,
            "list5": 0.0
        },
        "moment4": {
            "list1": 1435.7496999999998,
            "list2": 188.5337,
            "list3": 61.9457,
            "list4": 49.299199999999985,
            "list5": 120.8625
        },
        "normalDistribution": {
            "list1": 0.16426626916911458,
            "list2": 1.9551629612967223,
            "list3": 2.7682022197655676,
            "list4": 1.5452763009008592,
            "list5": 2.6277186767309857
        },
        "skewness": {
            "list1": 2.0020170589049986,
            "list2": 0.5443946172234717,
            "list3": 0.36379716011458546,
            "list4": 1.1924298525170918,
            "list5": 0.0
        },
        "kurtosis": {
            "list1": 2.983783869390736,
            "list2": -1.0724910312732263,
            "list3": -1.492368836719147,
            "list4": 1.1660356949702537,
            "list5": -1.2242424242424244
        },
        "list-wise ranges": {
            "Range 1": {
                "range lists": [
                    [
                        1,
                        2,
                        3,
                        5,
                        6
                    ],
                    [
                        2,
                        4,
                        5,
                        6,
                        8
                    ],
                    [
                        3,
                        4,
                        7
                    ],
                    [
                        2,
                        3,
                        4
                    ],
                    [
                        3,
                        4,
                        5,
                        6,
                        7,
                        8
                    ]
                ],
                "lengths": [
                    5,
                    5,
                    3,
                    3,
                    6
                ],
                "total_length": 5
            },
            "Range 2": {
                "range lists": [
                    [],
                    [
                        9,
                        11
                    ],
                    [
                        2,
                        8,
                        9
                    ],
                    [
                        1
                    ],
                    [
                        1,
                        2,
                        9,
                        10
                    ]
                ],
                "lengths": [
                    0,
                    2,
                    3,
                    1,
                    4
                ],
                "total_length": 5
            },
            "Range 3": {
                "range lists": [
                    [
                        15
                    ],
                    [],
                    [],
                    [
                        8
                    ],
                    []
                ],
                "lengths": [
                    1,
                    0,
                    0,
                    1,
                    0
                ],
                "total_length": 5
            }
        },
        "count_val": 10
    },
    "normal case results": {
        "mergedSeries": [
            3,
            3,
            3,
            2,
            1,
            1,
            2,
            5,
            6,
            15,
            11,
            2,
            2,
            4,
            2,
            2,
            5,
            6,
            8,
            9,
            9,
            2,
            3,
            3,
            4,
            4,
            4,
            7,
            8,
            9,
            1,
            2,
            3,
            4,
            4,
            4,
            4,
            2,
            2,
            8,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10
        ],
        "seriesLength": 50,
        "maxMergedSeries": 15,
        "minMergedSeries": 1,
        "mergedMean": 4.68,
        "mergedMedian": 4.0,
        "mergedMode": [
            2
        ],
        "mergedRanges": {
            "Range1": {
                "range lists": [
                    [
                        2,
                        3,
                        4,
                        5,
                        6,
                        7
                    ]
                ],
                "lengths": [
                    6
                ],
                "total_length": 1
            },
            "Range2": {
                "range lists": [
                    [
                        1,
                        8,
                        9,
                        10
                    ]
                ],
                "lengths": [
                    4
                ],
                "total_length": 1
            },
            "Range3": {
                "range lists": [
                    [
                        11
                    ]
                ],
                "lengths": [
                    1
                ],
                "total_length": 1
            }
        },
        "mergedVariance": 9.3376,
        "mergedMoment1": 0.0,
        "mergedMoment2": 9.3376,
        "mergedMoment3": 31.116864000000017,
        "mergedMoment4": 340.88207872,
        "mergedSkewness": 1.090543322614494,
        "mergedKurtosis": 0.9096118089088971
    },
    "created on": "2023-09-08 09:19:46"
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
