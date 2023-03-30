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
   "title": "backendtesting",
   "Process_id": 10122,
   "processSequenceId": 16,
   "series": 3,				
   "seriesvalues":{
       "list1":[2,23,5,7,2],
       "list2":[5,5,6,7,10],
       "list3":[11,12,13,14,11],
       "list4":[8,8,7,9,15]
   }
}

NOTE: Refer the variable definition section for clarity on input variables
```
### Response

```py
{
    "msg": "Successfully generated the results",
    "Title :": "backendtesting",
    "Process Id :": 10122,
    "Process Sequence Id :": 16,
    "Series :": {
        "list1": [
            2,
            2,
            5,
            7,
            23
        ],
        "list2": [
            5,
            5,
            6,
            7,
            10
        ],
        "list3": [
            11,
            11,
            12,
            13,
            14
        ],
        "list4": [
            7,
            8,
            8,
            9,
            15
        ]
    },
    "Minimum Series |": 5,
    "Minimum Series Data Point :": {
        "list1": 2,
        "list2": 5,
        "list3": 11,
        "list4": 7
    },
    "Minimum Continuous Data Point :": 2,
    "Min continous data point": 2,
    "Mean :": {
        "list1": 7.8,
        "list2": 6.6,
        "list3": 12.2,
        "list4": 9.4
    },
    "Median :": {
        "list1": 5,
        "list2": 6,
        "list3": 12,
        "list4": 8
    },
    "Mode :": {
        "list1": [
            2
        ],
        "list2": [
            5
        ],
        "list3": [
            11
        ],
        "list4": [
            8
        ]
    },
    "Moment1 :": {
        "list1": 0.0,
        "list2": 0.0,
        "list3": 0.0,
        "list4": 0.0
    },
    "Moment2 :": {
        "list1": 61.36,
        "list2": 3.44,
        "list3": 1.3599999999999999,
        "list4": 8.24
    },
    "Moment3 :": {
        "list1": 619.8239999999998,
        "list2": 6.192000000000003,
        "list3": 0.5760000000000028,
        "list4": 31.24799999999999
    },
    "Moment4 :": {
        "list1": 11140.9312,
        "list2": 29.379200000000008,
        "list3": 3.0112000000000014,
        "list4": 204.86719999999997
    },
    "Normal Distribution :": {
        "list1": -0.03326241102645611,
        "list2": 4.7452763009008585,
        "list3": 11.03380962103094,
        "list4": 6.529459981118535
    },
    "Skewness :": {
        "list1": 1.289556461793242,
        "list2": 0.9704949588309462,
        "list3": 0.3631734744194323,
        "list4": 1.3210869678752706
    },
    "Kurtosis :": {
        "list1": -0.04096031032366687,
        "list2": -0.5173066522444554,
        "list3": -1.3719723183390993,
        "list4": 0.01729663493260425
    },
    "Range :": {
        "1": [
            2,
            5,
            11,
            7
        ],
        "2": [
            2,
            5,
            11,
            8
        ],
        "3": [
            5,
            6,
            12,
            8
        ]
    },
    "Standard Deviation :": {
        "list1": 7.833262411026456,
        "list2": 1.8547236990991407,
        "list3": 1.16619037896906,
        "list4": 2.870540018881465
    },
    "StartTricks :": "yes",
    "Process Time :": "0:0:1",
    "created_on :": "2023-03-03 08:55:46.138123"
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
