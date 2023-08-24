from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import APIView, api_view
from .serializers import inputfields
from .dowellconnection import dowellconnection
from .stattricks import dowellstattricks
from .event_creation import get_event_id
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


class stattricksAPI(APIView):
    def post(self,request):
        serializer = inputfields(data=request.data)
        serializer.is_valid(raise_exception=True)

        Process_id = serializer.validated_data['Process_id']
        processSequenceId = serializer.validated_data['processSequenceId']
        title = serializer.validated_data['title']
        csv_path = serializer.validated_data['CSV']
        seriesvalues = serializer.validated_data['seriesvalues']
        current_datetime = datetime.now()

        if csv_path:
            csv_file_data = open(csv_path,'rb')
            if not csv_path.name.endswith('.csv'):
                return Response('File is not a CSV')
            else:
                csv_data = self.generate_dict(csv_file_data)
                json_d = json.dumps(csv_data)
                print("json is--->",json_d)

                switch_actions = {
                                    'qrImageData': lambda: dowellstattricks(csv_data),
                                    'combinedObservations': lambda: dowellstattricks(csv_data)
                                }

        else:
            field={"Process_id" : Process_id}
            res = dowellconnection("dowellfunctions","bangalore","dowellfunctions","stattricks","stattricks","1197001","ABCDE","fetch",field,"nil")
            result = json.loads(res)

        if not result['data']:
            seriesvalues = {
                                key: np.array(value) for key, value in seriesvalues.items()
                            }
            # print(seriesvalues)
            switch_actions = {
                                'qrImageData': lambda: dowellstattricks(seriesvalues),
                                'combinedObservations': lambda: dowellstattricks(seriesvalues)
                            }

            qrImageData = switch_actions.get('qrImageData', lambda: None)()
            combinedObservations = switch_actions.get('combinedObservations', lambda: None)()

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
            # dowellconnection("FB","bangalore","blr","input","input","1234567","ABCDE","insert",combinedObservations,"nil")

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

