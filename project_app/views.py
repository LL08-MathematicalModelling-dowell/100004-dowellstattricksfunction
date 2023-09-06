from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from bson import ObjectId
from .dowellconnection import dowellconnection
from .dowellstattricks import dowellstattricks
from .serializers import inputfields
from .event_creation import get_event_id
from datetime import datetime
import numpy as np
import pandas as pd
import json
import requests
# import threading

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def np_encoder(object):
    if isinstance(object, np.generic):
        return object.item()

def default(request):
    return render(request,"dashboard.html")

def form(request):
    return render(request,"insertDataForm.html")

#OLD STATTRICKS API
@api_view(['POST',])
def stattricks_api(request):

    if request.method=="POST":
        current_datetime = datetime.now()
        # startHours=current_datetime.hour
        # startMinutes=current_datetime.minute
        # startSeconds=current_datetime.second

        response=request.data

        Process_id = response["Process_id"]
        processSequenceId = response["processSequenceId"]
        seriesvalues = response["seriesvalues"]
        title=response["title"]
        field={"Process_id" : Process_id}
        res = dowellconnection("dowellfunctions","bangalore","dowellfunctions","stattricks","stattricks","1197001","ABCDE","fetch",field,"nil")
        result = json.loads(res)

        if not result['data']:

            qrImageData, combinedObservations = dowellstattricks(seriesvalues)

            # endHours=current_datetime.hour
            # endMinutes=current_datetime.minute
            # endSeconds=current_datetime.second
            # processHours=endHours-startHours
            # processMinutes=endMinutes-startMinutes
            # processSeconds=endSeconds-startSeconds
            # processTime=str(str(processHours)+":"+str(processMinutes)+":"+str(processSeconds+1))
            # qrImageData["processTime"]=processTime
            event_data =  get_event_id()
            field = {
                     "event_data": event_data,
                     "title":title,
                     "Process_id":Process_id,
                     "processSequenceId":processSequenceId,
                     "poisson_dist":qrImageData,
                     "normal_dist":combinedObservations
                     }


            dowellconnection("dowellfunctions","bangalore","dowellfunctions","stattricks","stattricks","1197001","ABCDE","insert",field,"nil")
            return Response({
                             "msg":"Successfully generated the results",
                             "title":title,
                             "Process_id":Process_id,
                             "processSequenceId":processSequenceId,
                             "poison case results":qrImageData,
                             "normal case results":combinedObservations,
                             "created on":current_datetime.strftime('%Y-%m-%d %H:%M:%S')
                             })
        else:
            return Response("Process Id already in use. Please enter a different Process Id & try again.")

    else:
        return Response({"msg": "No Data Found"},status=status.HTTP_404_NOT_FOUND)


#INSERT & CALCULATE FROM EXPERIMENTAL FRONTEND
def insertQrImageData(request):
    current_datetime = datetime.now()

    if request.method=="POST":

        serializer = inputfields(data=request.POST)
        serializer.is_valid(raise_exception=True)

        Process_id = serializer.validated_data['Process_id']
        processSequenceId = serializer.validated_data['processSequenceId']
        title = serializer.validated_data['title']
        # seriesvalues = serializer.validated_data['seriesvalues']
        # Process_id = int(request.POST.get("Process_id"))
        # processSequenceId = request.POST.get("processSequenceId")
        numOfValues = request.POST.get("numOfValues")
        title=request.POST.get("title")
        seriesvalues={}
        for i in range(int(numOfValues)):
            temporary=request.POST.get("1000"+str(i+1))
            temporary2=temporary.split(',')
            temporary3=[int(i) for i in temporary2]
            seriesvalues["1000"+str(i+1)]=temporary3
        field={"Process_id" : Process_id}
        res = dowellconnection("dowellfunctions","bangalore","dowellfunctions","stattricks","stattricks","1197001","ABCDE","fetch",field,"nil")
        result = json.loads(res)

        if not result['data']:
            seriesvalues={}
            for i in range(int(numOfValues)):
                temporary=request.POST.get("1000"+str(i+1))
                temporary2=temporary.split(',')
                temporary3=[int(i) for i in temporary2]
                seriesvalues["1000"+str(i+1)]=temporary3

            qrImageData, combinedObservations = dowellstattricks(seriesvalues)
            qrImage_json = json.dumps(qrImageData, default=np_encoder)
            combinedObs_json= json.dumps(combinedObservations, default=np_encoder)

            event_data =  get_event_id()
            field = {
                     "event_data": event_data,
                     "title":title,
                     "Process_id":Process_id,
                     "processSequenceId":processSequenceId,
                     "poisson_dist":qrImage_json,
                     "normal_dist":combinedObs_json
                     }


            dowellconnection("dowellfunctions","bangalore","dowellfunctions","stattricks","stattricks","1197001","ABCDE","insert",field,"nil")

            return render(request,'viewInsertedData.html',{'data':field})
        else:
            return HttpResponse("Process Id already in use. Please enter a different Process Id & try again.")
    else:
        return HttpResponse("No Data Found")

