import INPUT_mongo
import FETCH_QR_mongo

data = {"Process_id":123789123}

#INPUT_mongo.insert(data)

response = FETCH_QR_mongo.fetch(123789123)

print(response)