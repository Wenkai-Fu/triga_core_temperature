from nice_plot import *

def v2t(v):
    r = (2.5 - v) * 1e3 / v
    t = (r - 100.) / .385
    return t

v = np.linspace(2.256, 2.257, 1000)
t = v2t(v)

plt.plot(v, t, 'k-')
plt.xlabel('Voltage (V)')
plt.ylabel('Temperature (C)')
plt.grid()
plt.xticks(rotation=90)
plt.savefig('v2t.pdf')

v_cal = 2.25
v_probe = 2.236
t_cal = v2t(v_cal)
t_probe = v2t(v_probe)

print 'T of calibrate = %.2f, probe = %.2f'%(t_cal, t_probe)

v=2.235
t=v2t(v)
print t