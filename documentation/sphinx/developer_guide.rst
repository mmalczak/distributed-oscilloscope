.. _developer_guide:

Developer Guide
==================

As described in :ref:`introduction`, currently there are two types of User
Applications available:

* GUI
* testbench

and one type of Device Application available:

* ADCs supported by the `adc-lib <https://ohwr.org/project/adc-lib/wikis/home>`_.

This section provides guidelines on how to develop new applications for the
Distributed Oscilloscope.

The Server provides interfaces for User Applications and Devices Applications.
Each new application should use these interfaces. If the interfaces don't
meet the requirements for the new application, they should be modified.

In order to explain the interfaces, the communication patterns used in the DO
have to be explained before.

========================
Communication in the DO
========================

The schematics of the communication patterns used in the Distributed
Oscilloscope are presented in :numref:`fig_do_communication`.

.. figure:: graphics/DO_communication.png
   :name: fig_do_communication
   :width: 800pt
   :align: center
   :alt: alternate text
   :figclass: align-center

   Schematics of communications patterns in the Distributed Oscilloscope


In the Distributed Oscilloscope there are two messaging patterns used to
communicate the nodes:

* request/reply pattern
* publisher/subscriber pattern

Request/reply pattern is used to implement Remote Procedure Calls (RPC), which
allow to control the behaviour of other application in a reliable way.
The User Applications control the behaviour of the Distributed Oscilloscope,
using a Server as a proxy. Therefore, the User Applications send RPC request to
the Server and the Server sends the RPC requests to the ADC.

Publisher/subscriber pattern is used for sending acquisition data and
notifications about the availability of nodes. Device Applications send the
notifications and acquisition data to the Server, which propagates them to the
User Applications.
There are two ways of sending the notifications to the Server about the
presence of the Device Application:

* if the IP address of the server is provided during the startup of the
  Device Application, the notification is sent over the standard communication
  channel the most bottom one in :numref:`fig_do_communication`.
* using Zeroconf, which automatically discovers the IP address of the Server.
  However, the Zeroconf Listener in the Server also uses
  the publisher/subscriber pattern for internal communication.


======================
Server Interface
======================

.. todo::

    Since currently the only available device, is and ADC, the interface
    provides functions for interaction with the ADCs. If in the future other
    types of devices will be supported, the interface should be made more
    general or extended.

.. automodule:: server.expose

.. autoclass:: server.expose.Expose
    :members:



User Applications
------------------








.. autoclass:: server.connection_manager.ConnectionManager

.. autoclass:: server.user_app.UserApplication


.. todo::

    describe the interface of the server, for the GUI and for the adc

    describe what is required to be set in the server

    describe how to add a new application, what is done by RPC, which
    information the user has to poll for

    describe as much as you can how to add a new type of device, you can write
    that when more deivces will be there it will be worth creatin a virtual
    class




