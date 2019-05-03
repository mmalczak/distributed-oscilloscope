import threading
import cmd
import os
from proxy import *


class CommandsThread(threading.Thread):

    def __init__(self, cmd):
        threading.Thread.__init__(self)
        self.cmd = cmd

    def run(self):
        self.cmd.cmdloop()


class Commands(cmd.Cmd):

    def __init__(self, zeroconf_service, zeroconf_info, ADC_name,
                 server_proxy):
        super(Commands, self).__init__()
        self.zeroconf_service = zeroconf_service
        self.zeroconf_info = zeroconf_info
        self.ADC_name = ADC_name
        self.server_proxy = server_proxy

    def do_rpc_addr(self, line):
        print("xmlrpc.client.ServerProxy(" + '"' + "http://" +
              os.popen("ifconfig| grep inet").read().split()[1] + ":" +
              str(8000) + "/" + '"' + ").")

    def do_exit(self, line):
        if(self.zeroconf_service is not None):
            self.zeroconf_service.unregister_service(self.zeroconf_info)
        else:
            proxy = get_proxy(self.server_proxy.proxy_addr)
            proxy.remove_service(self.ADC_name)
        os._exit(1)
