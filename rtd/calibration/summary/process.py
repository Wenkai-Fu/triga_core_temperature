from nice_plot import *

temp = range(25, 61, 5)
lib = []
for t in temp:
    afile = '../results/t%i_rad_0.dat' % t
    # 9 RTDs readout at each temperature, eliminate the first time column
    adata = np.loadtxt(afile)[:, 1 : ] 
    tmp = []
    # calculate average of each RTD
    for i in range(len(adata[0])):
        rtd = adata[:, i]
        value = np.average(rtd)
        tmp.append(value)
    lib.append(tmp)
lib = np.array(lib) # time * rtd
plt.figure()
for i in range(len(lib[0])):
    # prevent temperature repetition
    if i == len(lib[0]) - 2:
        plt.plot(lib[:, i], temp, '*', color = (.5, .3, .2), label = 'RTD %i'%i)
    elif i == len(lib[0]) - 1:
        plt.plot(lib[:, i], temp, '*', color = (.4, .3, .6), label = 'RTD %i'%i)
    else:
        plt.plot(lib[:, i], temp, '*', label = 'RTD %i'%i)
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
# note the RTD 9 is not included
np.savetxt('pa_kw_cal_eq.txt', polyn)

# fitting using the RTD nearing to deliver water
fit = np.polyval(polyn[0], lib[:, 0])
plt.plot(lib[:, 0], fit, 'k-')
plt.text(2.208, 35, 'T = %.2f V + %.2f\nFitting using the RTD cloest to \nthe deliver water port, i.e., RTD 0'%\
         (polyn[0][0], polyn[0][1]))
plt.savefig('pa_k.pdf')
plt.savefig('pa_k.png')
print 'fitting eq. using Kevin\'s wiring'
for i in range(len(polyn)):
    print polyn[i]
    
    





