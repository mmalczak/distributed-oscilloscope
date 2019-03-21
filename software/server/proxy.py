import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer


def get_proxy(addr):
    return xmlrpc.client.ServerProxy(addr)


