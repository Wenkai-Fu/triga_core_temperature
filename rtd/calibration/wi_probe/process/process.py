from nice_plot import *

# avetage voltage over time of the three new UW probes at 25.3 and 22.3C
pa_avev = np.zeros((6, 2))
pb_avev = np.zeros((6, 2))
pc_avev = np.zeros((6, 2))

# measured voltage of the new WI probes in air, T = 25.3C
labjack139 = np.loadtxt('../wenkaifu/pAB_139_25.dat')
labjack166 = np.loadtxt('../wenkaifu/pC_166_25.dat')
pa = labjack139[:, 1 : 7]
pb = labjack139[:, -6 :]
pc = labjack166[:, 1 : 7]
# average over time
pa_avev[:, 0] = np.average(pa, axis = 0)
pb_avev[:, 0] = np.average(pb, axis = 0)
pc_avev[:, 0] = np.average(pc, axis = 0)

# measured voltage of the new WI probes in air, T = 22.3C
labjack139 = np.loadtxt('../wenkaifu/pab_139_22.dat')
labjack166 = np.loadtxt('../wenkaifu/pc_166_22.dat')
pa = labjack139[:, 1 : 7]
pb = labjack139[:, -6 :]
pc = labjack166[:, 1 : 7]
# average over time
pa_avev[:, 1] = np.average(pa, axis = 0)
pb_avev[:, 1] = np.average(pb, axis = 0)
pc_avev[:, 1] = np.average(pc, axis = 0)

# plot average voltage vs temperature
tem = [25.3, 22.3]
markers = ['sb-', '*g-', 'Dr-', 'hm-', 'pc-', 'vk-']
plt.figure()
for i in range(6):
    plt.plot(pa_avev[i], tem, markers[i], label = 'RTD%i' % (i+1))
plt.grid()
plt.xlabel('Voltage (V)')
plt.ylabel('Temperature (C)')
plt.legend(loc = 0)
plt.savefig('pa_uw_cal.pdf')

plt.figure()
for i in range(6):
    plt.plot(pb_avev[i], tem, markers[i], label = 'RTD%i' % (i+1))
plt.grid()
plt.xlabel('Voltage (V)')
plt.ylabel('Temperature (C)')
plt.legend(loc = 0)
plt.savefig('pb_uw_cal.pdf')

plt.figure()
for i in range(6):
    plt.plot(pc_avev[i], tem, markers[i], label = 'RTD%i' % (i+1))
plt.grid()
plt.xlabel('Voltage (V)')
plt.ylabel('Temperature (C)')
plt.legend(loc = 0)
plt.savefig('pc_uw_cal.pdf')

# fit equations
polyA = []
for i in range(6):
    poly = np.polyfit(pa_avev[i], tem, deg = 1)
    polyA.append(poly)
np.savetxt('pAwi_cal_eq.txt', polyA)

polyB = []
for i in range(6):
    poly = np.polyfit(pb_avev[i], tem, deg = 1)
    polyB.append(poly)
np.savetxt('pBwi_cal_eq.txt', polyB)

polyC = []
for i in range(6):
    poly = np.polyfit(pc_avev[i], tem, deg = 1)
    polyC.append(poly)
np.savetxt('pCwi_cal_eq.txt', polyC)


# check the fit equation with Dustin's in-pool results
labjack139 = np.loadtxt('../dustin/139_cal_0.dat')
labjack166 = np.loadtxt('../dustin/166_cal_0.dat')


# readout of original probe b, RTD 1 to 8
ogb1 = labjack139[:, 1 : 7]
ogb2 = labjack166[:, -2 : ]

# calibration equation of the 9 RTDs in old probe b
eqb = np.loadtxt('/home/kevin/workspace/triga_core_temperature_old/rtd/calibration/summary2/probeb_kw_cal_eq.txt')

# temperature measured by the original probe b, 8 RTDs
tem = []
# loop over  RTD 1 to 6 in original probe b
for i in range(len(ogb1[0])):
    rtd = ogb1[:, i]
    aveV = np.average(rtd)
    poly = eqb[i]
    aT = np.polyval(poly, aveV)
    tem.append(aT)
# loop over RTD 7 & 8 in original probe b
for i in range(len(ogb2[0])):
    rtd = ogb2[:, i]
    aveV = np.average(rtd)
    poly = eqb[i + 6]
    aT = np.polyval(poly, aveV)
    tem.append(aT)
    
print 'measured temperature of the 8 RTDs in original probe b'
print tem
aveTog = np.average(tem)
std = np.std(tem, ddof = 1)
print 'average T measured by original probe b = %.2f +- %.2f' % (aveTog, std)

# readout of three wi probes
pbwi = labjack139[:, -6 : ]
pawi = labjack166[:, 1 : 7]
pcwi = labjack166[:, 7 : 13]

# average over time
pa_avev = np.average(pawi, axis = 0)
pb_avev = np.average(pbwi, axis = 0)
pc_avev = np.average(pcwi, axis = 0)

# calculate temperature by fitted equation
ta = []
tb = []
tc = []
for i in range(6):
    tmp = np.polyval(polyA[i], pa_avev[i])
    ta.append(tmp)
    tmp = np.polyval(polyB[i], pb_avev[i])
    tb.append(tmp)
    tmp = np.polyval(polyC[i], pc_avev[i])
    tc.append(tmp)
print '\ncalculated T of probe A using fitted equation'
print ta

print '\ncalculated T of probe B using fitted equation'
print tb

print '\ncalculated T of probe C using fitted equation'
print tc





