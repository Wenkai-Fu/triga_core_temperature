from nice_plot import *

def volToTem(voltage):
    v_ref = 2.5
    r = (v_ref - voltage) * 1e3 / voltage
    tem = (r - 100.) / .385
    return tem

def read_data(afile):
    time = []
    voltage = []
    with open(afile, 'r') as f:
        for i, line in enumerate(f):
            tmp = line.split()
            if i == 0:
                t0 = float(tmp[0])
            time.append(float(tmp[0]) - t0)
            temv = []
            for v in tmp[1 : ]: # the last channel is not used
                value = float(v)
                temv.append(value)
            voltage.append(temv)
    return np.array(time), np.array(voltage)

def main():
    fname = '../data/measure_1_12_16_0.dat'
    time, voltage = read_data(fname)
    
    # find the power-off period to calculate correction value
    # according to pre plot, before 400s the reactor is power off
    for i in range(len(time)):
        if time[i] >= 400.:
            loc = i
            break
    
    even = 0.
    odd = 0.
    for i in range(len(voltage[0])):
        if i % 2 == 0 and i != len(voltage[0]) - 1:
            even += np.average(voltage[0 : loc, i])
        elif i % 2 == 1:
            odd += np.average(voltage[0 : loc, i])
    even = even / 4.
    odd = odd / 4.
    cor = even - odd
    for i in range(len(voltage[0])):
        if i % 2 == 1:
            voltage[:, i] = voltage[:, i] + cor
    tem = volToTem(voltage) 
    # plot
    """ time at 7.4 min for the temperature measurement corresponding to time
    0 of the power plot since we need 7.4 min to do the calibration, i.e., 
    calculate correction for the power off period"""
#     time_offset = 7
    for i in range(len(tem[0])):
        if i == len(tem[0]) - 1:
            plt.plot(time/60., tem[:, i],  'k--',  label = 'RTD %i'%i)
        elif i == len(tem[0]) - 2: # avoid color repetition
            plt.plot(time/60., tem[:, i],  color =  (.5, .3, .2), label = 'RTD %i'%i) 
        else:
            plt.plot(time/60., tem[:, i],  label = 'RTD %i'%i)
    plt.legend(loc = 'upper left')
#     plt.xlim(xmin=0)
    plt.grid()
    plt.xlabel('Time (min)')
    plt.ylabel('Temperature ($^\circ$C)')
    plt.savefig('rdt_temp.pdf')

main()