#PREVIOUS ANSWER
def fetchDataForm(request):
    return render(request,"fetchDataForm.html")


def fetchData(request):
    if request.method=="POST":
        Process_id = int(request.POST.get("id"))
        processId = {"Process_id":Process_id}
        res=dowellconnection("dowellfunctions","bangalore","dowellfunctions","stattricks","stattricks","1197001","ABCDE","find",processId,"nil")
        result=json.loads(res)
        if result:
            data=result['data']
            print(data)
            return render(request,'viewData.html',{'data':data})
        else:
            return HttpResponse("The requested data was not found. Enter correct process id")
    else:
        return HttpResponse("No Data Found")


#CALCULATE FROM SPREADSHEET
## function to generate a dictionary in the format accepted by stattricks API
def generate_dict(table):
    dictionary = {}
    for row in table:
        key = row[0]
        values = row[1:]
        dictionary[key] = values
    return dictionary

def uploadfileform(request):
    return render(request,"uploadfile.html")

def uploadfile(request):
    if request.method == 'POST':
        title=request.POST.get("title")
        Process_id = int(request.POST.get("Process_id"))
        processSequenceId = request.POST.get("processSequenceId")
        csv_file = request.FILES['csvfile']

        if csv_file:
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File is not a CSV')
                return HttpResponseRedirect(reverse("uploadfile"))
            else:
                # convert csv data to pandas dataframe
                df = pd.read_csv(csv_file)
                #convert the df into a list
                t = df.values.tolist()
                data = generate_dict(t)
                json_d = json.dumps(data)
                print("json is--->",json_d)
                qrImageData, combinedObservations = dowellstattricks(data)

                results = {
                             "title":title,
                             "Process_id":Process_id,
                             "processSequenceId":processSequenceId,
                             "poisson_dist":qrImageData,
                             "normal_dist":combinedObservations
                             }

                # dowellconnection("dowellfunctions","bangalore","dowellfunctions","stattricks","stattricks","1197001","ABCDE","insert",results,"nil")


                return render(request,'viewInsertedData.html',{'data':results})
        else:
            messages.error(request, 'Failed to upload file')
            return redirect(reverse("uploadfile"))

    else:
        return render(request, 'uploadfile.html')


# def findDataForm(request):
#     return render(request,"findDataForm.html")

# def findData(request):
#     if request.method=="POST":
#         Process_id = int(request.POST.get("id"))
#         processId = {"Process_id":Process_id}
#         res=dowellconnection("FB","bangalore","blr","QR_IMAGE","qr","123456","ABCDE","fetch",processId,"nil")
#         result=json.loads(res)
#         if result:
#             data=result['data']
#             data_1={}
#             data_1['data']=data[0]
#             print("data is: ",data_1)
#             return render(request,'viewData.html',data_1)
#         else:
#             return HttpResponse("The requested data was not found. Enter correct process id")
#     else:
#         return HttpResponse("No Data Found")
