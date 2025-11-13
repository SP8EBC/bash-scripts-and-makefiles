#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import socket               
import pycrc
import time
import sys

# Warning!! Relays on the silkscreen are numbered starting from 1
# while registers number in Modbus command starts from 0, so register
# 0 is relay 1 on the PCB etc....

cmd = [0, 0, 0, 0, 0 ,0 , 0, 0, 0, 0, 0, 0]
s = socket.socket()

def set_relay(number):
        cmd[5] = 0x06  #Byte length
        cmd[6] = 0x01  #Device address
        cmd[7] = 0x05  #command  
        cmd[8] = 0
        cmd[9] = number
        cmd[10] = 0xFF
        cmd[11] = 0
        #print(cmd)
        s.send(bytearray(cmd))
        time.sleep(0.2)
        data = s.recv(1024)
        print('[{}]'.format(','.join(hex(x) for x in data)))

def reset_relay(number):
        cmd[5] = 0x06  #Byte length
        cmd[6] = 0x01  #Device address
        cmd[7] = 0x05  #command  
        cmd[8] = 0
        cmd[9] = number
        cmd[10] = 0
        cmd[11] = 0
        #print(cmd)
        s.send(bytearray(cmd))
        time.sleep(0.2)
        data = s.recv(1024)
        print('[{}]'.format(','.join(hex(x) for x in data)))

# Check if exactly 2 arguments were provided (plus script name = 3 total)
if len(sys.argv) != 2:
    print("Error: Exactly 1 arguments required")
    print(f"Usage: {sys.argv[0]} <ip address>")
    sys.exit(1)

host = sys.argv[1]        # set ip
port = 502                 # Set port


print(f"Connecting to {host} : 502")

try:
	s.connect((host, port))     # connect serve
	print("Connected")
	set_relay(1)		# RESET
	time.sleep(2.0)
	set_relay(0)		# BOOT0
	time.sleep(1.0)
	reset_relay(1)		# RESET
	time.sleep(0.5)
	reset_relay(0)		# BOOT0
	s.close()
except OSError as e:
	print(f"Cannot connect to Ethernet relay module!")
	print(e)

