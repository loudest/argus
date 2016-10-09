import serial

def parse_serial():
	ser = serial.Serial(
		port='COM3',
		baudrate=9600,
		parity=serial.PARITY_ODD,
		stopbits=serial.STOPBITS_TWO,
		bytesize=serial.SEVENBITS
	)

	if ser.isOpen():
		print ser.read(10)
		print '\n'
	else:
		ser.close()

while(1):
	parse_serial()