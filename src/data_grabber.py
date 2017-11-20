#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 09:10:33 2017

@author: Philipe & Francois
"""
# Python headers:
from datetime import datetime
import serial, time
import sys
import os

# ROS headers:
import rospy
from std_msgs.msg import String

# Global variables (for tests):
GPS_ACTIVATED = True 
SINGLE_BEAM_ACTIVATED = False

# Parameters:
GPS_LOCATION = '/dev/ttyUSB0'
SINGLE_BEAM_LOCATION = '/dev/ttyUSB0'


def receive(sensor):
    """
    Communication with the sensor, using the serial port
    """
    # while True:
    try:
        time.sleep(0.01)
        state = sensor.readline()
        state = state[0:-2]  # to get rid of a "hidden" '\n'
        return state
    except:
        pass
    time.sleep(0.1)


def writeGPS(f):
    """
    Reads GPS data and writes it inside the file
    """
    # Adding time and date:
    dataLine = datetime.now().strftime("%Y%m%d%H%M%S%f")
    dataLine += (",")

    # Reading GPS:
    dataGPS = receive(GPS)

    # Writing:
    dataLine += dataGPS
    if len(dataGPS.split(",")) == 15:
        dataLine = str(dataLine)
        dataLine = dataLine.replace("[", "")
        dataLine = dataLine.replace("]", "")
        line = dataLine + '\n'

        f.write(line)
        print line
    else:
        pass


def writeSingleBeam(f):
    """
    Reads Single Beam data and writes it inside the file
    """
    # Adding time and date:
    dataLine = datetime.now().strftime("%Y%m%d%H%M%S%f")
    dataLine += (",")

    # Reading Single Beam:
    dataSingleBeam = receive(singleBeam)

    # Processing data:
    dataSingleBeam = dataSingleBeam.replace("+", "")

    # Writing:
    dataLine += dataSingleBeam
    if dataLine[-1] == ",":
        pass
    else:
        line = dataLine + '\n'
        f.write(line)
        print line


if __name__ == "__main__":
    # Definition of the node:
    rospy.init_node('data_grabber', anonymous=True)

    # Formatting the output file:
    t = time.localtime()
    namefile = "../GuerledanLogs/helios"  # We need to be sure that the folder logs exists! If not, nothing will be written!
    namefile += datetime.now().strftime("%Y%m%d%H%M%S")  # Adding time and date to the file's name
    namefile += ".txt"  # Adding the extension

    # Tunning I/O:
    if GPS_ACTIVATED:
        GPS = serial.Serial(GPS_LOCATION, 9600, timeout=0.1)
    if SINGLE_BEAM_ACTIVATED:
        singleBeam = serial.Serial(SINGLE_BEAM_LOCATION, 4800, timeout=0.1)  # for debugging

    # For safety reasons (if violently closed):
    f = open(namefile, 'w')
    f.close()

    # Openning the file:
    f = open(namefile, 'a')

    # while True:
    while not rospy.is_shutdown():
        try:
            if GPS_ACTIVATED:
                line = writeGPS(f)
            if SINGLE_BEAM_ACTIVATED:
                line = writeSingleBeam(f)
        except KeyboardInterrupt:
            f.close()
            exit()
