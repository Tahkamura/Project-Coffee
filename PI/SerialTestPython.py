#!/usr/bin/python
import os, sys
import serial
import time

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    # timeout=5
    )
counter=0

print ("aloitus")

while 1:
    x=ser.readline()
    #x=ser.read(ser.in_waiting)
    print (x.decode('utf-8'))
