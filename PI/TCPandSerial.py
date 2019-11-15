#!/usr/bin/python
import os, sys
import serial
import time
import socket

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    #timeout=5
    )
counter=0

TCP_IP = '192.168.43.195'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = 'Jaakko on NuGet'.encode()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

while 1:
    serialMessage=ser.readline()
    s.send(serialMessage)
    #time.sleep(0.5)
    print (serialMessage.decode('utf-8'))
    data = s.recv(BUFFER_SIZE)
    
s.close()

# print ('received data;', data)
