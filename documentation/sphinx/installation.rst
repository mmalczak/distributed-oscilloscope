.. _installation:

Installation
=============


.. _inst_app:

=============
Applications
=============

.. important::

    To be able to access the ADC device, the :ref:`dependencies` have to be
    installed.

To use the DO, the python version 3.6 is required.



Before installing the Distributed Oscilloscope and the requirements, create a
python virtual environment to avoid issues with packages versions.

.. code-block:: console

    $ python -m venv do_venv
    $ source do_venv/bin/activate


To install the Distributed Oscilloscope, type: 

.. code-block:: console

    $ pip install https://ohwr.org/project/distributed-oscilloscope/wikis/uploads/96748e7016d163f85cfb146e661bdc3d/DistributedOscilloscope-1.0.0.tar.gz 

Now, three available applications could be started form the terminal:

* dist_osc_server
* dist_osc_gui
* dist_osc_adc_node

Each of the applications requires installation of dependencies. 


To install the dependencies for the Server, issue: 

.. code-block:: console

    $ pip install -r https://ohwr.org/project/distributed-oscilloscope/raw/master/software/DistributedOscilloscope/server/requirements.txt 

To install the dependencies for the GUI, issue: 

.. code-block:: console

    $ pip install -r https://ohwr.org/project/distributed-oscilloscope/raw/master/software/DistributedOscilloscope/applications/pyqt_app/requirements.txt 

To install the dependencies for the ADC node, issue: 

.. code-block:: console

    $ pip install -r https://ohwr.org/project/distributed-oscilloscope/raw/master/software/DistributedOscilloscope/nodes/adc_lib_node/requirements.txt 


To display help for each of the applications, type the name of the applications
with '-h' option, e.g.:

.. code-block:: console

    $ dist_osc_server -h


.. _dependencies:

=============
Dependencies
=============


To be able to access the ADC device, the following drivers need to be loaded:

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

To be able to access ADC device and WRTD, the following libraries have to be
installed on the machine running the :ref:`adc_application`:

* adc-lib:
    https://ohwr.org/project/adc-lib/wikis/home

* WRTD:
    https://www.ohwr.org/project/wrtd/wikis/home


After installing the drivers and the libraries, the SPEC150T-based FMC_ADC
reference design has to be loaded. You can find the reference design
`here <https://wrtd.readthedocs.io/en/latest/ref_spec_fmc_adc.html#spec150t-ref-adc>`_. 

.. todo::
    Reset mockturtle CPUs
    Enable WRTD trigger in the adc-lib




