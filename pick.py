import pickle

# data = input('masukkan kalimat anda = ')

def pack(data):
    data_pickle = pickle.dumps(data)
    # print(data_pickle)
    return data_pickle

def unpack(data):
    pickle_data = pickle.loads(data)
    return pickle_data

# coba = pack(data)
# unpack(bytes(coba))