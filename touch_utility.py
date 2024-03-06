#!/usr/bin/python3

import RPi.GPIO as GPIO
import time

# Pin Definitions
cs_pin = 17
clk_pin = 21  # SCLK_1
mosi_pin = 20  # MOSI_1
miso_pin = 19  # MISO_1
irq_pin = 26
button_pin = 22  # Button for saving calibration

# Setup GPIO
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
GPIO.setup(cs_pin, GPIO.OUT)
GPIO.setup(clk_pin, GPIO.OUT)
GPIO.setup(mosi_pin, GPIO.OUT)
GPIO.setup(miso_pin, GPIO.IN)
GPIO.setup(irq_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# SPI Parameters
clock_speed_hz = 1000000  # 1 MHz
CMD_READ_X = 0x90  # Command to read X coordinate
CMD_READ_Y = 0xD0  # Command to read Y coordinate
READ_TIMES = 5
LOST_VAL = 1
ERR_RANGE = 50

def spi_transfer(command):
    byte_in = 0
    GPIO.output(cs_pin, GPIO.LOW)  # Begin SPI conversation
    spi_write_byte(command)  # Send command
    byte_in = spi_read_byte()  # Read 12-bit data
    GPIO.output(cs_pin, GPIO.HIGH)  # End SPI conversation
    return byte_in >> 3  # Return 12-bit ADC result

def spi_write_byte(byte_out):
    for bit in range(8):  # Loop through each bit
        GPIO.output(mosi_pin, (byte_out >> (7 - bit)) & 0x1)
        GPIO.output(clk_pin, GPIO.HIGH)
        time.sleep(1/(2*clock_speed_hz))  # Half period delay
        GPIO.output(clk_pin, GPIO.LOW)
        time.sleep(1/(2*clock_speed_hz))  # Half period delay

def spi_read_byte():
    byte_in = 0
    for _ in range(12):  # Loop through each bit of the 12-bit ADC
        byte_in <<= 1
        GPIO.output(clk_pin, GPIO.HIGH)
        time.sleep(1/(2*clock_speed_hz))
        if GPIO.input(miso_pin):
            byte_in |= 0x1
        GPIO.output(clk_pin, GPIO.LOW)
        time.sleep(1/(2*clock_speed_hz))
    return byte_in

def read_touch_coordinate_smoothed(command):
    readings = [spi_transfer(command) for _ in range(READ_TIMES)]
    readings.sort()
    # Remove the highest and lowest readings
    readings = readings[LOST_VAL:READ_TIMES-LOST_VAL]
    return sum(readings) // len(readings)

def read_touch_coordinates():
    x = read_touch_coordinate_smoothed(CMD_READ_X)
    y = read_touch_coordinate_smoothed(CMD_READ_Y)
    return x, y

def cleanup():
    GPIO.cleanup()
