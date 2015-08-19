#!/usr/bin/python3
import smbus
import time
import random

# I2C Address of AT24C32 EEPROM
at24c32addr = 0x50

# Set current adress of eeprom
def at24c32_set_addr(addr):
	upperbyte = (addr & 0b1111111100000000) >> 8
	lowerbyte = addr & 0b0000000011111111
	i2c.write_i2c_block_data(at24c32addr, upperbyte, [lowerbyte])
	time.sleep(0.1)

# Valid addr for RAM: 0 - 4096
def at24c32_get_ram(addr):
	at24c32_set_addr(addr)
	return i2c.read_byte(at24c32addr)	

# Valid addr for RAM: 0 - 4096
def at24c32_set_ram(addr, val):
	upperbyte = (addr & 0b1111111100000000) >> 8
	lowerbyte = addr & 0b0000000011111111
	i2c.write_i2c_block_data(at24c32addr, upperbyte, [lowerbyte, val])	
	time.sleep(0.1)

def main():
	if "i2c" not in vars():
		# open I2C Bus 1
		i2c = smbus.SMBus(1)

	# Set Data in EEPROM
	rannum = int(random.random()*100)
	print("Setting EEPROM to 'Hello World X' where X is a random number.")
	print("Random Number is: " + str(rannum))
	at24c32_set_ram(0, ord('H'))
	at24c32_set_ram(1, ord('e'))
	at24c32_set_ram(2, ord('l'))
	at24c32_set_ram(3, ord('l'))
	at24c32_set_ram(4, ord('o'))
	at24c32_set_ram(5, ord(' '))
	at24c32_set_ram(6, ord('W'))
	at24c32_set_ram(7, ord('o'))
	at24c32_set_ram(8, ord('r'))
	at24c32_set_ram(9, ord('l'))
	at24c32_set_ram(10, ord('d'))
	at24c32_set_ram(11, ord(' '))
	at24c32_set_ram(12, rannum)

	# Get Data from EEPROM
	data = []
	print("Reading EEPROM:")
	for i in range(13):
		data.append(at24c32_get_ram(i))

	# Print data as String
	for i in range(12):
		print(str(chr(data[i])), end='')
	print(str(data[12]))
	
# open I2C Bus 1 -> Everytime
i2c = smbus.SMBus(1)
	
# Only run when you are the main program. Not when you're importes as a module:
if __name__ == '__main__':
	main()

