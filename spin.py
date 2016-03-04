#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# spin                                                                         #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# The program spin provides an interface for control of the usage modes of     #
# laptop-tablet and similar computer interface devices.                        #
#                                                                              #
# copyright (C) 2013 William Breaden Madden                                    #
#                                                                              #
# This software is released under the terms of the GNU General Public License  #
# version 3 (GPLv3).                                                           #
#                                                                              #
# This program is free software: you can redistribute it and/or modify it      #
# under the terms of the GNU General Public License as published by the Free   #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# This program is distributed in the hope that it will be useful, but WITHOUT  #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or        #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for     #
# more details.                                                                #
#                                                                              #
# For a copy of the GNU General Public License, see                            #
# <http://www.gnu.org/licenses/>.                                              #
#                                                                              #
################################################################################

Usage:
    spin.py [options]

Options:
    -h,--help        display help message
    --version        display version and exit
    --nogui          non-GUI mode
    --debugpassive   display commands without executing
"""

name    = "spin"
version = "2015-04-30T0256Z"

import os
import sys
import glob
import subprocess
import multiprocessing
import socket
import time
import logging
import docopt
from   PyQt4 import QtGui

class interface(QtGui.QWidget):

    def __init__(self, options):
        self.options = options
        super(interface, self).__init__()
        log.info("initiate {name}".format(name = name))
        # Audit the inputs available.
        self.deviceNames = get_inputs()
        if options["--debugpassive"] is True:
            log.info("device names: {deviceNames}".format(
                deviceNames = self.deviceNames
            ))
        # engage stylus proximity control
        self.stylus_proximity_control_switch("on")
        # engage acceleration control
        #self.acceleration_control_switch(status = "on")
        # engage display position control
        self.displayPositionStatus = "laptop"
        #self.display_position_control_switch(status = "on")
        self.orientation = "normal"
        if not options["--nogui"]:
            # create buttons
            buttonsList = []
            for modeName in ("tablet", "laptop", "left", "right", "inverted", "normal"):
                buttonMode = QtGui.QPushButton(modeName, self)
                def modeFunction(m):
                    return lambda: self.engage_mode(m)
                buttonMode.clicked.connect(modeFunction(modeName))
                buttonsList.append(buttonMode)
            for device in ("touchscreen", "touchpad", "keyboard", "nipple"):
                if device in self.deviceNames:
                    for status in ("on", "off"):
                        button = QtGui.QPushButton(device + " " + status, self)
                        def switchFunction(d, s):
                            return lambda: self.switch(d, s)
                        button.clicked.connect(switchFunction(device, status))
                        buttonsList.append(button)
            # button: stylus proximity monitoring
            if "stylus" in self.deviceNames:
                for status in ("on", "off"):
                    button = QtGui.QPushButton("stylus monitor " + status, self)
                    def controlFunction(s):
                        return lambda: self.stylus_proximity_control_switch(s)
                    button.clicked.connect(controlFunction(status))
                    buttonsList.append(button)
            # button: acceleration monitoring on
            #buttonAccelerationControlOn = QtGui.QPushButton(
            #    "acceleration monitoring on",
            #    self
            #)
            #buttonAccelerationControlOn.clicked.connect(
            #    lambda: self.acceleration_control_switch(status = "on")
            #)
            #buttonsList.append(buttonAccelerationControlOn)
            # button: acceleration monitoring off
            #buttonAccelerationControlOff = QtGui.QPushButton(
            #    "acceleration monitoring off",
            #    self
            #)
            #buttonAccelerationControlOff.clicked.connect(
            #    lambda: self.acceleration_control_switch(status = "off")
            #)
            #buttonsList.append(buttonAccelerationControlOff)
            # button: display position monitoring on
            #buttondisplay_position_controlOn = QtGui.QPushButton(
            #    "display position monitoring on",
            #    self
            #)
            #buttondisplay_position_controlOn.clicked.connect(
            #    lambda: self.display_position_control_switch(status = "on")
            #)
            #buttonsList.append(buttondisplay_position_controlOn)
            # button: display position monitoring off
            #buttondisplay_position_controlOff = QtGui.QPushButton(
            #    "display position monitoring off",
            #    self
            #)
            #buttondisplay_position_controlOff.clicked.connect(
            #    lambda: self.display_position_control_switch(status = "off")
            #)
            #buttonsList.append(buttondisplay_position_controlOff)
            # set button dimensions
            buttonsWidth  = 140
            buttonsHeight = 50
            for button in buttonsList:
                button.setFixedSize(buttonsWidth, buttonsHeight)
                button.setStyleSheet(
                    """
                    color: #000000;
                    background-color: #ffffff;
                    border: 1px solid #000000;
                    font-size: 12pt;
                    text-align: left;
                    padding-left: 5px;
                    padding-right: 5px;
                    """
                )
            # set layout
            vbox = QtGui.QVBoxLayout()
            vbox.addStretch(1)
            for button in buttonsList:
                vbox.addWidget(button)
                vbox.addStretch(1)
            self.setLayout(vbox)
            # window
            self.setWindowTitle("spin")
            # set window position
            self.move(0, 0)
            self.show()
        elif options["--nogui"]:
            log.info("non-GUI mode")

    def close_event(self, event):
        log.info("terminate {name}".format(name = name))
        self.stylus_proximity_control_switch(status = "off")
        self.display_position_control_switch(status = "off")
        self.deleteLater() 

    def set_orientation(self, orientation):
        self.orientation = orientation
        for device in ("display", "stylus", "touchscreen", "touchpad"):
            if device == "display" or device in self.deviceNames:
                coordinateTransformationMatrix = {
                    "left":     "0 -1 1 1 0 0 0 0 1",
                    "right":    "0 1 0 -1 0 1 0 0 1",
                    "inverted": "-1 0 1 0 -1 1 0 0 1",
                    "normal":   "1 0 0 0 1 0 0 0 1"
                }
                if orientation in coordinateTransformationMatrix:
                    log.info("change %s to %s" % (device, orientation))
                    if device == "display":
                        engage_command("xrandr -o %s" % orientation)
                    else:
                        engage_command('xinput set-prop "%s" "Coordinate Transformation Matrix" %s' % (self.deviceNames[device], coordinateTransformationMatrix[orientation]))
                else:
                    log.error('unknown %s orientation "%s" requested' % (device, orientation))
                    sys.exit()
            else:
                log.debug("%s orientation unchanged" % device)

    def switch(self, device, status):
        if device in self.deviceNames:
            xinputStatus = {"on": "enable", "off": "disable"}
            if status in xinputStatus:
                log.info("change %s to %s" % (device, status))
                engage_command('xinput %s "%s"' % (xinputStatus[status], self.deviceNames[device]))
            else:
                log.error('unknown %s status "%s" requested' % (device, status))
                sys.exit()
        else:
            log.debug("%s status unchanged" % device)

    def stylus_proximity_control(self):
        previousStylusProximityStatus = None
        while True:
            stylusProximityCommand = 'xinput query-state "%s" | grep Proximity | cut -d " " -f3 | cut -d "=" -f2' % self.deviceNames["stylus"]
            stylusProximityStatus = subprocess.check_output(stylusProximityCommand, shell=True).lower().rstrip()
            if stylusProximityStatus == "out":
                if previousStylusProximityStatus != "out":
                    log.info("stylus inactive")
                    self.switch("touchscreen", "on")
            elif stylusProximityStatus == "in":
                if previousStylusProximityStatus != "in":
                    log.info("stylus active")
                    self.switch("touchscreen", "off")
            else:
                log.info("could not find stylus, resetting oreintation")
                self.set_orientation(self.orientation)
            previousStylusProximityStatus = stylusProximityStatus
            time.sleep(0.15)

    def stylus_proximity_control_switch(self, status):
        if "stylus" in self.deviceNames:
            if status == "on":
                log.info("change stylus proximity control to on")
                self.processStylusProximityControl = multiprocessing.Process(
                    target = self.stylus_proximity_control
                )
                self.processStylusProximityControl.start()
            elif status == "off":
                log.info("change stylus proximity control to off")
                self.processStylusProximityControl.terminate()
            else:
                log.error(
                    "unknown stylus proximity control status \"{status}\" "
                    "requested".format(
                        status = status
                    )
                )
                sys.exit()
        else:
            log.debug("stylus proximity status unchanged")

    def acceleration_control(self):
        while True:
            # Get the mean of recent acceleration vectors.
            numberOfMeasurements = 3
            measurements = []
            for measurement in range(0, numberOfMeasurements):
                measurements.append(AccelerationVector())
            stableAcceleration = mean_list(lists = measurements)
            log.info("stable acceleration vector: {vector}".format(
                vector = stableAcceleration
            ))
            tableOrientations = {
                (True,  True):  "left",
                (True,  False): "right",
                (False, True):  "inverted",
                (False, False): "normal"
            }
            orientation = tableOrientations[(
                abs(stableAcceleration[0]) > abs(stableAcceleration[1]),
                stableAcceleration[0] > 0
            )]
            self.engage_mode(mode = orientation)
            time.sleep(0.15)

    def acceleration_control_switch(
        self,
        status = None
        ):
        if status == "on":
            log.info("change acceleration control to on")
            self.processAccelerationControl = multiprocessing.Process(
                target = self.acceleration_control
            )
            self.processAccelerationControl.start()
        elif status == "off":
            log.info("change acceleration control to off")
            self.processAccelerationControl.terminate()
        else:
            log.error(
                "unknown acceleration control status \"{status}\" "
                "requested".format(
                    status = status
                )
            )
            sys.exit()

    def display_position_control(self):
        socketACPI = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        socketACPI.connect("/var/run/acpid.socket")
        log.info("display position is {displayPositionStatus}".format(
            displayPositionStatus = self.displayPositionStatus
            )
        )
        while True:
            eventACPI = socketACPI.recv(4096)
            # Ubuntu 13.10 compatibility:
            #eventACPIDisplayPositionChange = \
            #    "ibm/hotkey HKEY 00000080 000060c0\n"
            # Ubuntu 14.04 compatibility:
#            print eventACPI
            eventACPIDisplayPositionChange = \
                "ibm/hotkey LEN0068:00 00000080 000060c0\n"
            if eventACPI == eventACPIDisplayPositionChange:
                log.info("display position change")
                if self.displayPositionStatus == "laptop":
                    self.engage_mode(mode = "tablet")
                    self.displayPositionStatus = "tablet"
                    log.info(
                        "display position is {displayPositionStatus}".format(
                            displayPositionStatus = self.displayPositionStatus
                        )
                    )
                elif self.displayPositionStatus == "tablet":
                    self.engage_mode(mode = "laptop")
                    self.displayPositionStatus = "laptop"
                    log.info(
                        "display position is {displayPositionStatus}".format(
                            displayPositionStatus = self.displayPositionStatus
                        )
                    )
            time.sleep(0.15)

    def display_position_control_switch(
        self,
        status = None
        ):
        if status == "on":
            log.info("change display position control to on")
            self.processdisplay_position_control = multiprocessing.Process(
                target = self.display_position_control
            )
            self.processdisplay_position_control.start()
        elif status == "off":
            log.info("change display position control to off")
            self.processdisplay_position_control.terminate()
        else:
            log.error(
                "unknown display position control status \"{orientation}\" "
                "requested".format(
                    status = status
                )
            )
            sys.exit()

    def engage_mode(self, mode):
        log.info("engage mode %s" % mode)
        if mode == "tablet":
            self.set_orientation("left")
            for device in ("touchpad", "nipple", "keyboard",
                           "brightness keys", "wireless keys"):
                self.switch(device, "off")
        elif mode == "laptop":
            self.set_orientation("normal")
            for device in ("touchpad", "nipple", "keyboard",
                           "brightness keys", "wireless keys"):
                self.switch(device, "on")
        elif mode in ("left", "right", "inverted", "normal"):
            self.set_orientation(mode)
        else:
            log.error('unknown mode "%s" requested' % mode)
            sys.exit()

def get_inputs():
    log.info("audit inputs")
    inputDevices = subprocess.check_output(["xinput", "--list"])
    devicesAndKeyphrases = {
        "touchscreen": ["SYNAPTICS Synaptics Touch Digitizer V04",
                        "ELAN Touchscreen"],
        "touchpad":    ["PS/2 Synaptics TouchPad",
                        "SynPS/2 Synaptics TouchPad"],
        "keyboard":    ["AT Translated Set 2 keyboard"],
        "brightness keys": ["Video Bus"],
        "wireless keys":   ["HP Wireless hotkeys"],
        "nipple":      ["TPPS/2 IBM TrackPoint"],
        "stylus":      ["Wacom ISDv4 EC Pen stylus",
                        "ELAN Touchscreen Pen"]
    }
    deviceNames = {}
    for device, keyphrases in devicesAndKeyphrases.items():
        for keyphrase in keyphrases:
            if keyphrase in inputDevices:
                deviceNames[device] = keyphrase
    for device, keyphrases in devicesAndKeyphrases.items():
        if device in deviceNames:
            log.info("input {device} detected as \"{deviceName}\"".format(
                device     = device,
                deviceName = deviceNames[device]
            ))
        else:
            log.info("input %s not detected" % device)
    return deviceNames

def engage_command(command):
    if options["--debugpassive"] is True:
        log.info("command: %s" % command)
    else:
        subprocess.call(command, shell=True)

def mean_list(lists):
    return([sum(element)/len(element) for element in zip(*lists)])

class AccelerationVector(list):

    def __init__(self):
        list.__init__(self)  
        # Access the IIO interface to the accelerometer.
        devicesDirectories = glob.glob("/sys/bus/iio/devices/iio:device*")
        for directory in devicesDirectories:
            if "accel_3d" in open(os.path.join(directory, "name")).read():
                self.accelerometerDirectory = directory
        self.accelerometerScaleFileFullPath =\
            self.accelerometerDirectory + "/" + "in_accel_scale"
        self.accelerometerAxisxFileFullPath =\
            self.accelerometerDirectory + "/" + "in_accel_x_raw"
        self.accelerometerAxisyFileFullPath =\
            self.accelerometerDirectory + "/" + "in_accel_y_raw"
        self.accelerometerAxiszFileFullPath =\
            self.accelerometerDirectory + "/" + "in_accel_z_raw"
        self.accelerometerScaleFile = open(self.accelerometerScaleFileFullPath)
        self.accelerometerAxisxFile = open(self.accelerometerAxisxFileFullPath)
        self.accelerometerAxisyFile = open(self.accelerometerAxisyFileFullPath)
        self.accelerometerAxiszFile = open(self.accelerometerAxiszFileFullPath)
        # Access the scale.
        self.scale = float(self.accelerometerScaleFile.read())
        # Initialise the vector.
        self.extend([0, 0, 0])
        self.update()

    def update(self):
        # Access the acceleration.
        self.accelerometerAxisxFile.seek(0)
        self.accelerometerAxisyFile.seek(0)
        self.accelerometerAxiszFile.seek(0)
        acceleration_x = float(self.accelerometerAxisxFile.read()) * self.scale
        acceleration_y = float(self.accelerometerAxisyFile.read()) * self.scale
        acceleration_z = float(self.accelerometerAxiszFile.read()) * self.scale
        # Update the vector.
        self[0] = acceleration_x
        self[1] = acceleration_y
        self[2] = acceleration_z

    def __repr__(self):
        self.update()
        return(list.__repr__(self))

def main(options):
    # logging
    global log
    log        = logging.getLogger()
    logHandler = logging.StreamHandler()
    log.addHandler(logHandler)
    logHandler.setFormatter(logging.Formatter("%(message)s"))
    log.level  = logging.INFO

    application = QtGui.QApplication(sys.argv)
    interface1  = interface(options)
    sys.exit(application.exec_())

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
