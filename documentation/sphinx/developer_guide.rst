.. _developer_guide:

Developer Guide
==================

As described in :ref:`introduction`, DO currently supports two types of User
Applications:

* GUI
* testbench

and one type of Device Application available:

* ADCs supported by the `adc-lib <https://ohwr.org/project/adc-lib/wikis/home>`_.

Depending on the needs of the user, different applications could be developed.
In order to do this, the following tasks have to be performed:

* write application specific code
* update or add a new model of the application in the Server
* establish communication with the Server using the existing interface and if
  necessary, update the interface

The section expalins briefly the communication patterns, existing interfaces
and models of applications as well as the changes that have to be done to be
able to add a new application.


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
the Server and the Server sends the RPC requests to the Device Application.

Publisher/subscriber pattern is used for sending acquisition data and
notifications about the availability of nodes. Device Applications send the
notifications and acquisition data to the Server, which propagates them to
User Applications.

There are two ways of providing the information about the presence of the
Device Application to the Server:

* if the IP address of the server is provided during the startup of the
  Device Application, the notification is sent over the standard communication
  channel -- the most bottom one in :numref:`fig_do_communication`.
* using Zeroconf, which automatically discovers the IP address of the Server.
  However, the Zeroconf Listener in the Server also uses
  the publisher/subscriber pattern for internal communication.

When implementing the :ref:`interfaces` for new applications, the communication
patterns should not be changed.


=======================
Applications Models
=======================

The Server contains models of User Applications and Device Applications.
Interaction with the applications is done through interaction with the models,
using provided :ref:`interfaces`.

User Application model
-----------------------

The User Applications model is similar to standard oscilloscope. The
functionality of the User Applications depends on the changes made in the
model, that is:

* channels selection
* triggers selection
* acquisition settings (e.g. length of acquisition, position of the trigger...)

There are no forseen changes in the User Application model when adding a new
User Application.

New applications should make use of the
:ref:`server_interface` and implement the
:ref:`user_application_interface`.

Device Application model
-----------------------

The Device Application model reflects the functionalities of the particular
device. In case of the ADC, the functionalities are the following:

* channels settings
* triggers settings
* acquisition settings

The main reason for adding a new Device Application is adding a new type of
device. In that case, the model of the application,
:ref:`device_application_interface` and
:ref:`server_interface`
should be modified.


.. _interfaces:

===============
Interfaces
===============

The Server provides interfaces for User Applications and Devices Applications.
Each new application should use these interfaces. If the interfaces don't
meet the requirements for new application, they should be modified.


.. _server_interface:

Server Interface
------------------

.. todo::

    Since currently the only available device is and ADC, the interface
    provides functions for interaction with ADCs. If in the future other
    types of devices will be supported, the interface should be made more
    general or extended.

.. automodule:: server.expose

.. autoclass:: server.expose.Expose
    :members:


.. _user_application_interface:

User Application Interface
----------------------------

The following methods are used to receive information about availablility of
of the devices and the data.

.. autoclass:: applications.pyqt_app.GUI.GUI_Class
    :members: register_ADC, unregister_ADC, set_ADC_available,
                set_ADC_unavailable, update_data



.. _device_application_interface:

Device Application Interface
----------------------------

.. autoclass:: nodes.adc_lib_node.server_expose.ServerExpose
    :members: __getattr__, set_server_address

.. autoclass:: nodes.adc_lib_node.devices_access.DevicesAccess
    :members: set_user_app_name, set_WRTD_master, configure_adc_parameter,
                get_current_adc_conf, configure_acquisition,
                run_acquisition
