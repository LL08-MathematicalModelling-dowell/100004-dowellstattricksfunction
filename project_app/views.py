from django.shortcuts import render
from django.http import HttpResponse
import pymongo
from collections import Counter
import math
from scipy.stats import kurtosis
from scipy.stats import moment
from django.http import JsonResponse
import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
db = client['mongodb']

def default(request):
    return render(request,"dashboard.html")

def dbConnectionTest(reuest):
    return HttpResponse(str(client.test))

def form(request):
    return render(request,"form.html")

def mean(n_num):
    n = len(n_num)  
    get_sum = sum(n_num)
    mean = get_sum / n
    return mean

def median(n_num):
    n = len(n_num)
    n_num.sort()
    if n % 2 == 0:
        median1 = n_num[n//2]
        median2 = n_num[n//2 - 1]
        median = (median1 + median2)/2
        return median
    else:
        median = n_num[n//2]
        return median

def mode(n_num):
    n = len(n_num)
    data = Counter(n_num)
    get_mode = dict(data)
    mode = [k for k, v in get_mode.items() if v == max(list(data.values()))]
    return mode

def variance(data, ddof=0):
    n = len(data)
    mean = sum(data) / n
    return sum((x - mean) ** 2 for x in data) / (n - ddof)

def stdev(data):
    var = variance(data)
    std_dev = math.sqrt(var)
    return std_dev

def insertData(request):
    cursor=db.QR_IMAGE
    if request.method=="POST":
        processId = request.POST.get("processId")
        processSequenceId = request.POST.get("processSequenceId")
        numOfValues = request.POST.get("numOfValues")
        minimumSeries = request.POST.get("minimumSeries")
        minimumSeriesDatapoint = request.POST.get("minimumSeriesDatapoint")
        minimumContinuousDatapoint = request.POST.get("minimumContinuousDatapoint")
        processHours = request.POST.get("processHours")
        values = request.POST.get("values")
        startTricks=request.POST.get("startTricks")
        series={}
        seriesValues=[]
        seriesValuesMean={}
        seriesValuesMedian={}
        seriesValuesMode={}
        moment1={}
        moment2={}
        moment3={}
        moment4={}
        stdValue={}
        for i in range(int(numOfValues)):
            temporary=request.POST.get("1000"+str(i+1))
            temporary2=temporary.split(',')
            temporary3=[int(i) for i in temporary2]
            seriesValuesMean["1000"+str(i+1)]=mean(temporary3)
            seriesValuesMedian["1000"+str(i+1)]=median(temporary3)
            seriesValuesMode["1000"+str(i+1)]=mode(temporary3)
            stdValue["1000"+str(i+1)]=stdev(temporary3)
            moment1["1000"+str(i+1)]=moment(temporary3, moment=1)
            moment2["1000"+str(i+1)]=moment(temporary3, moment=2)
            moment3["1000"+str(i+1)]=moment(temporary3, moment=3)
            moment4["1000"+str(i+1)]=moment(temporary3, moment=4)
            series["1000"+str(i+1)]=temporary3
        print(series)
        result=cursor.find_one({"processSequenceId":processSequenceId})
        if result:
            return HttpResponse("Entered sequence id is already exist!")
        else:
            cursor.insert_one({"document":"qr","title":"userData","processId":processId,"processSequenceId":processSequenceId,"series":series,"minimumSeries":minimumSeries,"minimumSeriesDatapoint":minimumSeriesDatapoint,"minimumContinuousDatapoint":minimumContinuousDatapoint,"processHours":processHours,"startTricks":startTricks,"mean":seriesValuesMean,"median":seriesValuesMedian,"mode":seriesValuesMode,"standardDeviation":stdValue,"moment1":moment1,"moment2":moment2,"moment3":moment3,"moment4":moment4})
            return HttpResponse("Inserted!")
    else:
        return HttpResponse("No Data Found")

def fetchDataForm(request):
    return render(request,"fetchData.html")

def fetchData(request):
    cursor=db.QR_IMAGE
    if request.method=="POST":
        processSequenceId = request.POST.get("psi")
        result=cursor.find_one({"processSequenceId":processSequenceId})
        print(result)
        if result!=None:
            data=JSONEncoder().encode(result)
            return HttpResponse(data)
        else:
            return HttpResponse("No Data Found")
