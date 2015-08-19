#!/usr/bin/python3
import smbus
import datetime
import random

# I2C Address of DS1307 RTC
ds1307addr = 0x68

# Functions for getting and setting according to the DS1307 Datasheet
def ds1307_get_seconds():
	retbyte = i2c.read_byte_data(ds1307addr, 0x00)
	lower4bits = retbyte & 0b00001111
	upper4bits = ((retbyte & 0b01110000) >> 4)
	returnstr = str(upper4bits) + str(lower4bits)
	return int(returnstr)
	
def ds1307_get_minutes():
	retbyte = i2c.read_byte_data(ds1307addr, 0x01)
	lower4bits = retbyte & 0b00001111
	upper4bits = ((retbyte & 0b01110000) >> 4)
	returnstr = str(upper4bits) + str(lower4bits)
	return int(returnstr)	

# Returns in 24 hours mode
def ds1307_get_hours():
	retbyte = i2c.read_byte_data(ds1307addr, 0x02)
	lower4bits = retbyte & 0b00001111
	# Check if 24 Hour Clock
	mode12 = ((retbyte & 0b01000000) >> 6)
	if mode12 == 0:
		# 24-hour-mode
		upper4bits = ((retbyte & 0b00110000) >> 4)
		returnstr = str(upper4bits) + str(lower4bits)
		return int(returnstr)	
	else:
		# 12-hour-mode
		upper4bits = ((retbyte & 0b00010000) >> 4)
		returnstr = str(upper4bits) + str(lower4bits)
		pm_am = ((retbyte & 0b00100000) >> 5)
		if pm_am == 1:
			# pm - we return in 24-hour-mode
			return int(returnstr) + 12
		else:
			# am
			return int(returnstr)

def ds1307_get_day():
	retbyte = i2c.read_byte_data(ds1307addr, 0x03)
	lower3bits = retbyte & 0b00000111
	returnstr = str(lower3bits)
	return int(returnstr)		

def ds1307_get_date():
	retbyte = i2c.read_byte_data(ds1307addr, 0x04)
	lower4bits = retbyte & 0b00001111
	upper4bits = ((retbyte & 0b00110000) >> 4)
	returnstr = str(upper4bits) + str(lower4bits)
	return int(returnstr)		

def ds1307_get_month():
	retbyte = i2c.read_byte_data(ds1307addr, 0x05)
	lower4bits = retbyte & 0b00001111
	upper4bits = ((retbyte & 0b00010000) >> 4)
	returnstr = str(upper4bits) + str(lower4bits)
	return int(returnstr)		

def ds1307_get_year():
	retbyte = i2c.read_byte_data(ds1307addr, 0x06)
	lower4bits = retbyte & 0b00001111
	upper4bits = ((retbyte & 0b11110000) >> 4)
	returnstr = str(upper4bits) + str(lower4bits)
	returnval = int(returnstr)	
	if returnval > 60:
		# year 60 - 99 must be 1900
		return returnval + 1900
	else:
		# year 00 - 60 must be 2000
		return returnval + 2000

# Returns: Clock stopped, 12-hour-mode, outputmode, squarewaveenabled, frequency as a five value tuple
def ds1307_get_control():
	retbyte1 = i2c.read_byte_data(ds1307addr, 0x00)
	retbyte2 = i2c.read_byte_data(ds1307addr, 0x02)
	retbyte3 = i2c.read_byte_data(ds1307addr, 0x07)
	clockstopped = ((retbyte1 & 0b10000000) >> 7)
	mode12 = ((retbyte2 & 0b01000000) >> 6)
	out = ((retbyte3 & 0b10000000) >> 7)
	sqwe = ((retbyte3 & 0b00010000) >> 4)
	rs0 = ((retbyte3 & 0b00000001) >> 0)
	rs1 = ((retbyte3 & 0b00000010) >> 1)
	if rs1 == 0 and rs0 == 0:
		freq = 1
	if rs1 == 0 and rs0 == 1:
		freq = 4096000
	if rs1 == 1 and rs0 == 0:
		freq = 8192000
	if rs1 == 1 and rs0 == 1:
		freq = 32768000
	return clockstopped, mode12, out, sqwe, freq
	
