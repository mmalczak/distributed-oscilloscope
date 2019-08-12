.. _installation:

Installation
===========


.. _inst_app:

===========
Applications
===========

.. important::

    In order to be able to access the ADC device, the ref::`dependencies` have to be installed.

In order to use the DO, the python version 3.6 is required.



Before installing the Distributed Oscilloscope and the requirements, create a python virtual environment in order to avoid issues with packages versions.

.. code-block:: console

    $ python -m venv do_venv
    $ source do_venv/bin/activate


In order to install the Distributed Oscilloscope, type: 

.. code-block:: console

    $ pip install https://ohwr.org/project/distributed-oscilloscope/wikis/uploads/96748e7016d163f85cfb146e661bdc3d/DistributedOscilloscope-1.0.0.tar.gz 

Now, three available applications could be started form the terminal:

* dist_osc_server
* dist_osc_gui
* dist_osc_adc_node

Each of the applications requires installation of dependencies. 


In order to install the dependencies for the Server, issue: 

.. code-block:: console

    $ pip install -r https://ohwr.org/project/distributed-oscilloscope/raw/master/software/DistributedOscilloscope/server/requirements.txt 

In order to install the dependencies for the GUI, issue: 

.. code-block:: console

    $ pip install -r https://ohwr.org/project/distributed-oscilloscope/raw/master/software/DistributedOscilloscope/applications/pyqt_app/requirements.txt 

In order to install the dependencies for the ADC node, issue: 

.. code-block:: console

    $ pip install -r https://ohwr.org/project/distributed-oscilloscope/raw/master/software/DistributedOscilloscope/nodes/adc_lib_node/requirements.txt 


In order to display help for each of the applications, type the name of the applications with '-h' option, e.g.:

.. code-block:: console

    $ dist_osc_server -h


.. _dependencies:

===========
Dependencies
===========


In order to be able to access the ADC device, the following drivers need to be loaded:

* htvic.ko:
    https://gitlab.cern.ch/cohtdrivers/coht-vic

    commit: df07c670abcf87c967b634504417e482d5e3696b

* zio.ko, zio-buf-vmalloc.ko:
    https://www.ohwr.org/project/zio/wikis/home

    commit: d8bef4d89361194c2e5644e751add9bd9ffa106d

* fmc-adc-100m14b.ko:
    https://ohwr.org/project/fmc-adc-100m14b4cha-sw/wikis/home

    commit: 54a77d73df0ef321bbe74ef4acaf2776f6a142c5

* fmc.ko:
    https://gitlab.cern.ch/fvaga/fmc

    commit: ca386f42df6cdfe5fb6462215622ab2796c2ec75

* fpga-mgr.ko:
    https://gitlab.cern.ch/fvaga/fpga-manager

    commit: a3711f798ec4a17121c2f6ccfe160fde24a170bb

* spec.ko:
    https://gitlab.cern.ch/fvaga/fmc-spec

    commit: e893e85ff45dfa3b532295b0b86c5a276b2f221c

* mockturtle.ko:
    https://ohwr.org/project/mock-turtle/wikis/home

    commit: b07df87ad36d963beb7d7596b3dffa4221d6bd58



After installing the drivers, the WRTD reference design has to be loaded.

.. todo::

    Provide the link for the WRTD reference design



.. todo::
    What about init script




