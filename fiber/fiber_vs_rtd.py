from nice_plot import *
from configglue.inischema.attributed import marker

# use the processed temperature to save time
fiber = np.loadtxt('rtd.txt')

# continuous the time grids
time = np.loadtxt('FiberTime.csv')
t = np.zeros(len(time))
t[0] = time[0]
delta = 0.0
for i in range(1, len(time)) :
    if time[i] < time[i-1] :
        delta = t[i-1]
    t[i] = time[i] + delta
time = t
# change second to minute
time_min = time / 60.


"""calculate temperature average over steady-state time of a power level
to compare with the RTD measurement. To evaluate the gamma heating effects"""

# select steady-state time index based on time plot
p1s = np.searchsorted(time_min, 12.12)
p1e = np.searchsorted(time_min, 18.)
p2s = np.searchsorted(time_min, 22.8)
p2e = np.searchsorted(time_min, 30.0)
p3s = np.searchsorted(time_min, 33.7)
p3e = np.searchsorted(time_min, 39.4)
p4s = np.searchsorted(time_min, 42.2)
p4e = np.searchsorted(time_min, 48.9)

# axial averaged temperature over time of the 9 RTDs 
axial_fiber = [] # (rtd, power_level)
for i in range(len(fiber[0])):
    artd = fiber[:, i]
    ave_p1 = np.average(artd[p1s : p1e])
    ave_p2 = np.average(artd[p2s : p2e]) 
    ave_p3 = np.average(artd[p3s : p3e])
    ave_p4 = np.average(artd[p4s : p4e])
    axial_fiber.append([ave_p1, ave_p2, ave_p3, ave_p4])
axial_fiber = np.array(axial_fiber)

# -----------------------------------------------------------------------------
# RTD-measured temperature
# -----------------------------------------------------------------------------
rtd_dir = '/home/kevin/workspace/triga_core_temperature/rtd/calibration/summary'
rtd_temp = rtd_dir + '/inCore_rtd_temp.txt'
rtd_time = rtd_dir + '/inCore_time.txt'
rtd_temp = np.loadtxt(rtd_temp)
rtd_time = np.loadtxt(rtd_time)
rtd_time_min = rtd_time / 60.

# steady-state time index
p1s = np.searchsorted(rtd_time_min, 11.54)
p1e = np.searchsorted(rtd_time_min, 17.3)
p2s = np.searchsorted(rtd_time_min, 22.9)
p2e = np.searchsorted(rtd_time_min, 29.8)
p3s = np.searchsorted(rtd_time_min, 33.9)
p3e = np.searchsorted(rtd_time_min, 38.5)
p4s = np.searchsorted(rtd_time_min, 42.7)
p4e = np.searchsorted(rtd_time_min, 48.3)

# axial temperature from RTD measurement
axial_rtd = []
for i in range(len(rtd_temp[0])):
    artd = rtd_temp[:, i]
    p1 = np.average(artd[p1s : p1e])
    p2 = np.average(artd[p2s : p2e])
    p3 = np.average(artd[p3s : p3e])
    p4 = np.average(artd[p4s : p4e])
    axial_rtd.append([p1, p2, p3, p4])
axial_rtd = np.array(axial_rtd)


# RTD locations in the probe
length = 1.2
start = 14.51 + length * 0.5
space = 4.7625
distance = []
for i in range(9):
    d = start + i * space 
    distance.append(d)
    
power = ['50kW', '100kW', '250kW', '500kW']
colors = ['b', 'r', 'g', 'm']
marks = ['o', 'p', 's', '*']

plt.figure()
# fiber temperature
for i in range(len(power)):
    plt.plot(distance, axial_fiber[:, i], color = colors[i], ls = '-',
             marker = marks[i], label = power[i])
# RTD temperature
for i in range(len(power)):
    plt.plot(distance, axial_rtd[:, i], color = colors[i], ls = '--',
             marker = marks[i])
plt.xlabel('Distance from probe tip (cm)')
plt.ylabel('Temperature ($^o$C)')
plt.grid()
plt.legend(loc = 0)
plt.savefig('fiber_vs_rtd.png')





