# Valid addr for RAM: 0 - 55
def ds1307_get_ram(addr):
	# RAM starts at Address 0x08
	addr = addr + 0x08	
	return i2c.read_byte_data(ds1307addr, addr)	
	
def ds1307_set_seconds(val):
	if len(str(val)) == 1:
		lower4bits = int(str(val))
		upper4bits = 0
	else:
		lower4bits = int(str(val)[1:])
		upper4bits = int(str(val)[:1]) & 0b00000111
	setstr = "0b" + str("{0:04b}".format(upper4bits)) + str("{0:04b}".format(lower4bits))
	i2c.write_byte_data(ds1307addr, 0x00, int(setstr, 2))

def ds1307_set_minutes(val):
	if len(str(val)) == 1:
		lower4bits = int(str(val))
		upper4bits = 0
	else:
		lower4bits = int(str(val)[1:])
		upper4bits = int(str(val)[:1]) & 0b00000111
	setstr = "0b" + str("{0:04b}".format(upper4bits)) + str("{0:04b}".format(lower4bits))
	i2c.write_byte_data(ds1307addr, 0x01, int(setstr, 2))

# Sets in 24 hours mode
def ds1307_set_hours(val):
	if len(str(val)) == 1:
		lower4bits = int(str(val))
		upper4bits = 0
	else:
		lower4bits = int(str(val)[1:])
		upper4bits = int(str(val)[:1]) & 0b00000011
	setstr = "0b00" + str("{0:02b}".format(upper4bits)) + str("{0:04b}".format(lower4bits))
	i2c.write_byte_data(ds1307addr, 0x02, int(setstr, 2))
	
def ds1307_set_day(val):
	lower3bits = int(str(val)[:1]) & 0b00000111
	setstr = "0b0000" + str("{0:04b}".format(lower3bits))
	i2c.write_byte_data(ds1307addr, 0x03, int(setstr, 2))

def ds1307_set_date(val):
	if len(str(val)) == 1:
		lower4bits = int(str(val))
		upper4bits = 0
	else:
		lower4bits = int(str(val)[1:])
		upper4bits = int(str(val)[:1]) & 0b00000011
	setstr = "0b" + str("{0:04b}".format(upper4bits)) + str("{0:04b}".format(lower4bits))
	i2c.write_byte_data(ds1307addr, 0x04, int(setstr, 2))

def ds1307_set_month(val):
	if len(str(val)) == 1:
		lower4bits = int(str(val))
		upper4bits = 0
	else:
		lower4bits = int(str(val)[1:])
		upper4bits = int(str(val)[:1]) & 0b00000001
	setstr = "0b" + str("{0:04b}".format(upper4bits)) + str("{0:04b}".format(lower4bits))
	i2c.write_byte_data(ds1307addr, 0x05, int(setstr, 2))

def ds1307_set_year(val):
	if len(str(val)) == 1:
		lower4bits = int(str(val))
		upper4bits = 0
	elif len(str(val)) == 2:
		lower4bits = int(str(val)[1:])
		upper4bits = int(str(val)[:1]) & 0b00001111		
	else:
		val = str(val)[2:]
		lower4bits = int(str(val)[1:])
		upper4bits = int(str(val)[:1]) & 0b00001111
	setstr = "0b" + str("{0:04b}".format(upper4bits)) + str("{0:04b}".format(lower4bits))
	i2c.write_byte_data(ds1307addr, 0x06, int(setstr, 2))

