import matplotlib.pyplot as plt
import numpy as np
import csv
import matplotlib.patches as mpatches

def main():
    '''
    Description of the data files are followed:
    The files with "nopump" are the pump-off measurement, and the others are the pump-on measurement.
    The "139" are the first T7 PRO device, and the "166" are the second one.
    Each file has 15 columns. The first column is the time in second.
    The remaining columns are the RTD readout temperatures in C.
    Since the LogM software will start a new log file if the first log file exceeds a certain size, the "*_1"
    file follows the "*_0" file, i.e., the time are continuous in these two files.
    The port assignments are (the numbering starts at 0):

    The 139 device:
    port          RTD

    0 to 6        RTD 0 to 6 in probe A
    7 is not used (broken)
    8             RTD 8 in probe A
    9 to 13       RTD 0 to 4 in probe B

    The 166 device:
    port          RTD

    0 to 3        RTD 5 to 8 in probe B
    4 to 12       RTD 0 to 8 in probe C
    13            RTD 7 in probe A

    returns plots

    '''

########################################################################################################################
# Load Raw data
    # 139_pab
########################################################################################################################
    pab_0 = read_data('139_pab_0.dat')
    pab_1 = read_data('139_pab_1.dat')

    pab_off =  pab_0[0][-1]

    pab_time = pab_0[0]
    for item in pab_1[0]:
        pab_time.append(item + pab_off )

    pab_dat = []

    for ind, im in enumerate(pab_0[1]):

        li = []
        for itm in im:
            li.append(itm)
        for itm in pab_1[1][ind]:
            li.append(itm)

        pab_dat.append(li)
################################################################
# 166_pbc load
################################################################

    pbc_0 = read_data('166_pbc_0.dat')
    pbc_1 = read_data('166_pbc_1.dat')

    pbc_off =  pbc_0[0][-1]


    pbc_time = pbc_0[0]
    for item in pbc_1[0]:
        pbc_time.append(item + pbc_off )

    pbc_dat = []

    for ind, im in enumerate(pbc_0[1]):

        li = []
        for itm in im:
            li.append(itm)
        for itm in pbc_1[1][ind]:
            li.append(itm)

        pbc_dat.append(li)

################################################################
# 166_pbc nopump load
################################################################

    pbcnp_0 = read_data('166_pbc_nopump_100kw_0.dat')
    pbcnp_1 = read_data('166_pbc_nopump_100kw_1.dat')

    pbcnp_off =  pbcnp_0[0][-1]

    pbcnp_time = pbcnp_0[0]

    for item in pbcnp_1[0]:
        pbcnp_time.append(item + pbcnp_off )

    pbcnp_dat = []

    for ind, im in enumerate(pbcnp_0[1]):

        li = []
        for itm in im:
            li.append(itm)
        for itm in pbcnp_1[1][ind]:
            li.append(itm)

        pbcnp_dat.append(li)


################################################################
# 139_pbc nopump load
################################################################

    pabnp_0 = read_data('139_pab_nopump_100kw_0.dat')
    pabnp_1 = read_data('139_pab_nopump_100kw_1.dat')

    pabnp_off =  pabnp_0[0][-1]

    pabnp_time = pabnp_0[0]
    for item in pabnp_1[0]:
        pabnp_time.append(item + pabnp_off )

    pabnp_dat = []

    for ind, im in enumerate(pabnp_0[1]):

        li = []
        for itm in im:
            li.append(itm)
        for itm in pabnp_1[1][ind]:
            li.append(itm)

        pabnp_dat.append(li)

#######################################################################################################################
# Seperate data by probe qtih pumps
#######################################################################################################################

    pa_dat = pab_dat[:7]
    pa_dat.append(pbc_dat[13])
    pa_dat.append(pab_dat[8])

    pb_dat = pab_dat[9:]
    for item in pbc_dat[:4]:
        pb_dat.append(item)


    pc_dat = pbc_dat[4:13]

#######################################################################################################################
#Generate Times for each probe
#######################################################################################################################
    pa_time = []
    for item in pa_dat:
        pa_time.append([ind * 0.5 for  ind, it in enumerate(item)])
    pb_time = [ind * 0.5 for  ind, it in enumerate(pb_dat[0])]
    pc_time = [ind * 0.5 for  ind, it in enumerate(pc_dat[0])]


#######################################################################################################################
# Seperate data by probe  NO pumps
#######################################################################################################################
    pnpa_dat = pabnp_dat[:7]
    pnpa_dat.append(pbcnp_dat[13])
    pnpa_dat.append(pabnp_dat[8])


    pnpb_dat = pabnp_dat[9:]

    for item in pbcnp_dat[:4]:
        pnpb_dat.append(item)


    pnpc_dat = pbcnp_dat[4:13]

#######################################################################################################################
#Generate Times for each probe
#######################################################################################################################

    pnpa_time = [ind * 0.5 for  ind, it in enumerate(pnpa_dat[0])]
    pnpb_time = [ind * 0.5 for  ind, it in enumerate(pnpb_dat[0])]
    pnpc_time = [ind * 0.5 for  ind, it in enumerate(pnpc_dat[0])]



########################################################################################################################
    # Generate test plots
########################################################################################################################

    #for ind, it in enumerate(pa_dat):
    #    plt.plot(pa_time[ind], it)


########################################################################################################################
    # Create Axially Averaged Data and Times (2Hz sampling rate)
