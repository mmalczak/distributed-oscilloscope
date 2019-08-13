.. _introduction:

-----------
Introduction
-----------

The Distributed Oscilloscope (DO) is an application allowing to synchronously monitor analog signals in a distributed system, independently of the distance.

The idea of the DO is presented in :numref:`fig_problem_description`.

.. figure:: graphics/problem_description.png
   :name: fig_problem_description
   :width: 400pt
   :align: center
   :alt: alternate text
   :figclass: align-center

   Synchronous acqusition of distributed data

Analog signals from various digitizers are time-stamped, aligned to the same moment in time and sent to the Graphical User Interface (GUI), to be displayed. The synchronization is obtained using the White Rabbit Trigger Distribution `(WRTD)  <https://www.ohwr.org/project/wrtd>`_ project.


Architecture
===========

The DO constits of three layers:

* `User Applications`_
* `DO Server`_
* `Device Application`_


The structure of the DO is presented in :numref:`fig_DO_basic_schematics`. 

.. figure:: graphics/DO_basic_schematics.png
   :name: fig_DO_basic_schematics
   :width: 400pt
   :align: center
   :alt: alternate text
   :figclass: align-center

   Structure of the DO 

The DO Server is a proxy between Devices and Users Applications. In a single network there could be one Server, multiple Users and multiple devices. The applications typically are run on different machines, but it is not a restriction.




================
`User Applications`_
================

There are currently two User Applications available:

* GUI --- it is designed to resemble standard oscilloscope.
* testbench --- it is used to test the DO Server and the Device Applications as well as to perform statistical measurements of data acquisition speed and of the precision of the synchronization.

The User Applications serve the following purposes:

* Sending the configuration settings
* Collecting and processing the acquisition data

The Device Applications never communicate with the devices directly, always through the DO Server. This allows to hide all the implementation details and to provide a common interface for various types of applications.
The details how to write User Applications are described in section :ref:`user_applications`

================
`DO Server`_
================

The DO Server is a central unit responsible for managing all the connections, preprocessing the data and providing a common interface for connected applications.


================
`Device Application`_
================

Device applications provide a direct access to hardware resources. At the moment the only available devices are ADCs supported by the `adc-lib <https://ohwr.org/project/adc-lib>`_.


Hardware setup
==============

The minimum hardware requirements necessary to demonstrate features of the DO are the following:

* computer with minimum 2 PCIe slots and CentOS 7.6.1810

.. note::

    The DO is designed to run each application on different machine. However, it is possible ot run them on the same machine. Also, to make the DO really distributed, the ADC cards should be installed in different locations in different machines. The described hardware setup should serve only as a demonstrator.


.. note::
    CentOS 7.6.1810 guaranties that all the drivers will function properly. However, it is possible to use the DO with different OS. In case of the machines where the Server and the GUI are run, the Linux version does not matter.


* `White Rabbit Switch <https://www.ohwr.org/projects/white-rabbit/wiki/switch>`_
* 2 `SPEC 150T <https://ohwr.org/project/spec/wikis/home>`_ boards 
  
    .. important::

        The DO will work only with SPEC 150T version. Be carrefoul not to purchase standard SPEC 45T version.
* 2 `FMC ADC 100M 14b 4cha <https://www.ohwr.org/project/fmc-adc-100m14b4cha/wikis/home>`_ boards
* 2 fibres -- in order to demonstrate the synchronization features, the fibres could be of different lenghts
* 4 SFP cages
* signal generator

The minimum hardware setup of the DO is presented in :numref:`fig_hardware_setup`.

.. figure:: graphics/hardware_setup.png
   :name: fig_hardware_setup
   :width: 250pt
   :align: center
   :alt: alternate text
   :figclass: align-center

   Minimum hardware setup for the DO 



The SPEC boards togehter with ADC cards should be installed in PCIe slots of the computer and connected to any of White Rabbit switch Channels using the SFP cages and fibres. In order to be able to demonstrate the synchronization accuracy, the same signal from the generator should be provided to both ADCs, with cables of the same length or precisely known lengths.

