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
    #timeout=0.01
    )
counter=0

TCP_IP = '192.168.43.195'
TCP_PORT = 5005
BUFFER_SIZE = 20

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

while 1:
    serialMessage=ser.readline() #ser.read yksi byte, readline \n päätteiselle
    #print (serialMessage)
    s.send(serialMessage)
    #time.sleep(0.5)
    data = s.recv(BUFFER_SIZE)
    print ('received data;', data)
    
s.close()


