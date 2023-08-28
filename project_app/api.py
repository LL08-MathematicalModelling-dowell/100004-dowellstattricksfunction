from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import APIView
from .serializers import inputfields
from .dowellconnection import dowellconnection
from .stattricks import dowellstattricks
from .event_creation import get_event_id
from .apikey import processApikey
from datetime import datetime
import json
import pandas as pd
import numpy as np
import threading

def generate_dict(csv_file):
    df = pd.read_csv(csv_file)
    data = df.values.tolist()

    dictionary = {}
    for row in data:
        key = row[0]
        values = row[1:]
        dictionary[key] = values
    return dictionary

def np_encoder(object):
    if isinstance(object, np.generic):
        return object.item()

def insertion_thread(title,processId,seqId,poisson_data,normal_data):
    event_id = get_event_id()
    field = {
                    "title": title,
                    "Process_id": processId,
                    "processSequenceId": seqId,
                    "poisson_dist": poisson_data,
                    "normal_dist": normal_data,
                    "event_data": event_id
                }

    dowellconnection("dowellfunctions", "bangalore", "dowellfunctions", "stattricks", "stattricks", "1197001", "ABCDE", "insert", field, "nil")
    return event_id


class publicAPI(APIView):
    def post(self,request):
        request_data = json.loads(request.body)
        if "api_key" in request_data:
            api_key = request_data.get('api_key')
            data = processApikey(api_key)
            api_resp = json.loads(data)
            if api_resp['success'] is True:
                credit_count = api_resp['total_credits']
                if credit_count>=0:
                    serializer = inputfields(data=request.data)
                    serializer.is_valid(raise_exception=True)

                    Process_id = serializer.validated_data['Process_id']
                    processSequenceId = serializer.validated_data['processSequenceId']
                    title = serializer.validated_data['title']
                    # csv_path = serializer.validated_data['CSV']
                    seriesvalues = serializer.validated_data['seriesvalues']


                    current_datetime = datetime.now()

                    # if csv_path:
                    #     csv_file_data = open(csv_path,'rb')
                    #     if not csv_path.name.endswith('.csv'):
                    #         return Response('File is not a CSV')
                    #     else:
                    #         csv_data = self.generate_dict(csv_file_data)
                    #         json_d = json.dumps(csv_data)
                    #         print("json is--->",json_d)

                    #         switch_actions = {
                    #                             'qrImageData': lambda: dowellstattricks(csv_data),
                    #                             'combinedObservations': lambda: dowellstattricks(csv_data)
                    #                         }

                    # else:
                    field={"Process_id" : Process_id}
                    res = dowellconnection("dowellfunctions","bangalore","dowellfunctions","stattricks","stattricks","1197001","ABCDE","fetch",field,"nil")
                    result = json.loads(res)

                    if not result['data']:
                        seriesvalues = {
                                            key: np.array(value) for key, value in seriesvalues.items()
                                        }

                        qrImageData, combinedObservations = dowellstattricks(seriesvalues)
                        qrImage_json = json.dumps(qrImageData, default=np_encoder)
                        combinedObs_json= json.dumps(combinedObservations, default=np_encoder)

                        thread1 = threading.Thread(target=insertion_thread,args=(title,Process_id,processSequenceId,qrImage_json,combinedObs_json))

                        thread1.start()
                        thread1.join()

                        print("Insertion thread execution successful")


                        return Response({
                            "msg": "Successfully generated the results",
                        "title": title,
                        "Process_id": Process_id,
                        "processSequenceId": processSequenceId,
                        "poison case results": qrImageData,
                        "normal case results": combinedObservations,
                        "created on": current_datetime.strftime('%Y-%m-%d %H:%M:%S')
                    })

                    else:
                        return Response("Process Id already in use. Please enter a different Process Id & try again.")
                else:
                    Response({"sucesss":False, "message":api_resp['message'], "total credits":api_resp['total_credits']},status=status.HTTP_200_OK)
            elif api_resp['success'] is False:
                return Response({"sucesss":False, "message":api_resp['message'], "total credits":api_resp['total_credits']},status=status.HTTP_200_OK)

        else:
            return Response({"success":False, "msg":"Provide a valid API key"},status=status.HTTP_403_FORBIDDEN)


    def get(self, request, format=None):
        request_data = json.loads(request.body)
        if "api_key" in request_data:
            api_key = request_data.get('api_key')
            data = processApikey(api_key)
            api_resp = json.loads(data)
            if api_resp['success'] is True:
                credit_count = api_resp['total_credits']
                if credit_count>=0:
                    if not request_data:
                        return Response("Process id required")
                    else:
                        Process_id = request_data["Process_id"]
                        processId = {"Process_id" : Process_id}
                        res=dowellconnection("dowellfunctions","bangalore","dowellfunctions","stattricks","stattricks","1197001","ABCDE","fetch",processId,"nil")
                        result=json.loads(res)
                        if result:
                            data = result['data'][0]
                            print(data)

                            poisson_json = json.loads(data["poisson_dist"])
                            poisson_data = poisson_json

                            normal_json = json.loads(data["normal_dist"])
                            normal_data = normal_json

                            return Response({
                                                "msg" : "Fetched data successfully",
                                                "_id" : data["_id"],
                                                "Process_id" : data["Process_id"],
                                                "title" : data["title"],
                                                "processSequenceId" : data["processSequenceId"],
                                                "poisson_dist" : poisson_data,
                                                "normal_dist" : normal_data
                                            })
                        else:
                            return Response("Requested data was not found. Enter the correct process id")

                else:
                    Response({"sucesss":False, "message":api_resp['message'], "total credits":api_resp['total_credits']},status=status.HTTP_200_OK)
            elif api_resp['success'] is False:
                return Response({"sucesss":False, "message":api_resp['message'], "total credits":api_resp['total_credits']},status=status.HTTP_200_OK)

        else:
            return Response({"success":False, "msg":"Provide a valid API key"},status=status.HTTP_403_FORBIDDEN)

