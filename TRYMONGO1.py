import json
import requests

url = 'http://100002.pythonanywhere.com/'
url = 'http://100002.pythonanywhere.com/'

def insert(x):
	data={
	  "cluster": "FB",
	  "database": "mongodb",
	  "collection": "QR_IMAGE",
	  "document": "qr",
	  "team_member_ID": "123456",
	  "function_ID": "ABCDE",
	  "command": "insert",
	  "field": x,
	  'update_field':{
	    "name": "Joy update",
	    "phone": "123456",
	    "age": "26",
	    "language": "Englis",

	   },
	  "platform": "bangalore",
	}
	headers = {'content-type': 'application/json'}
	response = requests.post(url, json =data,headers=headers)
	print(response.text)