def ds1307_set_control(clockstopped, mode12, outputmode, squarewaveenabled, frequency):
	if clockstopped == 1:
		setstr = "0b1" + str("{0:07b}".format(i2c.read_byte_data(ds1307addr, 0x00) & 0b01111111))
		i2c.write_byte_data(ds1307addr, 0x00, int(setstr, 2))
	else:
		setstr = "0b0" + str("{0:07b}".format(i2c.read_byte_data(ds1307addr, 0x00) & 0b01111111))
		i2c.write_byte_data(ds1307addr, 0x00, int(setstr, 2))		
	if mode12 == 1:
		setstr = "0b01" + str("{0:06b}".format(i2c.read_byte_data(ds1307addr, 0x02) & 0b00111111))
		i2c.write_byte_data(ds1307addr, 0x02, int(setstr, 2))	
	else:
		setstr = "0b00" + str("{0:06b}".format(i2c.read_byte_data(ds1307addr, 0x02 & 0b00111111)))
		i2c.write_byte_data(ds1307addr, 0x02, int(setstr, 2))	
	if outputmode == 1:
		setstr = "0b1"
	else:
		setstr = "0b0"
	if squarewaveenabled == 1:
		setstr += "001"
	else:
		setstr += "000"
	if frequency == 32768000:
		setstr += "0011"
	elif frequency == 8192000:
		setstr += "0010"
	elif frequency == 4096000:
		setstr += "0001"
	else:
		setstr += "0000"	
	i2c.write_byte_data(ds1307addr, 0x07, int(setstr, 2))

# Valid addr for RAM: 0 - 55
def ds1307_set_ram(addr, val):
	# RAM starts at Address 0x08
	addr = addr + 0x08
	i2c.write_byte_data(ds1307addr, addr, val)	
	
# Only run when you are the main program. Not when you're importes as a module:
if __name__ == '__main__':
	# open I2C Bus 1
	i2c = smbus.SMBus(1)

	# Set RTC Control
	# -> Set Clock to running
	# -> Set 24-hour-mode
	# -> Output (when SquareWave disabled) 0
	# -> Square Wave enabled
	# -> Frequency 1 Hertz
	ds1307_set_control(0, 0, 0, 1, 1)

	# Set RTC Time
	now = datetime.datetime.now()

	ds1307_set_seconds(int(now.second))
	ds1307_set_minutes(int(now.minute))
	ds1307_set_hours(int(now.hour))
	ds1307_set_day(int(now.strftime("%w")))
	ds1307_set_date(int(now.day))
	ds1307_set_month(int(now.month))
	ds1307_set_year(int(now.year))

	# read RTC
	seconds = ds1307_get_seconds()
	minutes = ds1307_get_minutes()
	hours = ds1307_get_hours()
	day = ds1307_get_day()
	date = ds1307_get_date()
	month = ds1307_get_month()
	year = ds1307_get_year()
	clockstopped, mode12hour, output, squarewavean, freq = ds1307_get_control()

	# Print time
	print("Time is: " + str("{0:02}".format(date)) + "." + str("{0:02}".format(month)) + "." + str("{0:04}".format(year)) + " " + str("{0:02}".format(hours)) + ":" + str("{0:02}".format(minutes)) + ":" + str("{0:02}".format(seconds)))
	print("Day of week: " + str(day))
	print("Clock stopped: " + str(clockstopped))
	print("12-hour-mode: " + str(mode12hour))
	print("Output when SquareWave disabled: " + str(output))
	print("Square-Wave Enabled: " + str(squarewavean))
	print("Frequency of Output: " + str(freq) + " Hz")

	# Set Data in RAM
	rannum = int(random.random()*100)
	print("Setting RAM to 'Hello World X' where X is a random number.")
	print("Random Number is: " + str(rannum))
	ds1307_set_ram(0, ord('H'))
	ds1307_set_ram(1, ord('e'))
	ds1307_set_ram(2, ord('l'))
	ds1307_set_ram(3, ord('l'))
	ds1307_set_ram(4, ord('o'))
	ds1307_set_ram(5, ord(' '))
	ds1307_set_ram(6, ord('W'))
	ds1307_set_ram(7, ord('o'))
	ds1307_set_ram(8, ord('r'))
	ds1307_set_ram(9, ord('l'))
	ds1307_set_ram(10, ord('d'))
	ds1307_set_ram(11, ord(' '))
	ds1307_set_ram(12, rannum)

	# Get Data from RAM
	data = []
	print("Reading RAM:")
	for i in range(13):
		data.append(ds1307_get_ram(i))

	# Print data as String
	for i in range(12):
		print(str(chr(data[i])), end='')
	print(str(data[12]))

	# close I2C Bus
	del i2c
else:
	# We're a module, just open the Bus, and leave it open
	i2c = smbus.SMBus(1)	
