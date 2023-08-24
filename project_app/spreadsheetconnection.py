import json
import requests


url = "http://uxlivinglab.pythonanywhere.com/"
#url = 'http://127.0.0.1:8000/'

def spreadsheetconnection(cluster,platform,database,collection,document,team_member_ID,function_ID,command,field,update_field):
    
    payload={
      "cluster": cluster,
      "platform": platform,
      "database": database,
      "collection": collection,
      "document": document,
      "team_member_ID": team_member_ID,
      "function_ID": function_ID,
      "command": command, # 'fetch_db_names' for getting the database nmaes
      "field": field,
      "update_field":update_field
       }
    
    headers = {'content-type': 'application/json'}
    
    try :
      response = requests.post( url, headers=headers, json=payload)
      print(json.loads(response.text))
      return json.loads(response.text)
    
    except:
      return "check your connectivity"
