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



.. todo:

Explain the hardware setup
