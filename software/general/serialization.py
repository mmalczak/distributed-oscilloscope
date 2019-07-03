import json 

def serialize(data):
    data = json.dumps(data)
    return data.encode('utf-8')
 
def deserialize(data):
    data = data.decode('utf-8')
    return json.loads(data)    
 
