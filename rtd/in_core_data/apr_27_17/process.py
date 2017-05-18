from nice_plot import *

"""The wiring sequence is from probe a to probe b to probe c. For each probe,
from RTD 1 to 9.
 
Port assignment:
device 1: 9 RTD in probe a + 5 RTD in probe b
device 2: 4 RTD in probe b + 9 RTD in probe c + the 8th RTD in probe a
The 8th port of the pab device is broken, so the RTD 8 in 
probe a is connected to the last port of the pbc device.

The geometric location of these three probes are

     T                
   O   pc * pa * pb 
     T
   
   O: center of the core
   T: Instrumented fuel
   *: GRid plate flux penetration

The tested power levels are 50 100 250 500 (kW), each lasts for ~15 min with
pump on.

The convertion equation used is
    T = -1338.89 * V + 3014.74
"""

def t2v(a):
    """In measurement, for easy check the realistic temperature, all the RTDs
    use the above equation to convert voltage to temperature. Now we change 
    back and then apply different calibration equations for accuracy.
    """
    voltage = (a - 3014.74) / (-1338.89)
    return voltage

def v2t(voltage, polyn):
    """Apply linear polynomial equation to convert voltage to temperature
       voltage: voltage of 9 RTDs (time * RTD)
       polyn:   polynomial equation for 9 RTDs
    """
    temp = np.zeros(voltage.shape)
    for i in range(len(voltage[0])):
        v_rtd = voltage[:, i]
        ap = polyn[i]
        tmp = np.polyval(ap, v_rtd)
        temp[:, i] = tmp
    return temp

def rtd_plot(time, temp, name):
    """plot the 9 RTD readout of each probe
    """
    plt.figure()
    for i in range(len(temp[0])):
        if i < 7:
            plt.plot(time / 60., temp[:, i], label = 'RTD %i'% (i+1))
        elif i == 7:
            plt.plot(time / 60., temp[:, i], color='gray', label = 'RTD %i'% (i+1))
        elif i == 8:
            plt.plot(time / 60., temp[:, i], color='greenyellow', label = 'RTD %i'% (i+1))
    plt.xlabel('Time (min)')
    plt.ylabel('Temperature ($^o$C)')
    plt.legend(loc = 0)
    plt.savefig('%s.pdf'%name)

# calibration equations for different RTDs
pa_cal = np.loadtxt('pa_kw_cal_eq.txt')
# since in calibration, the toppest RTD of probe a is strange, so no data
# for this RTD. Using the bottom RTd results instead, which is listed above
pa_cal = np.vstack((pa_cal, pa_cal[0]))
pb_cal = np.loadtxt('probeb_kw_cal_eq.txt')
pc_cal = np.loadtxt('probec_kw_cal_eq.txt')


pab1 = np.loadtxt('139_pab_0.dat') 
pab2 = np.loadtxt('139_pab_1.dat')
pab = np.concatenate((pab1, pab2))

pbc1 = np.loadtxt('166_pbc_0.dat')
pbc2 = np.loadtxt('166_pbc_1.dat')
pbc = np.concatenate((pbc1, pbc2))

# since the two recording devices are not start at the exact same time (an 
# difference about 1s, so truncate the first few rows in the first device, 
# which start earlier
diff = len(pab) - len(pbc)
pab = pab[diff : ]

# the first column is the time in second 
time = pab[:, 0] - pab[0, 0]

# probe a
pa = pab[:, 1 : 10]
# the 8th rtd of probe a
rtd8 = pbc[:, -1]
pa[:, 7] = rtd8

# probe b
pb = pab[:, 10 : ]
pb2 = pbc[:, 1 : 5]
pb = np.concatenate((pb, pb2), axis = 1)

# probe c
pc = pbc[:, 5 : -1]

# apply different convertion equations
pa = t2v(pa)
pa = v2t(pa, pa_cal)
pb = t2v(pb)
pb = v2t(pb, pb_cal)
pc = t2v(pc)
pc = v2t(pc, pc_cal)    

np.savetxt('time_pump.txt', time)
np.savetxt('center_pump.txt', pc)
np.savetxt('middle_pump.txt', pa)
np.savetxt('out_pump.txt', pb)

rtd_plot(time, pa, 'probea')
rtd_plot(time, pb, 'probeb')
rtd_plot(time, pc, 'probec')

"""*************************************************************************
In the second phase, the pump is off. The power levels are 100 -> 250
-> 100 kw, each lasts for 30 min.
"""
pab1 = np.loadtxt('139_pab_nopump_100kw_0.dat') 
pab2 = np.loadtxt('139_pab_nopump_100kw_1.dat')
pab = np.concatenate((pab1, pab2))

pbc1 = np.loadtxt('166_pbc_nopump_100kw_0.dat')
pbc2 = np.loadtxt('166_pbc_nopump_100kw_1.dat')
pbc = np.concatenate((pbc1, pbc2))

# since the two recording devices are not start at the exact same time 
# so truncate the first few rows of the start-earlier device.
diff = len(pbc) - len(pab)
pbc = pbc[diff : ]

# the first column is the time in second 
time = pab[:, 0] - pab[0, 0]

# probe a
pa = pab[:, 1 : 10]
# the 8th rtd of probe a
rtd8 = pbc[:, -1]
pa[:, 7] = rtd8

# probe b
pb = pab[:, 10 : ]
pb2 = pbc[:, 1 : 5]
pb = np.concatenate((pb, pb2), axis = 1)

# probe c
pc = pbc[:, 5 : -1]

# apply different convertion equations
pa = t2v(pa)
pa = v2t(pa, pa_cal)
pb = t2v(pb)
pb = v2t(pb, pb_cal)
pc = t2v(pc)
pc = v2t(pc, pc_cal)   

np.savetxt('time_nopump.txt', time)
np.savetxt('center_nopump.txt', pc)
np.savetxt('middle_nopump.txt', pa)
np.savetxt('out_nopump.txt', pb)

rtd_plot(time, pa, 'pa_nopump')
rtd_plot(time, pb, 'pb_nopump')
rtd_plot(time, pc, 'pc_nopump')






