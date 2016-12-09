#Spit out VBA commands for writing config file equivalent, 16 bit registers, using I2C Bridge from Bill

import sys

registersReached = False

for line in sys.stdin:
	if "[Control Registers]" in line:
		registersReached = True
		continue
	if registersReached != True:
		continue
	
	#0x0010	0x20
	hi = line[2:4]
	lo = line[4:6]
	val = line.split()[1][2:4]
	
	print( "Call I2C_Controls_.I2C_bridge_16Bit_Write_Control(DEV, &H" + hi + ", &H" + lo + ", &H" + val + ")" )