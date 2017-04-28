from nice_plot import *

temp = range(30, 81, 5)
# radiated rtd (pc) standard wiring
lib_rtd_std = []
# calibrated probe
lib_cal = []
for t in temp:
    afile1 = '../results2/rad_std_%i_0.dat' % t
    afile2 = '../results2/rad_std_cal_%i_0.dat' % t
    adata1 = np.loadtxt(afile1)[:, 1 : ]
    adata2 = np.loadtxt(afile2)[:, 1 : ]
    # get only the used readout
    adata1 = adata1[:, 0 : : 2]
    adata2 = adata2[:, 0 : : 2]
    tmp_rad = []
    for i in range(len(adata1[0])):
        value = np.average(adata1[:, i])
        tmp_rad.append(value)
    for i in range(len(adata2[0])):
        value = np.average(adata2[:, i])
        if i != len(adata2[0]) - 1:
            tmp_rad.append(value)
        else:
            lib_cal.append(value)
    lib_rtd_std.append(tmp_rad)
    
lib_rtd_std = np.array(lib_rtd_std)
lib_cal = np.array(lib_cal)
ap = np.polyfit(lib_rtd_std[:, 0], temp, 1)
fit = np.polyval(ap, lib_rtd_std[:, 0])
# radiated probe
plt.figure()
for i in range(len(lib_rtd_std[0])):
    if i < 7:
        plt.plot(lib_rtd_std[:, i], temp, '*', label = 'RTD %i'%i, ms=8)
    else:
        plt.plot(lib_rtd_std[:, i], temp, 's', label = 'RTD %i'%i, ms=8)
plt.plot(lib_rtd_std[:, 0], fit, 'k-')
plt.text(2.192, 50, 'T = %.2f V + %.2f\nFitting using the RTD0 data'%\
         (ap[0], ap[1]))
plt.legend(loc = 0)
plt.ylabel('Temperature ($^o$C)')
plt.xlabel('Voltage (V)')
# plt.grid()
plt.ylim((25, 85))
plt.savefig('rad_pc_std.pdf')
plt.savefig('rad_pc_std.png')

# calibrated RTD
plt.figure()
plt.plot(lib_cal, temp, '*k')
plt.ylabel('Temperature ($^o$C)')
plt.xlabel('Voltage (V)')
# plt.grid()
plt.ylim((25, 85))
plt.savefig('cal_rtd.pdf')
plt.savefig('cal_rtd.png')

# radiated rtd using kevin's wiring
rad_k = []
for t in temp:
    afile = '../results2/rad_kw_%i_0.dat' % t
    adata = np.loadtxt(afile)[:, 1 : ] 
    tmp = []
    for i in range(len(adata[0])):
        ave = np.average(adata[:, i])
        tmp.append(ave)
    rad_k.append(tmp)
rad_k = np.array(rad_k)

# save the calibration results
polyn = []
for i in range(len(rad_k[0])):
    tmp = np.polyfit(rad_k[:, i], temp, 1)
    polyn.append(tmp)
np.savetxt('probec_kw_cal_eq.txt', polyn)

ap = np.polyfit(rad_k[:, 0], temp, 1)
fit = np.polyval(ap, rad_k[:, 0])
plt.figure()
for i in range(len(rad_k[0])):
    if i < 7:
        plt.plot(rad_k[:, i], temp, '*', label = 'RTD %i'%i, ms=8)
    else:
        plt.plot(rad_k[:, i], temp, 's', label = 'RTD %i'%i, ms=8)
plt.plot(rad_k[:, 0], fit, 'k-')
plt.text(2.192, 50, 'T = %.2f V + %.2f\nFitting using the RTD0 data'%\
         (ap[0], ap[1]))
plt.legend(loc = 0)
plt.ylabel('Temperature ($^o$C)')
plt.xlabel('Voltage (V)')
# plt.grid()
plt.ylim((25, 85))
plt.savefig('rad_pc_k.pdf')
plt.savefig('rad_pc_k.png')

# probe b using kevin wiring
pb = []
for t in temp:
    afile = '../results2/pb_kw_%i_0.dat' % t
    adata = np.loadtxt(afile)[:, 1 : ] 
    tmp = []
    for i in range(len(adata[0])):
        ave = np.average(adata[:, i])
        tmp.append(ave)
    pb.append(tmp)
pb = np.array(pb)

# save the calibration equations
polyn = []
for i in range(len(pb[0])):
    tmp = np.polyfit(pb[:, i], temp, 1)
    polyn.append(tmp)
np.savetxt('probeb_kw_cal_eq.txt', polyn)

