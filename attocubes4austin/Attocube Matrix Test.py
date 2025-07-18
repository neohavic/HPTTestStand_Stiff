# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 08:20:32 2023

@author: aeverman
"""

import numpy as np
from IDS import Device

J = np.array([[-0.0931,    0.4916,   -0.8658,   -0.1226,   -0.0119,    0.0064],
             [-0.1192,    0.4903,   -0.8634,   -0.1223,    0.0193,    0.0278],
             [0.1827,    0.6106,   -0.7706,    0.0953,   -0.1074,   -0.0625],
             [0.1964,    0.5962,   -0.7784,    0.0719,   -0.1225,   -0.0757],
             [-0.1134,   -0.0576,   -0.9919,    0.0931,    0.1340,   -0.0184],
             [-0.1281,   -0.0835,   -0.9882,    0.0619,    0.1513,   -0.0208]])

optical_paths = np.array([0, 0, 0, 0, 0, 0])

matrix_result = np.array([[0], [0], [0], [0], [0], [0]])

# Try establish connection to AttoCube 206 and get info from device; If unable, print error to console and exit
try:
    print("Connecting to AttoCubube 206...")
    dev206 = Device('192.168.88.206')
    dev206.connect()
    
    print(dev206.getFeatureName(1)) #OK
    print(dev206.getSerialNumber()) #OK
    print(dev206.getFpgaVersion()) #OK
    print(dev206.getMacAddress()) #OK
    print(dev206.getDeviceType()) #OK
    print(dev206.getDeviceName()) #OK
    print("#206 CONNECTED \n")


    print("Connecting to AttoCubube 207...")
    dev207 = Device('192.168.88.207')
    dev207.connect()
    
    print(dev207.getFeatureName(1)) #OK
    print(dev207.getSerialNumber()) #OK
    print(dev207.getFpgaVersion()) #OK
    print(dev207.getMacAddress()) #OK
    print(dev207.getDeviceType()) #OK
    print(dev207.getDeviceName()) #OK
    print("#207 CONNECTED \n")
    
except:
    print("Could not connect to AttoCubes.\n Please check connection and try again.\n Now exiting.")
    exit()


while True:
    Dev206Ch0 = dev206.getAxisDisplacement(0)
    Dev206Ch1 = dev206.getAxisDisplacement(1)
    Dev206Ch2 = dev206.getAxisDisplacement(2)
    Dev207Ch0 = dev207.getAxisDisplacement(0)
    Dev207Ch1 = dev207.getAxisDisplacement(1)
    Dev207Ch2 = dev207.getAxisDisplacement(2)

    optical_paths = ([Dev206Ch0, Dev206Ch1, Dev206Ch2, Dev207Ch0, Dev207Ch1, Dev207Ch2])

    matrix_result = np.dot(optical_paths, J)
    #print(matrix_result[2])
    print(matrix_result)