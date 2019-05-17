import paramiko
import os
import time

def start_adc(port, pci):
    host = 'spechost'
    key_filename = '/home/milosz/.ssh/known_hosts'
    client = paramiko.SSHClient()
    ssh_config_file = os.path.expanduser("/home/milosz/.ssh/config")
    if os.path.exists(ssh_config_file):
        conf = paramiko.SSHConfig()
        with open(ssh_config_file) as f:
            conf.parse(f)
        host_config = conf.lookup(host)
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username='root')
    (stdin, stdout, stderr) = client.exec_command("python3.6 "
        "/home/Projects/distributed_oscilloscope/software/fec/adc_client.py "
        "--ip_server 128.141.79.22 --port " +str(port) + " --pci_addr " + 
        str(pci))
    #(stdin, stdout, stderr) = client.exec_command("ps -A | grep python")
    #for line in stdout.readlines():
    #    print(line.split()[0])

