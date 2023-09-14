import requests

def processApikey(api_key):
    url = f'https://100105.pythonanywhere.com/api/v3/process-services/?type=api_service&api_key={api_key}'
    print(api_key)
    print(url)
    payload = {
        "service_id" : "DOWELL10021"
    }

    response = requests.post(url, json=payload)
    print("CREDIT SYSTEM RESPONSE-------->", response)
    return response.text