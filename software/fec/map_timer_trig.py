from mmap import*


f1 = open('/sys/bus/pci/devices/0000:01:00.0/resource0', "r+")
f2 = open('/sys/bus/pci/devices/0000:02:00.0/resource0', "r+")
f1.flush()
f2.flush()
a1 = mmap(f1.fileno(), 0, flags=MAP_SHARED, prot=PROT_WRITE|PROT_READ)
a2 = mmap(f2.fileno(), 0, flags=MAP_SHARED, prot=PROT_WRITE|PROT_READ)



def write_word(offset, value, dev):
   if(dev==1):
      a=a1
   else:
      a=a2
   ar = [0, 0, 0, 0]
   word = bytearray()
   for count in range(3, -1, -1):
      wr = value/(256**count)
      value = value-int(wr)*(256**count)
      ar[count] = int(wr)
   for count in range(0, 4):
      word.append(ar[count])
   a[offset:offset+4] = word

def read_word(offset, dev):
   if(dev==1):
      a=a1
   else:
      a=a2

   value = 0
   for count in range(3, -1, -1):
      value = value*256 + a[offset+count]
   return value


def timetag_trig_enable():
   write_word(trig_en, 0x0010, 1)
   write_word(trig_en, 0x0010, 2)
#   print(read_word(time_trig_sec_up))

timetag_sec_up = 0x3900
timetag_sec_lo = 0x3904
timetag_tic = 0x3908
time_trig_sec_up = 0x390c
time_trig_sec_lo = 0x3910
time_trig_tic = 0x3914

trig_en = 0x300c


#write_word(time_trig_tic, 512+8+1)
#print(format(read_word(time_trig_tic), "08X"))
#timetag_trig_enable()
