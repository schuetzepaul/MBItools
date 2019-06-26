#!/usr/bin/python

# This little tool calculates the width of the multiple coulomb scattering angle distribution using the highland formula

import math
import sys
import getopt
import csv


x0alu = 88.97
x0air = 303900.
x0ni = 14.24
x0pb = 5.612
x0w = 3.504
x0si = 93.70
x0fe = 17.57
x0cu = 14.36
x0h2o = 360.8
x0k = 285.7


def highland(energy, thickness, x0):
    return 0.0136/energy*math.sqrt(thickness/x0)*(1.+0.038*math.log(thickness/x0))


message = "\nSpecify the material:\nal: Aluminum \nair: Air \nni: Nickel \npb: Lead \nsi: Silicon \nw: Tungsten \nfe: Iron \ncu: Copper \nh2o: Water \nk: Kapton \no: Other \n"
print message

materialChoice = raw_input("Enter your choice: ")

radLength = 0.
if materialChoice=="al":
    radLength = x0alu
elif materialChoice=="air":
    radLength = x0air
elif materialChoice=="ni":
    radLength = x0ni
elif materialChoice=="pb":
    radLength = x0pb
elif materialChoice=="w":
    radLength = x0w
elif materialChoice=="si":
    radLength = x0si
elif materialChoice=="fe":
    radLength = x0fe
elif materialChoice=="cu":
    radLength = x0cu
elif materialChoice=="h2o":
    radLength = x0h2o
elif materialChoice=="k":
    radLength = x0k
elif materialChoice=="o":
    radLength = input("Enter the radiation length in mm: ")
else:
    print "\nPlease choose a valid option next time, dumbass! I'm outta here!\n"
    exit(1)


thickness = float(raw_input("Enter the material thickness in mm: "))

energy = float(raw_input("Enter the particle energy in GeV: "))

angleWidth = highland(energy,thickness,radLength)*1.E3

lateralDisplacement = angleWidth*thickness/math.sqrt(3)

print "\nThe material budget is " + str(thickness/radLength)
print "\nThe RMS angle is " + str(angleWidth) + " mrad\n"
print "\nThe lateral displacement is " + str(lateralDisplacement) + " um\n"