# fitting
ap = np.polyfit(pb[:, 0], temp, 1)
fit = np.polyval(ap, pb[:, 0])
plt.figure()
for i in range(len(pb[0])):
    if i < 7:
        plt.plot(pb[:, i], temp, '*', label = 'RTD %i'%i, ms=8)
    else:
        plt.plot(pb[:, i], temp, 's', label = 'RTD %i'%i, ms=8)
plt.plot(pb[:, 0], fit, 'k-')
plt.text(2.195, 45, 'T = %.2f V + %.2f\nFitting using the RTD cloest to \nthe deliver water port, i.e., RTD 0'%\
         (ap[0], ap[1]))
plt.legend(loc = 0)
plt.ylabel('Temperature ($^o$C)')
plt.xlabel('Voltage (V)')
# # plt.grid()
plt.ylim((25, 85))
plt.savefig('pb_k.pdf')
plt.savefig('pb_k.png')
exit()





plt.figure()
for i in range(len(lib[0])):
    # prevent temperature repetition
    if i == len(lib[0]) - 2:
        plt.plot(lib[:, i], temp, '*', color = (.5, .3, .2), label = 'RTD %i'%i)
    elif i == len(lib[0]) - 1:
        plt.plot(lib[:, i], temp, '*', color = (.4, .3, .6), label = 'RTD %i'%i)
    else:
        plt.plot(lib[:, i], temp, '*', label = 'RTD %i'%i)
# plt.legend(loc='upper right', bbox_to_anchor=(1.01, 1.01),
#            framealpha=.3)
plt.legend(loc = 0)
plt.ylabel('Temperature ($^o$C)')
plt.xlabel('Voltage (V)')
# plt.grid()
plt.ylim((20, 65))
plt.savefig('cal_raw_data.pdf')
plt.savefig('cal_raw_data.png')

# find fitting function of each RTD
polyn = []
for i in range(len(lib[0])):
    rtd = lib[:, i]
    polyn.append(np.polyfit(rtd, temp, 1))
print 'standard wiring fitting equation'
print polyn[-1]
print 'Dustin\'s wiring fitting equation'
for i in range(len(polyn[0 : -1])):
    print polyn[i]

core_data = np.loadtxt('../../in_core_data/measure_1_12_16_0.dat')
time = core_data[:, 0] - core_data[0, 0]
rtds = core_data[:, 1 :]
plt.figure()
for i in range(len(rtds[0])):
    artd = rtds[:, i]
    atemp = np.polyval(polyn[i], artd)
    if i == len(lib[0]) - 2:
        plt.plot(time / 60., atemp, '-', color = (.5, .3, .2), label = 'RTD %i'%i)
    elif i == len(lib[0]) - 1:
        plt.plot(time / 60., atemp, '-', color = (.4, .3, .6), label = 'RTD %i'%i)
    else:
        plt.plot(time / 60., atemp, '-', label = 'RTD %i'%i)
plt.xlabel('Time (min)')
plt.ylabel('Temperature ($^o$C)')
# plt.grid()
plt.legend(loc = 0)
plt.savefig('core_rtd.pdf')
plt.savefig('core_rtd.png')

# Kevin's wiring method
lib = []
# the last RTD seems innormal
for t in temp:
    afile = '../results/t%i_pa_0.dat'%t
    adata = np.loadtxt(afile)[:, 1 : -1]
    tmp = []
    for i in range(len(adata[0])):
        tmp.append(np.average(adata[:, i]))
    lib.append(tmp)
lib = np.array(lib)
plt.figure()
for i in range(len(lib[0])):
    if i < 2:
        plt.plot(lib[:, i], temp, 's', label = 'RTD %i'%i)
    else:
        plt.plot(lib[:, i], temp, '*', label = 'RTD %i'%i)
plt.xlabel('Voltage (V)')
plt.ylabel('Temperature ($^o$C)')
# plt.grid()
plt.ylim((20, 65))
plt.legend()

polyn = []
for i in range(len(lib[0])):
    ap = np.polyfit(lib[:, i], temp, 1)
    polyn.append(ap)
# fitting using the RTD nearing to deliver water
fit = np.polyval(polyn[0], lib[:, 0])
plt.plot(lib[:, 0], fit, 'k-')
plt.text(2.208, 35, 'T = %.2f V + %.2f\nFitting using the RTD cloest to \nthe deliver water port, i.e., RTD 0'%\
         (polyn[0][0], polyn[0][1]))
plt.savefig('rtd_k.pdf')
plt.savefig('rtd_k.png')
print 'fitting eq. using Kevin\'s wiring'
for i in range(len(polyn)):
    print polyn[i]
    
    





