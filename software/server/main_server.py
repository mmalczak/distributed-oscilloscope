from oscilloscope import *
from service_management import *
from ADC_expose import *
from GUI_expose import *


def main():
    osc = Oscilloscope()
    thread_GUI_expose = ThreadGUI_Expose(osc)
    thread_GUI_expose.start()
    thread_ADC_expose = ThreadADC_Expose(osc)
    thread_ADC_expose.start()
    thread_zero_conf = ThreadZeroConf(osc)
    thread_zero_conf.start()


if __name__ == '__main__':
    main()
