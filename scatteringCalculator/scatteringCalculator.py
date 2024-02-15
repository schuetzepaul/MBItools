#!/usr/bin/python3

# This little tool calculates the width of the multiple coulomb scattering angle distribution using the highland formula

import math
import sys
import getopt
import csv

x0_dict = {"alu": [88.97, "Aluminium"]
           , "air": [303900., "Air"]
           , "ni": [14.24, "Nickel"]
           , "pb": [5.612, "Lead"]
           , "w": [3.504, "Tungsten"]
           , "si": [93.70, "Silicon"]
           , "fe": [17.57, "Iron"]
           , "cu": [14.36, "Copper"]
           , "h2o": [360.8, "Water"]
           , "k": [285.7, "Kapton"]
           , "sc": [425.4, "Plastic scintillator"] # Polyvinyltoluene, DESY Telescope scintillators
           , "fs": [122.9, "Fused Silica"]
           , "ti": [35.6, "Titanium"]
           , "gr": [193.2, "Graphite"]
           , "br": [ 356.5, "Brain"]
           , "tis": [376.3, "Tissue"]
           , "bon": [148.2, "Bone"]
           , "pcb": [167.608, "PCB"]
           , "plg": [340.7, "Plexiglass"]
           }

try:
    input = raw_input
except NameError:
    pass

def highland(energy, thickness, x0):
    return 0.0136/energy*math.sqrt(thickness/x0)*(1.+0.038*math.log(thickness/x0))


x0_dict = dict(sorted(x0_dict.items()))

print("\nSpecify the material:")

for key, material in x0_dict.items():
    print(key + ": " + material[1])
print()    

materialChoice = input("Enter your choice: ")

radLength = 0.

if materialChoice=="o":
    radLength = float(input("Enter the radiation length in mm: "))
elif materialChoice in x0_dict.keys():
    radLength = x0_dict[materialChoice][0]
else:
    print("\nPlease choose a valid option next time, dumbass! I'm outta here!\n")
    exit(1)


thickness = float(input("Enter the material thickness in mm: "))

energy = float(input("Enter the particle energy in GeV: "))

angleWidth = highland(energy,thickness,radLength)*1.E3

lateralDisplacement = angleWidth*thickness/math.sqrt(3)

print("\nThe material budget is " + str(thickness/radLength))
print("\nThe RMS angle is " + str(angleWidth) + " mrad\n")
print("\nThe lateral displacement is " + str(lateralDisplacement) + " um\n")
