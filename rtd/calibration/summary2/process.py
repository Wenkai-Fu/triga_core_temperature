from nice_plot import *

def ave_std(array):
    """ Compute the average and standard deviation of the average of an array"""
    ave1 = np.average(array)
    ave2 = np.average(array ** 2)
    diff = ave2 - ave1 ** 2
    std = (diff / (len(array) - 1)) ** 0.5
    return ave1, std
    
    
    
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

# calibrated RTD
plt.figure()
plt.plot(lib_cal, temp, '*k')
plt.ylabel('Temperature ($^o$C)')
plt.xlabel('Voltage (V)')
# plt.grid()
plt.ylim((25, 85))
plt.savefig('cal_rtd.pdf')

# radiated rtd using kevin's wiring
rad_k = []
max_re = -1.
for t in temp:
    afile = '../results2/rad_kw_%i_0.dat' % t
    adata = np.loadtxt(afile)[:, 1 : ] 
    tmp = []
    for i in range(len(adata[0])):
        # use the average value to represent the RTD readout at set temperature
        # check the relative error is small enough
        ave, std = ave_std(adata[:, i])
        rel_err = std / ave
        if rel_err > max_re:
            max_re = rel_err
        tmp.append(ave)
    rad_k.append(tmp)
print 'the maximum of the relative error = %.4e' % max_re
rad_k = np.array(rad_k)

# save the calibration results
polyn = []
for i in range(len(rad_k[0])):
    tmp = np.polyfit(rad_k[:, i], temp, 1)
    polyn.append(tmp)
np.savetxt('probec_kw_cal_eq.txt', polyn)

ap = np.polyfit(rad_k[:, 0], temp, 1)
fit = np.polyval(ap, rad_k[:, 0])
mks = ['o', 'v', '^', '<', '>', '8', 's', 'p', '*']
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'gray', 'saddlebrown']
plt.figure()
for i in range(len(rad_k[0])):
    plt.plot(rad_k[:, i], temp, marker = mks[i], color = colors[i], ls='None',
              label = 'RTD %i'%(i+1), ms=8)
plt.grid()
plt.legend(loc = 0)
plt.ylabel('Temperature ($^o$C)')
plt.xlabel('Voltage (V)')
plt.ylim((25, 85))
plt.savefig('rad_pc_k.pdf')

# compute the RTD resistance based on the measured voltage across the 1000-ohm 
# resistor. The total voltage applied to RTD and the resistor is 2.5 V.
rtd_r = 1e3 * (2.5 - rad_k) / rad_k
plt.figure()
for i in range(len(rad_k[0])):
    plt.plot(rtd_r[:, i], temp, marker = mks[i], color = colors[i], ls='None',
              label = 'RTD %i'%(i+1), ms=8)
plt.xlabel('Resistance of the RTD ($\Omega$)')
plt.ylabel('Temperature ($^o$C)')
plt.ylim((25, 85))
plt.grid(True)
plt.legend(loc = 0)
plt.savefig('rtd_resistance_pc.png')

max_r = max(rtd_r[-1])
print 'The max resistance of the RTD is {:.6f} ohm'.format(max_r)
t_coeff = (rtd_r[0, -1] - rtd_r[0, 0]) / (temp[-1] - temp[0])
t0 = rtd_r[0, 0] - t_coeff * 30
print 'The resistance of RTD at temperature at 0C = %.6f ohm'%t0



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



