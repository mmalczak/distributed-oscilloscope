.. _usage:

Usage of the GUI
================


The GUI application is presented in :numref:`fig_gui`.

.. figure:: graphics/GUI.png
   :name: fig_gui
   :align: center
   :alt: alternate text
   :figclass: align-center
    
   Screenshot of the GUI application


Channels selection
------------------

Just like in standard oscilloscope, there is a possibility of observing up to
4 channels. Any channel of any available ADC can be connected to the particular
channel of the GUI. 

.. figure:: graphics/GUI_channels_selection.png
   :name: fig_gui_chann_sel
   :align: center
   :alt: alternate text
   :figclass: align-center
    
   Selection of GUI channels 


Triggers selection
------------------

The ADCs could be triggered either by external trigger pulse or when the signal
of the observed channel crosses the threshold value (internal trigger).

.. figure:: graphics/GUI_triggers_selection.png
   :name: fig_gui_trigg_sel
   :width: 120pt
   :align: center
   :alt: alternate text
   :figclass: align-center
    
   Selection of trigger type 


Internal trigger
^^^^^^^^^^^^^^^^

If the internal trigger is selected, the GUI could be triggered on any channel
to which a signal is connected. 

.. figure:: graphics/GUI_internal_trigger.png
   :name: fig_gui_int_trigg
   :width: 120pt
   :align: center
   :alt: alternate text
   :figclass: align-center
    
   Selection of internal trigger 


External trigger
^^^^^^^^^^^^^^^^

If the external trigger is selected, the GUI could be triggered by the external
trigger input of any connected ADC.

.. figure:: graphics/GUI_external_trigger.png
   :name: fig_gui_ext_trigg
   :width: 180pt
   :align: center
   :alt: alternate text
   :figclass: align-center
    
   Selection of external trigger 


Channels settings
-----------------

Currently available channels settings are the following:

* range
* termination
* offset

.. figure:: graphics/GUI_channels_settings.png
   :name: fig_gui_chann_sett
   :width: 220pt
   :align: center
   :alt: alternate text
   :figclass: align-center
    
   Channels settings 


Trigger settings
----------------

Currently available trigger settings are the following:

* polarity
* delay
* threshold (in case of internal trigger)

.. figure:: graphics/GUI_trigger_settings.png
   :name: fig_gui_trigg_sett
   :width: 120pt
   :align: center
   :alt: alternate text
   :figclass: align-center
    
   Trigger settings 


Run control
---------------

There are two available modes:

* single acquisition
* continuous acquisition

.. figure:: graphics/GUI_run_control.png
   :name: fig_gui_run_control
   :width: 120pt
   :align: center
   :alt: alternate text
   :figclass: align-center
    
   Run control 


Acquisition settings
--------------------

Acquisition settings allow modifying the acquisition time and position of the
trigger. Position of the trigger is given in percentage of the acquisition time.

.. figure:: graphics/GUI_acquisition_settings.png
   :name: fig_gui_acq_set
   :width: 220pt
   :align: center
   :alt: alternate text
   :figclass: align-center
    
   Acquisition settings 
