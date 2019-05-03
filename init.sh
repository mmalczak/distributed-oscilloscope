MT_CPU_RESTART="/home/Projects/distributed_oscilloscope/dependencies/mock-turtle/software/tools/mockturtle-cpu-restart"

#WRTD_CONFIG="/home/dlamprid/wrtd/repos/wrtd/software/tools/wrtd-config"

if [ "$EUID" -ne 0 ]
  then echo "Please run as root (or with sudo)"
  exit
fi

for id in 1 2
do

    # take MT out of reset, FPGA is pre-programmed with the firmware
    ${MT_CPU_RESTART} -D "0x0${id}" -i 0

    # Enable WRTD logging
    #${WRTD_CONFIG} -D "MT0${id}" set-log on

    # 251723810 = 0x0f010022 = SW trigger, ALT TIME trigger and full trigger forwarding to WRTD
    echo 251723810 > "/sys/bus/zio/devices/adc-100m14b-000${id}/cset0/trigger/source"

done
