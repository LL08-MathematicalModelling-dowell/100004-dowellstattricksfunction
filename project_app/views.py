from django.shortcuts import render
from django.http import HttpResponse
import pymongo
from collections import Counter
import math
from scipy.stats import kurtosis
from scipy.stats import moment
from TRYMONGO1 import insert

client = pymongo.MongoClient("mongodb+srv://sohaib:sohaib2140@project0.ghjdn.mongodb.net/FB?retryWrites=true&w=majority")
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
    cursor=db.qr
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
            cursor.insert_one({"title":"userData","processId":processId,"processSequenceId":processSequenceId,"series":series,"minimumSeries":minimumSeries,"minimumSeriesDatapoint":minimumSeriesDatapoint,"minimumContinuousDatapoint":minimumContinuousDatapoint,"processHours":processHours,"startTricks":startTricks,"mean":seriesValuesMean,"median":seriesValuesMedian,"mode":seriesValuesMode,"standardDeviation":stdValue,"moment1":moment1,"moment2":moment2,"moment3":moment3,"moment4":moment4})
            print("done")
            sendData={"title":"userData","processId":processId,"processSequenceId":processSequenceId,"series":series,"minimumSeries":minimumSeries,"minimumSeriesDatapoint":minimumSeriesDatapoint,"minimumContinuousDatapoint":minimumContinuousDatapoint,"processHours":processHours,"startTricks":startTricks,"mean":seriesValuesMean,"median":seriesValuesMedian,"mode":seriesValuesMode,"standardDeviation":stdValue,"moment1":moment1,"moment2":moment2,"moment3":moment3,"moment4":moment4}
            insert(sendData)
            return HttpResponse("Inserted!")
    else:
        return HttpResponse("No Data Found")

# def processSeries10001(request):
#     cursor=db.qr
#     result=cursor.find({"title":"userData"})
#     temp=0
#     minimumValue=0
#     maximumValue=0
#     series10001=[]
#     for row in result:
#         if temp==0:
#             minimumValue=int(row["series"]["10001"])
#             maximumValue=int(row["series"]["10001"])
#             series10001.append(int(row["series"]["10001"]))
#         else:
#             if minimumValue > int(row["series"]["10001"]):
#                 minimumValue = int(row["series"]["10001"])
#             else:
#                 pass
#             if maximumValue < int(row["series"]["10001"]):
#                 maximumValue=int(row["series"]["10001"])
#             else:
#                 pass
#             series10001.append(int(row["series"]["10001"]))
#         temp=temp+1
#     meanValue=mean(series10001)
#     medianValue=median(series10001)
#     modeValue=mode(series10001)
#     stdValue=stdev(series10001)
#     moment1=moment(series10001, moment=1)
#     moment2=moment(series10001, moment=2)
#     moment3=moment(series10001, moment=3)
#     moment4=moment(series10001, moment=4)
#     cursor.find_one_and_update({"title":"processSeries10001"},{"$set":{"minimumValue":minimumValue,"mean":meanValue,"maximumValue":maximumValue,"median":medianValue,"mode":modeValue,"standardDeviation":str("%.3f" % stdValue),"m1":str(moment1),"m2":str(moment2),"m3":str(moment3),"m4":str(moment4)}})
#     return HttpResponse("Minimum Value of Series 10001: "+str(minimumValue)+"<br>Maximum Value of Series 10001: "+str(maximumValue)+"<br>Mean Value of Series 10001: "+str("%.2f" % meanValue)+"<br>Median Value of Series 10001: "+str(medianValue)+"<br>Mode Value of Series 10001: "+str(modeValue[0])+"<br>Standard Deviation of Series 10001: "+str("%.3f" % stdValue)+"<br>m1 : "+str(moment1)+"<br>m2 : "+str(moment2)+"<br>m3 : "+str(moment3)+"<br>m4 : "+str(moment4))

# def processAllDatapoints(request):
#     cursor=db.qr
#     result=cursor.find({"title":"userData"})
#     dataPoints=[]
#     for row in result:
#         for i in row["series"]:
#             dataPoints.append(int(row["series"][i]))
#     kurtosisValue=kurtosis(dataPoints, fisher = True)
#     meanValue = mean(dataPoints)
#     medianValue = median(dataPoints)
#     stdValue = stdev(dataPoints)
#     moment1=moment(dataPoints, moment=1)
#     moment2=moment(dataPoints, moment=2)
#     moment3=moment(dataPoints, moment=3)
#     moment4=moment(dataPoints, moment=4)
#     temp1 = meanValue-medianValue
#     temp1 = 3*temp1
#     skewness=temp1/stdValue
#     cursor.find_one_and_update({"title":"processAllDatapoints"},{"$set":{"kurtosis":kurtosisValue,"skewness":str("%.3f" %skewness),"m1":str(moment1),"m2":str(moment2),"m3":str(moment3),"m4":str(moment4)}})
#     return HttpResponse("Kurtosis Value: "+str("%.3f" % kurtosisValue)+"<br>Skewness Value: "+str("%.3f" %skewness)+"<br>m1 : "+str(moment1)+"<br>m2 : "+str(moment2)+"<br>m3 : "+str(moment3)+"<br>m4 : "+str(moment4))