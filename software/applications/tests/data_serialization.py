import pickle 

def save_object(obj):
    with open('test.pkl', 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def read_object():
    with open('test.pkl', 'rb') as input:
        return pickle.load(input)
