from general.rpc_pb2 import RPC 

def serialize(data):
    rpc = RPC()
    rpc.function_name = data['function_name']

    if data['function_name'] == 'update_data':
        if(len(data['args']) == 4):
            rpc.args.timestamps.extend(data['args'][0])
            rpc.args.presamples = (data['args'][1]['presamples'])
            rpc.args.postsamples = (data['args'][1]['postsamples'])
            for channel_idx, channel_data in data['args'][2].items():
                rpc.args.data[channel_idx].values.extend(channel_data)
            rpc.args.unique_ADC_name = data['args'][3]
        else:
            for channel_idx, channel_data in data['args'][0].items():
                rpc.args.data2[channel_idx].values.extend(channel_data)
            for idx, prepost in data['args'][1].items():
                rpc.args.pre_post[idx].value.extend(prepost)
            for idx, offsets in data['args'][2].items():
                rpc.args.offsets[idx] = offsets
    elif data['function_name'] == 'register_ADC':
        if(len(data['args']) == 3):
            rpc.args.unique_ADC_name = data['args'][0]
            rpc.args.addr = data['args'][1]
            rpc.args.port = data['args'][2]
        else:
            rpc.args.unique_ADC_name = data['args'][0]
            rpc.args.number_of_channels = data['args'][1]
    elif data['function_name'] == 'unregister_ADC':
        rpc.args.unique_ADC_name = data['args'][0]



    data = rpc.SerializeToString()
    return data
 
def deserialize(data):
    rpc = RPC()
    rpc.ParseFromString(data)
    args = rpc.args
    function_name = rpc.function_name
    if function_name == 'update_data':
        if args.unique_ADC_name:
            timestamps = args.timestamps
            pre_post = {'presamples': args.presamples,
                        'postsamples': args.postsamples}
            data_arg = {}
            for key in args.data:
                data_arg[key] = args.data[key].values
            unique_ADC_name = args.unique_ADC_name
            args_dict = [timestamps, pre_post, data_arg, unique_ADC_name]
        else:
            data_arg = {}
            pre_post_samples = {}
            offsets = {}
            for key in args.data2:
                data_arg[key] = args.data2[key].values
            for key in args.pre_post:
                pre_post_samples[key] = args.pre_post[key].value
            for key in args.offsets:
                offsets[key] = args.offsets[key]
            args_dict = [data_arg, pre_post_samples, offsets]
    elif function_name == 'register_ADC':
        if args.addr:
            args_dict = [args.unique_ADC_name, args.addr, args.port]
        else:
            args_dict = [args.unique_ADC_name, args.number_of_channels]
    elif function_name == 'unregister_ADC':
        args_dict = [args.unique_ADC_name]




    message = {'function_name': function_name,
               'args': args_dict
              }
    return message 
 