class stattricksAPI(APIView):
    def post(self,request):
        serializer = inputfields(data=request.data)
        serializer.is_valid(raise_exception=True)

        Process_id = serializer.validated_data['Process_id']
        processSequenceId = serializer.validated_data['processSequenceId']
        title = serializer.validated_data['title']
        # csv_path = serializer.validated_data['CSV']
        seriesvalues = serializer.validated_data['seriesvalues']


        current_datetime = datetime.now()

        # if csv_path:
        #     csv_file_data = open(csv_path,'rb')
        #     if not csv_path.name.endswith('.csv'):
        #         return Response('File is not a CSV')
        #     else:
        #         csv_data = self.generate_dict(csv_file_data)
        #         json_d = json.dumps(csv_data)
        #         print("json is--->",json_d)

        #         switch_actions = {
        #                             'qrImageData': lambda: dowellstattricks(csv_data),
        #                             'combinedObservations': lambda: dowellstattricks(csv_data)
        #                         }

        # else:
        field={"Process_id" : Process_id}
        res = dowellconnection("dowellfunctions","bangalore","dowellfunctions","stattricks","stattricks","1197001","ABCDE","fetch",field,"nil")
        result = json.loads(res)

        if not result['data']:
            seriesvalues = {
                                key: np.array(value) for key, value in seriesvalues.items()
                            }
            print(seriesvalues)
            # switch_actions = {
            #                     'qrImageData': lambda: dowellstattricks(seriesvalues),
            #                     'combinedObservations': lambda: dowellstattricks(seriesvalues)
            #                 }

            # qrImageData = switch_actions.get('qrImageData', lambda: None)()
            # combinedObservations = switch_actions.get('combinedObservations', lambda: None)()
            qrImageData, combinedObservations = dowellstattricks(seriesvalues)
            qrImage_json = json.dumps(qrImageData, default=np_encoder)
            combinedObs_json= json.dumps(combinedObservations, default=np_encoder)

            thread1 = threading.Thread(target=insertion_thread,args=(title,Process_id,processSequenceId,qrImage_json,combinedObs_json))

            thread1.start()
            thread1.join()

            print("Insertion thread execution successful")


            return Response({
                "msg": "Successfully generated the results",
            "title": title,
            "Process_id": Process_id,
            "processSequenceId": processSequenceId,
            "poison case results": qrImageData,
            "normal case results": combinedObservations,
            "created on": current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        })

        else:
            return Response("Process Id already in use. Please enter a different Process Id & try again.")

        return Response({"msg": "No Data Found"},status=status.HTTP_404_NOT_FOUND)

    def get(self, request, format=None):
        request_data = json.loads(request.body)

        if not request_data:
            return Response("Process id required")
        else:
            Process_id = request_data["Process_id"]
            processId = {"Process_id" : Process_id}
            res=dowellconnection("dowellfunctions","bangalore","dowellfunctions","stattricks","stattricks","1197001","ABCDE","fetch",processId,"nil")
            result=json.loads(res)
            if result['data']:
                data = result["data"][0]
                poisson_json = json.loads(data["poisson_dist"])
                poisson_data = poisson_json

                normal_json = json.loads(data["normal_dist"])
                normal_data = normal_json

                return Response({
                                    "msg" : "Fetched data successfully",
                                    "_id" : data["_id"],
                                    "Process_id" : data["Process_id"],
                                    "title" : data["title"],
                                    "processSequenceId" : data["processSequenceId"],
                                    "poisson_dist" : poisson_data,
                                    "normal_dist" : normal_data
                                })
            else:
                return Response("Requested data was not found. Enter the correct process id")




class revisedAPI(APIView):
    def post(self,request):
        serializer = inputfields(data=request.data)
        serializer.is_valid(raise_exception=True)

        Process_id = serializer.validated_data['Process_id']
        processSequenceId = serializer.validated_data['processSequenceId']
        title = serializer.validated_data['title']
        # csv_path = serializer.validated_data['CSV']
        seriesvalues = serializer.validated_data['seriesvalues']
        current_datetime = datetime.now()

        field={"Process_id" : Process_id}
        res = dowellconnection("dowellfunctions","bangalore","dowellfunctions","stattricks","stattricks","1197001","ABCDE","fetch",field,"nil")
        result = json.loads(res)

        if not result['data']:
            seriesvalues = {
                                key: np.array(value) for key, value in seriesvalues.items()
                            }
        for key,value in seriesvalues.items():
            print("Processing list: ",key)

        chunk_size = 10
        chunk_count = len(value)//chunk_size

        for i in range(chunk_count):
            start_index = i*chunk_size
            end_index = (i+1)*chunk_size

            list_chunk = value[start_index:end_index]
            print("this list chunk is:", list_chunk)

        if len(value) % chunk_size!=0:
            start_index = chunk_count * chunk_size
            list_chunk = value[start_index:]
            print("Remaining elements result:", list_chunk)

        return Response({"List":list_chunk})



