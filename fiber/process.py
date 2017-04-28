from nice_plot import *
from mpi4py import MPI
import math

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    data = np.zeros((7307, 9675))
else:
    data = None
local = np.zeros((7307, 9675)) # (time, space)
with open('FiberData.csv', 'r') as f:
    for i, line in enumerate(f):
        if i % 27 == rank:
            aline = line.split(',')
            assert len(aline) == len(local[0])
            for j in range(len(aline)):
                local[i, j] = float(aline[j])
    assert i == 7306
comm.Reduce(local, data, MPI.SUM, 0)
if rank == 0:
    temp = 1.558 * np.absolute(data) ** .8532 + 11.38
    row = len(temp)
    column = len(temp[0])
    for i in range(row):
        for j in range(column):
            # eliminate the nan points
            if math.isnan(temp[i, j]):
                temp[i, j] = 0.
            # eliminate temperature larger than 100 C
            if temp[i, j] > 100.:
                temp[i, j] = 0.
    
    # for imshow using time as x axis
    temp = np.transpose(temp) # (space, time)
    # consistent with the experimental alignment, i.e.,
    # space[0] is the first entry at the probe bottom
    temp = np.flipud(temp)
    
    plt.figure()
    plt.imshow(temp, cmap = 'Blues', origin='lower', interpolation='nearest')
    plt.colorbar()
    plt.xlabel('Time grid')
    plt.ylabel('Sensor number')
    plt.xticks(rotation='vertical')
    plt.savefig('fiber_data.pdf')
    
    time = np.loadtxt('FiberTime.csv')
    t = np.zeros(len(time))
    t[0] = time[0]
    delta = 0.0
    for i in range(1, len(time)) :
        if time[i] < time[i-1] :
            delta = t[i-1]
        t[i] = time[i] + delta
    time = t
    
    """ Assume:
    the first fiber sensor located 14.51 cm from the tip of the probe;
    the gap between each sensor is 0.6 mm
    each RTD has a length of 1.2 cm
    the distance between the center points of two RTDs is 4.7625 cm"""
    # in unit cm
    rtd_len = 1.2
    gap_fiber = 0.06
    gap_rtd = 4.7625
    offset = 14.51
    # number of fiber sensor in a RTD length
    num_fiber = int(rtd_len / gap_fiber)
    
    # Find the fiber index corresponding to the 9 RTDs
    indexes = []
    for i in range(9):
        tmp = []
        z = i * gap_rtd
        # start fiber index
        si = int(z / gap_fiber)
        tmp = range(si, si + num_fiber)
        indexes.append(tmp)
    
    rtd = [] # time, temperature
    for t in range(len(temp[0])):
        # the 9 rtd temperature at a time grid
        rtd_temp = []
        acol = temp[:, t]
        # 9 RTDs
        for i in range(9):
            rt = np.average(acol[indexes[i]])
            rtd_temp.append(rt)
        rtd.append(rtd_temp)
    np.savetxt('rtd.txt', rtd)
    rtd = np.array(rtd)
    
    plt.figure()
    for i in range(len(rtd[0])):
        if i == len(rtd[0]) - 1:
            plt.plot(time / 60., rtd[:, i], '-', color = (.5, .3, .2), 
                     label = 'RTD %i'%i)
        elif i == len(rtd[0]) - 2:
            plt.plot(time/60., rtd[:, i], '-', color=(.4, .3, .6),
                     label = 'RTD %i'%i)
        else:
            plt.plot(time / 60., rtd[:, i], '-', label = 'RTD %i'%i)
    plt.xlabel('Time (min)')
    plt.ylabel('Temperature ($^o$C)')
    plt.legend(loc = 0)
    plt.savefig('fiber_at_rtd.pdf')
    plt.savefig('fiber_at_rtd.png')
    
    # find temperature profile outside the RTD location
    indexes = []
    for i in range(9, 15):
        tmp = []
        z = i * gap_rtd
        # start fiber index
        si = int(z / gap_fiber)
        tmp = range(si, si + num_fiber)
        indexes.append(tmp)
    
    rtd = [] # time, temperature
    for t in range(len(temp[0])):
        # the 9 rtd temperature at a time grid
        rtd_temp = []
        acol = temp[:, t]
        # 9 RTDs
        for i in range(len(indexes)):
            rt = np.average(acol[indexes[i]])
            rtd_temp.append(rt)
        rtd.append(rtd_temp)
    np.savetxt('rtd_out.txt', rtd)
    rtd = np.array(rtd)
    
    plt.figure()
    for i in range(len(rtd[0])):
        plt.plot(time / 60., rtd[:, i], '-', label = 'RTD %i'%(i+9))
    plt.xlabel('Time (min)')
    plt.ylabel('Temperature ($^o$C)')
    plt.legend(loc = 0)
    plt.savefig('fiber_at_out_rtd.pdf')
    plt.savefig('fiber_at_out_rtd.png')
    
    
    
    
    
    
    
    
   
