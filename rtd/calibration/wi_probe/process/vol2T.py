""" Transfer an RTD voltage to temperature for real time use.
Hence, do not need to input individual calibration equation in the Labjack software 
manully.

Command line input: RTD voltage
RTD is the ID, as A1, A6, B1, C1, etc.
"""
import numpy as np
import sys

rtd, voltage = sys.argv[1 : 3]

if rtd[0] == 'A' or rtd[0] == 'a':
    poly = np.loadtxt('pAwi_cal_eq.txt')
    
elif rtd[0] == 'B' or rtd[0] == 'b':
    poly = np.loadtxt('pBwi_cal_eq.txt')
    
elif rtd[0] == 'C' or rtd[0] == 'c':
    poly = np.loadtxt('pCwi_cal_eq.txt')
    
else:
    raise SyntaxError('RTD selection is wrong. Accept values are: A-C1-6')

number = int(rtd[1])
tem = np.polyval(poly[number - 1], float(voltage))
print 'RTD %s reads %.2f C' % (rtd, tem)