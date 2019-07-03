from general import rpc_pb2
from general import rpc_pb2_grpc

import grpc
from concurrent import futures

class RPC_req(rpc_pb2_grpc.RPC_reqServicer):

    def register_ADC(self, request, context):
        return rpc_pb2.reply(value="bleble")


import time
import logging
_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class GRPC_Server:
    def __init__(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        rpc_pb2_grpc.add_RPC_reqServicer_to_server(RPC_req(), self.server)
        self.server.add_insecure_port('128.141.79.50:50051')
        self.server.start()
