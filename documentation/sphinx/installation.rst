.. _installation:

Installation
===========

===========
Applications
===========

In order to use the DO, the python version 3.6 is required.

All the necessary files are available in the `DistOsc <https://ohwr.org/project/distributed-oscilloscope/wikis/uploads/2f7d710befa8b3dc66dff3a82a3e5abb/DistScope.zip>`_.

Download the file and go to its location. In order to unzip the file, issue the following commands.

.. code-block:: console

    $ unzip DistScope.zip
    $ cd DistScope/

In the folder there are DistributedOscilloscope package and three requirements files, for the DistOscServer, ADC_lib_node and the GUI.

Before installing the Distributed Oscilloscope and the requirements, create a python virtual environment in order to avoid issues with packages versions.

.. code-block:: console

    $ python -m venv do_venv
    $ source do_venv/bin/activate

In order to install the Distributed Oscilloscope, issue:

.. code-block:: console

    $ pip install DistributedOscilloscope-1.0.0.tar.gz

Now, three available applications could be started form the terminal:

* dist_osc_gui
* dist_osc_server
* dist_osc_adc_node


Depending on the application that will be run on the given machine, install appriopriate set of requirements, issuing:

.. code-block:: console

    $ pip install -r requirements*.txt

In order to display help for each of the applications, type the name of the applications with '-h' option, e.g.:

.. code-block:: console

    $ dist_osc_server -h


===========
Drivers
===========