########################################################################################################################
     ####################### pa_sum
    pa_sum = []

    for ind, it in enumerate(pa_dat[0]):
        try:
            pa_sum.append(sum([float(item) for item in [it, pa_dat[1][ind], pa_dat[2][ind], pa_dat[3][ind],
                                                        pa_dat[4][ind], pa_dat[5][ind], pa_dat[6][ind],
                                                        pa_dat[7][ind], pa_dat[8][ind]]])/9)
        except IndexError:
            pass

    ########################### pb_sum
    pb_sum = []

    for ind, it in enumerate(pb_dat[0]):
        try:
            pb_sum.append(sum([float(item) for item in [it, pb_dat[1][ind], pb_dat[2][ind], pb_dat[3][ind], pb_dat[4][ind], pb_dat[5][ind], pb_dat[6][ind], pb_dat[7][ind], pb_dat[8][ind]]])/9)
        except IndexError:
            pass

    ###########################  pc_sum
    pc_sum = []

    for ind, it in enumerate(pc_dat[0]):
        try:
            pc_sum.append(sum([float(item) for item in [it, pc_dat[1][ind], pc_dat[2][ind], pc_dat[3][ind], pc_dat[4][ind], pc_dat[5][ind], pc_dat[6][ind], pc_dat[7][ind], pc_dat[8][ind]]])/9)
        except IndexError:
            pass

    pa_sum_time = [ind * 0.5/60 for ind, item in enumerate(pa_sum)]
    pb_sum_time = [ind * 0.5/60 for ind, item in enumerate(pa_sum)]
    pc_sum_time = [ind * 0.5/60 for ind, item in enumerate(pa_sum)]


    ####################### pnpa_sum
    pnpa_sum = []

    for ind, it in enumerate(pnpa_dat[0]):
        try:
            pnpa_sum.append(sum([float(item) for item in [it, pnpa_dat[1][ind], pnpa_dat[2][ind], pnpa_dat[3][ind], pnpa_dat[4][ind], pnpa_dat[5][ind], pnpa_dat[6][ind], pnpa_dat[7][ind], pnpa_dat[8][ind]]])/9)
        except IndexError:
            pass

    ######################## pnpb_sum
    pnpb_sum = []

    for ind, it in enumerate(pnpb_dat[0]):
        try:
            pnpb_sum.append(sum([float(item) for item in [it, pnpb_dat[1][ind], pnpb_dat[2][ind], pnpb_dat[3][ind], pnpb_dat[4][ind], pnpb_dat[5][ind], pnpb_dat[6][ind], pnpb_dat[7][ind], pnpb_dat[8][ind]]])/9)
        except IndexError:
            pass

    ######################## pnpc_sum
    pnpc_sum = []

    for ind, it in enumerate(pnpc_dat[0]):
        try:
            pnpc_sum.append(sum([float(item) for item in [it, pnpc_dat[1][ind], pnpc_dat[2][ind], pnpc_dat[3][ind], pnpc_dat[4][ind], pnpc_dat[5][ind], pnpc_dat[6][ind], pnpc_dat[7][ind], pnpc_dat[8][ind]]])/9)
        except IndexError:
            pass

######################### Sum Times
    pa_sum_time = [ind * 0.5/60 for ind, item in enumerate(pa_sum)]
    pb_sum_time = [ind * 0.5/60 for ind, item in enumerate(pb_sum)]
    pc_sum_time = [ind * 0.5/60 for ind, item in enumerate(pc_sum)]

    pnpa_sum_time = [ind * 0.5/60 for ind, item in enumerate(pnpa_sum)]
    pnpb_sum_time = [ind * 0.5/60 for ind, item in enumerate(pnpb_sum)]
    pnpc_sum_time = [ind * 0.5/60 for ind, item in enumerate(pnpc_sum)]


########################################################################################################################
#  GENERATE PLOTS Of AXIALLY AVERAGED DATA
########################################################################################################################
    plt.plot(pa_sum_time, pa_sum, 'b', label='Probe A')
    plt.plot(pb_sum_time, pb_sum, 'g', label='Probe B')
    plt.plot(pc_sum_time, pc_sum, 'r', label='Probe C')
    plt.xlabel('Time (Minutes)')
    plt.ylabel('Temperature (Celsius)')
    plt.title('Transient Temperature Data for 3 Probe Multipower Test')

    plt.legend(loc=2)
    plt.savefig('fig_pumps.png')
    plt.show()
    plt.clf()

    plt.plot(pnpa_sum_time, pnpa_sum, 'b', label='Probe A')
    plt.plot(pnpb_sum_time, pnpb_sum, 'g', label='Probe B')
    plt.plot(pnpc_sum_time, pnpc_sum, 'r', label='Probe C')
    plt.xlabel('Time (Minutes)')
    plt.ylabel('Temperature (Celsius)')
    plt.title('Temperature Data for 3 Probe Multipower Test No Pumps')

    plt.legend(loc=2)
    plt.savefig('fig_nopumps.png')
    plt.show()



def read_data(fname):
    '''


    :param fname: filename of loaded file
    :return: Tuple
    1st item is tru_time (adjusted time to start at 0 seconds and step in 0.5 secs)
    2nd item is the data as a list of lists. each list contains a column from the input

    time can be used instead of tru_time to return the time provided by the output file
    '''


    time = []
    data = []
    d = []

    with open(fname, 'rb') as infile:
        spamreader = csv.reader(infile, delimiter='	')
        for row in spamreader:
            time.append(row[0])
            data.append(row[1:])

    ref = data[0]

    for index, item in enumerate(ref):
        d.append([it[index] for it in data])



    tru_time = [index * 0.5 for index, i in enumerate(time)]

    return (tru_time, d)

if __name__ == '__main__':
    main()