#expected usage:
# /.convert_EVKITConfig_to_I2CBridge.py
# Accepts evkit config file on std in
# Writes file to paste into I2CBridge template to std out

# I2CBridge template is in the format of packet writes. Each packet encompasses sequential I2C writes, aka 0x0020, 0x0021, 0x0022, no skipping or going backwards inside a packet

# split test register writes from normal register writes
# split register writes when the maxWritesPerPacket is met
# split register writes when there is a gap to the next sequential register bigger than maxGap


import fileinput

class G: #Setup
	maxWritesPerPacket = 120 #positive integer
	maxPackets = 127 #positive integer
	maxGap = 1 #positive integer - only tested with 1 at the moment (basic usage)
	revIDAddress = "0x01ff" #hex address "0x~~~~"
	deviceAddress = "0x74"

def parseInput():
	lines = []
	writes = [] #list of tuples of (addr, val)
	testWrites = []
	registersFound = False
	deviceAddressFound = False
	testRegistersFound = False
	
	#first do test registers
	for line in fileinput.input():
		lines.append(line)
		if "[Device Address]" in line:
			deviceAddressFound = True
			continue

		if "[Test Registers]" in line:
			testRegistersFound = True
			continue
			
		if deviceAddressFound:
			G.deviceAddress = line.strip()
			deviceAddressFound = False
		if testRegistersFound:
			(addr, val) = line.strip().split()
			testWrites.append((addr,val))
			
		
	#next do normal registers
	for line in lines:
		if len(line) < 3 and registersFound:
			break
		if "[Control Registers]" in line:
			registersFound = True
			continue
			
		if registersFound:
			try:
				(addr, val) = line.strip().split()
				writes.append((addr,val))
			except:
				continue
			
	# print(writes)
	return testWrites, writes

def buildGrid(testWrites, controlWrites):
	#given test wrutes and control writes, split them up into packets (rows) and sequential writes (columns)
	
	#packet: [addr-hi] [addr-lo] [val1] [val2 @ addr+1] [val3@addr+2] ...
	
	
	grid = []
	currentRow = []
	
	grid.append([G.revIDAddress[0:4], "0x" + G.revIDAddress[4:], "0x54"])
	grid.append([G.revIDAddress[0:4], "0x" + G.revIDAddress[4:], "0x4d"])
			
	for i, (addr, val) in enumerate(testWrites):
		#print(i, addr, val)
		if i == 0:
			currentRow.append(addr[0:4])
			currentRow.append("0x" + addr[4:])
			currentRow.append(val)
		if i >= 1:
			#print(int(addr,16), int(testWrites[i-1][0], 16))
			if (int(addr,16) - int(testWrites[i-1][0], 16)) > G.maxGap:
				#print("Appending currentRow:", currentRow)
				grid.append(currentRow) #dump and restart
				currentRow = []
				currentRow.append(addr[0:4])
				currentRow.append("0x" + addr[4:])
				currentRow.append(val)
			else: #code for if it's sequential
				currentRow.append(val)
	grid.append(currentRow)
			
	currentRow = []
	
	for i, (addr, val) in enumerate(controlWrites):
		#print(i, addr, val)
		if i == 0:
			currentRow.append(addr[0:4])
			currentRow.append("0x" + addr[4:])
			currentRow.append(val)
		if i >= 1:
			#print(int(addr,16), int(controlWrites[i-1][0], 16))
			if (int(addr,16) - int(controlWrites[i-1][0], 16)) > G.maxGap:
				#print("Appending currentRow:", currentRow)
				grid.append(currentRow) #dump and restart
				currentRow = []
				currentRow.append(addr[0:4])
				currentRow.append("0x" + addr[4:])
				currentRow.append(val)
			else: #code for if it's sequential
				currentRow.append(val)
	grid.append(currentRow)
	
	return grid
	#print("Grid:", grid)
	
def main():
	testWrites, controlWrites = parseInput()
	outputGrid = buildGrid(testWrites, controlWrites)
	
	

	for row in outputGrid:
		#print('\t'.join(map(str,row)))
		print('\t'.join([G.deviceAddress, "0", str(len(row))] + list(map(str,row))))
		
	
if __name__ == "__main__":
	main()