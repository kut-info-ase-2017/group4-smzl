# coding:utf-8
from __future__ import print_function
from ctypes import *
import re

import RPi.GPIO as GPIO
import time
import socket

# set BCM_GPIO 17(GPIO 0) as PIR pin
PIRPin = 17

# libpafe.hの77行目で定義
FELICA_POLLING_ANY = 0xffff
# 学籍番号,名前,idmのリスト
MEMBERS_FILE_NAME = '/home/pi/pasori/members_list.txt'

# initiralze PaSoRi
libpafe = cdll.LoadLibrary("/usr/local/lib/libpafe.so")
libpafe.pasori_open.restype = c_void_p
pasori = libpafe.pasori_open()

# preload members
file = open(MEMBERS_FILE_NAME)
global lines_data
lines_data = file.readlines()
file.close()


#print message at the begining ---custom function
def print_message():
    print ('Program is running...')
    print ('Please press Ctrl+C to end the program...')

#setup function for some setup---custom function
def setup():
    GPIO.setwarnings(False)
    #set the gpio modes to BCM numbering
    GPIO.setmode(GPIO.BCM)
    #set BuzzerPin's mode to output,and initial level to HIGH(3.3V)
    #GPIO.setup(BuzzerPin,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(PIRPin,GPIO.IN)

#define a destroy function for clean up everything after the script finished
def destroy():
    #turn off buzzer
    ##GPIO.output(BuzzerPin,GPIO.HIGH)
    #release resource
    GPIO.cleanup()

def idm2name(idm):
    line_count = 0
    for line in lines_data:
        line_count += 1
        if re.search(idm, line):
            name_value = line.split(',')[1]  # 0:学籍番号
            print('Felica HIT: '+ name_value)
            break
        if line_count == len(lines_data):
            print("Not match, not registered.")
            name_value = 0
    return name_value


def getIDm():
    libpafe.pasori_init(pasori)
    libpafe.felica_polling.restype = c_void_p
    felica = libpafe.felica_polling(pasori, FELICA_POLLING_ANY, 0, 0)

    idm = c_ulonglong() #16桁
    libpafe.felica_get_idm.restype = c_void_p
    libpafe.felica_get_idm(felica, byref(idm))

    idm_value = "{0:016X}".format(idm.value)

    libpafe.free(felica)
    libpafe.pasori_close(pasori)

    return idm_value


if __name__ == '__main__':
    print_message()

    setup()
    try:
        while True:
            try:
                host = '172.21.32.85'
                port = 8081

                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((host, port))

                while True:
                    #print(PIRPin)
                    if(GPIO.input(PIRPin)!=0):
                        print('HUMAN EXIST')
                        client.send('detect')
                        client.send(idm2name(getIDm()))
                        time.sleep(1)
                    else:
                        print ('====================')
                        print ('=     no human     =')
                        print ('====================')
                        print ('\n')
                        time.sleep(1)

            except Exception as e:
                print(e)
                
    except KeyboardInterrupt:
        destroy()
        client.close()

        
