from nice_plot import *

d0 = np.loadtxt('2017_5_15_tmpdata_0.dat')
d1 = np.loadtxt('2017_5_15_tmpdata_1.dat')
d2 = np.loadtxt('2017_5_15_tmpdata_2.dat')

data = np.append(d0, d1, 0)
data = np.append(data, d2, 0)
# time in second
time = data[:, 0] - data[0, 0]
probec = data[:, 5 :]
# convert back to voltage
probec = (probec - 3014.74) / (-1338.89) 

# calibration equation
polyn = np.loadtxt('probec_kw_cal_eq.txt')
for i in range(9):
    apoly = polyn[i]
    probec[:, i] = np.polyval(apoly, probec[:, i])
    if i < 7:
        plt.plot(time/60., probec[:, i], label = 'RTD %i'%(i+1))
    elif i == 7:
        plt.plot(time/60., probec[:, i], color = 'gray', label = 'RTD %i'%(i+1))
    elif i == 8:
        plt.plot(time/60., probec[:, i], color = 'greenyellow', label = 'RTD %i'%(i+1))
plt.xlabel('Time (min)')
plt.ylabel('Temperature ($^o$C)')
plt.legend(loc = 'upper right')
plt.xlim(xmax=170)
plt.savefig('probec.pdf')

# store the calibrated temperature
processed = np.zeros((len(data), 10))
processed[:, 0] = time
for i in range(9):
    processed[:, i+1] = probec[:, i]
np.savetxt('temperature.txt', processed)