ADC_CONF_100M14B4CHA_CHN_RANGE_N = 3

#List of known voltage ranges to be used with the configuration option
#ADC_CONF_CHN_RANGE

#enum adc_configuration_100m14b4cha_channel_range {
ADC_CONF_100M14B4CHA_CHN_RANGE_OPEN_DRAIN   = 0
ADC_CONF_100M14B4CHA_CHN_RANGE_100mV        = 0x23
ADC_CONF_100M14B4CHA_CHN_RANGE_1V           = 0x11
ADC_CONF_100M14B4CHA_CHN_RANGE_10V          = 0x45
ADC_CONF_100M14B4CHA_CHN_RANGE_100mV_CAL    = 0x42
ADC_CONF_100M14B4CHA_CHN_RANGE_1V_CAL       = 0x40
ADC_CONF_100M14B4CHA_CHN_RANGE_10V_CAL      = 0x44


#List of possible buffer types (options for ADC_CONF_100M14B4CHA_BUF_TYPE)

#enum adc_100m14b4cha_buf_type {
ADC_CONF_100M14B4CHA_BUF_KMALLOC    = 0     #< buffer type 'kmalloc' 
ADC_CONF_100M14B4CHA_BUF_VMALLOC    = 1     #< buffer type 'vmalloc'


#It describes the possible configuration parameters for the
#FMCADC100M14B4CHA card (ADC_CONF_TYPE_CUS)

#enum adc_configuration_100m14b4cha {
ADC_CONF_100M14B4CHA_BUF_TYPE       = 0 # < the ZIO buffer type in use */
ADC_CONF_100M14B4CHA_TRG_SW_EN      = 1 # < software trigger enable/disable */
ADC_CONF_100M14B4CHA_ACQ_MSHOT_MAX  = 2 # < Maximum size for a single shot
                                        # in multi-shot mode (in samples) */
ADC_CONF_100M14B4CHA_BUF_SIZE_KB    = 3 # < it manually sets the buffer size but
                                        # only for VMALLOC buffers */
ADC_CONF_100M14B4CHA_TRG_ALT_EN     = 4 # < alternate trigger enable/disable */
__ADC_CONF_100M14B4CHA_LAST_INDEX   = 5 # < It represents the the last index
                                        # of this enum. It can be useful for
                                        # some sort of automation */
                               
