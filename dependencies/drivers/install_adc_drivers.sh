PYTHON=python3.6
DRIVERSDIR=/home/Projects/distributed_oscilloscope/dependencies/drivers
PLATFORM_DEVICE_LOADER=$DRIVERSDIR/coht-tools/drivers/platform-device-loader/platform-device-loader
HTVIC_IRQ_HW_TO_LNX=$DRIVERSDIR/htvic_irq_hw_to_lnx
SPEC_GPIO_HW_TO_LNX=$DRIVERSDIR/spec_irq_gpio_to_lnx


adc_bitstream=$DRIVERSDIR/bitstream/spec_adc_top.bin
spec_irq_gpio=8

#VIC HW IRQ
adc_irq_ready=0
adc_irq_dma=1
trtl_irq=2
#memory offsets
SPEC_MEM_START=0x1000
SPEC_MEM_END=0x10FF
SPEC_DMA_START=0x2000
SPEC_DMA_END=0x220F
VIC_MEM_START=0x1200
VIC_MEM_END=0x12FF
ADC_MEM_START=0x4000
ADC_MEM_END=0x5FFF
TRTL_MEM_START=0x20000
TRTL_MEM_END=0x3FFFF

sudo mount -t debugfs none /sys/kernel/debug/
# laziness, needed to avoid to compile two different ADC drivers
#sudo insmod ${DRIVERSDIR}/vmebridge/vmebus.ko
sudo insmod ${DRIVERSDIR}/coht-vic/drivers/htvic.ko
sudo insmod ${DRIVERSDIR}/fmc-adc-100m14b4cha-sw/zio/zio.ko
sudo insmod ${DRIVERSDIR}/fmc-adc-100m14b4cha-sw/zio/buffers/zio-buf-vmalloc.ko   #????
sudo insmod ${DRIVERSDIR}/fmc-adc-100m14b4cha-sw/kernel/fmc-adc-100m14b.ko
sudo insmod ${DRIVERSDIR}/fmc/drivers/fmc/fmc.ko
sudo insmod ${DRIVERSDIR}/fpga-manager/drivers/fpga/fpga-mgr.ko
sudo insmod ${DRIVERSDIR}/fmc-spec/kernel/spec.ko
sudo insmod ${DRIVERSDIR}/mockturtle/software/kernel/mockturtle.ko



for id in 1 2
do
	 
	pciid="0000:01:00.0"
	if [ $id == 2 ]
		then
		pciid="0000:02:00.0"
	fi	


	#FPGA device id
	vic_id=$id
	adc_id=$id
	trtl_id=$id



	fpga=$(basename $(ls -d /sys/bus/pci/devices/$pciid/fpga_manager/fpga*))

	echo unlock > /sys/class/fpga_manager/$fpga/config_lock
	sudo dd if=$adc_bitstream of=/dev/$fpga obs=10M

	BASE_ADDR=$(awk 'FNR == 1 {print $1}' /sys/bus/pci/devices/$pciid/resource)
	MAIN_IRQ=$($PYTHON $SPEC_GPIO_HW_TO_LNX --pci $pciid --gpio $spec_irq_gpio)
	HTVIC_MEM=$(printf "0x%x,0x%x" $(($BASE_ADDR + $VIC_MEM_START)) $(($BASE_ADDR + $VIC_MEM_END)))


	$PYTHON $PLATFORM_DEVICE_LOADER -c load \
		--name htvic-spec --id $vic_id \
		--mem $HTVIC_MEM,0x0 \
		--irq $MAIN_IRQ,0x1

	ADC_IRQ_READY=$($PYTHON $HTVIC_IRQ_HW_TO_LNX --bus pci --id $vic_id --vect $adc_irq_ready)
	ADC_IRQ_DMA=$($PYTHON $HTVIC_IRQ_HW_TO_LNX --bus pci --id $vic_id --vect $adc_irq_dma)
	ADC_DMA_MEM=$(printf "0x%x,0x%x" $(($BASE_ADDR + $SPEC_DMA_START)) $(($BASE_ADDR + $SPEC_DMA_END)))
	ADC_CARR_MEM=$(printf "0x%x,0x%x" $(($BASE_ADDR + $SPEC_MEM_START)) $(($BASE_ADDR + $SPEC_MEM_END)))
	ADC_MEM=$(printf "0x%x,0x%x" $(($BASE_ADDR + $ADC_MEM_START)) $(($BASE_ADDR + $ADC_MEM_END)))

	$PYTHON $PLATFORM_DEVICE_LOADER -c load --name adc-100m-spec \
		    --id $adc_id \
		    --irq $ADC_IRQ_READY,0x4 \
		    --irq $ADC_IRQ_DMA,0x4 \
		    --mem $ADC_MEM,0x0 \
		    --mem $ADC_CARR_MEM,0x0 \
		    --mem $ADC_DMA_MEM,0x0 \
		    --busn 1,0x0

	BASE_IRQ=$($PYTHON $HTVIC_IRQ_HW_TO_LNX --bus pci --id $vic_id --vect 2)
	$PYTHON $PLATFORM_DEVICE_LOADER -c load --name mock-turtle \
		--id $trtl_id \
		--mem $(printf "0x%x,0x%x" $(($BASE_ADDR + $TRTL_MEM_START)) $(($BASE_ADDR + $TRTL_MEM_END))),0x0 \
		--irq $(($BASE_IRQ + 0)),0x4 \
		--irq $(($BASE_IRQ + 1)),0x4 \
		--irq $(($BASE_IRQ + 2)),0x4 \
		--irq $(($BASE_IRQ + 3)),0x4

	# some debug stuff
	sudo sh -c 'awk '"'"'$2 == "[fmc_adc_100m14b]" {print $1}'"'"' /sys/kernel/debug/tracing/available_filter_functions > /sys/kernel/debug/tracing/set_ftrace_filter'
	sudo sh -c 'awk '"'"'$2 == "[mockturtle]" {print $1}'"'"' /sys/kernel/debug/tracing/available_filter_functions >> /sys/kernel/debug/tracing/set_ftrace_filter'
	sudo sh -c 'echo function > /sys/kernel/debug/tracing/current_tracer'
	sudo sh -c 'echo 1 > /sys/kernel/debug/tracing/tracing_on'

done
