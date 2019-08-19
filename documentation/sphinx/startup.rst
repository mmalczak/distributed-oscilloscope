.. _startup:


Starting Applications 
======================

The GUI (:ref:`user_application_intro`) and the :ref:`do_server_intro` can be
run on any Linux machine with python3.6. Before starting the
ADC application (:ref:`device_application_intro`), all the dependencies,
described in section :ref:`dependencies`, have to be installed.

The first application that has to be run is the Server. When the Server is
already started, GUIs and ADC nodes can be run in any order. 


Before starting any of the applications, start the virtual environment and
install the Distributed Oscilloscope, as described in section :ref:`inst_app`.

.. _server_application:

Server Application
--------------------

To start the Server Application, run in terminal:

.. code-block:: console

    $ dist_osc_server 

Optional arguments:

* port_user -- port of the Server exposed to the User Application, default value -- 8003 
* port_device -- port of the Server exposed to the device, default value -- 8023

.. _gui:

GUI:
----------------

Before starting the GUI applications, find out what is the IP address of the
Server: SERVER_IP_ADDRESS. You can check it using the command:


.. code-block:: console
    
    $ ifconfig 


To start the GUI, run in terminal:

.. code-block:: console

    $ dist_osc_gui --ip_server SERVER_IP_ADDRESS 

Required arguments:

    * ip_server -- IP address of the Server

Optional arguments:

    * port -- port used on the current machine to listen for notifications and
      acquisition data, default value -- 8001
    * port_server -- port used on the Server to listen for the requests from
      the GUI, default value -- 8003

.. _adc_application:

ADC application:
------------------

If the Server and the ADC device are in different local networks, before
staring the ADC applications, find out what is the IP address of the Server:
SERVER_IP_ADDRESS. If the IP address of the Server is not provided, Zeroconf
will be used to automatically find out this information.

.. important::

    The Zeroconf will only work if the Server and the ADC are in the same local
    networks. Otherwise, the IP of the Server has to be provided manually.


To start the GUI, run in terminal:

.. code-block:: console

    $ dist_osc_adc_node --ip_server SERVER_IP_ADDRESS 

Optional arguments:
   
* ip_server -- IP address of the server 
* port_server -- port of the server used to listen for notifications and
  acquisition data, default value -- 8023 
* port -- port used on the current machine to listen for the requests from the
  Server, default value -- 8000
* pci_addr -- PCI address of the desired board, default value -- 0x01


Examples configuration:
-------------------------
Supposing that the IP address of the Server is 128.141.79.22, the ADCs are
installed in the same machine and the PCI slots where the ADCs are installed
are 01 and 02, the applications have to be started with following parameters:

.. code-block:: console

    $ dist_osc_server 
    $ dist_osc_gui --ip_server 128.141.79.22
    $ dist_osc_adc_node --ip_server 128.141.79.22 --port 8000 --pci_addr 01
    $ dist_osc_adc_node --ip_server 128.141.79.22 --port 8001 --pci_addr 02

