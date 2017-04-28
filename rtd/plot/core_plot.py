import csv
from datetime import timedelta
from numpy import trapz
from nice_plot import *

dates=[]
time=[]
nmp=[]
nlw=[]
fuel=[]
npp=[]

csvfile = open('../data/wutang.txt')
csvfilereader = csv.reader(csvfile)
# nmp channel 
#Turns csv reader object into list of lists and assings it the variable name values.
values=list(csvfilereader)
for list in values:
    dates.append(list[0])
    time.append(list[1])
    nmp.append(list[2])
    nlw.append(list[4])
    fuel.append(list[6])
    if len(list)-1 == 8:
        npp.append(list[8])

# nmp: power pencentage
# nlw: calculate power range
# fule: temperature of one of the B ring rod in degree C
print 'nmp'
print nmp[0 : 10]
print 'nlw'
print nlw[0 : 10]
print 'fuel'
print fuel[0 : 10]
print 'npp'
print npp[0 : 10]

#Splitting the unnecessary string in the time list
time1=[]    
for thestring in time:
    a=thestring.replace(";01", "")
    time1.append(a)
print 'time1'
print time1

total_time=[]
#Converting the time from military standard "00:00:00" to "0"s
for thestring1 in time1:
    (h,m,s)=thestring1.split(":")
    t=int(h)*3600+int(m)*60+int(s)
    total_time.append(t)    

#Converting the lists from the default strings to floats 
nlw=map(float,nlw)
nmp=map(float,nmp)
fuel=map(float,fuel)
npp=map(float,npp)

"""
For loop to convert the percentages in the nmp channel to powers by:
1) Finding out what range the power is in>>>(1):10mW, (2):100mW, 
   (3):1W, (4):10W, (5):100W, (6):1kW, (7):10kW, (8):100kW, (9):1000kW
    
2) Comparing the percentage difference for all power options between the 
   nmp and nlw channels to find out the least error
    
3) Computing lowest error percent gives us the right range of power based 
   on which power level is closest to nmp
    
4) If statement to find the lowest error between the options and setting 
   the power, respectively"""

new_nmp=[]
for i in range(len(nmp)):
	#power in W 
	power_1=(nmp[i]/100)*.01
	power_2=(nmp[i]/100)*.1
	power_3=(nmp[i]/100)*1
	power_4=(nmp[i]/100)*10
	power_5=(nmp[i]/100)*100
	power_6=(nmp[i]/100)*1000
	power_7=(nmp[i]/100)*10000
	power_8=(nmp[i]/100)*100000
	power_9=(nmp[i]/100)*1000000

	error_1=abs(power_1-1000*nlw[i])/100
	error_2=abs(power_2-1000*nlw[i])/100
	error_3=abs(power_3-1000*nlw[i])/100
	error_4=abs(power_4-1000*nlw[i])/100
	error_5=abs(power_5-1000*nlw[i])/100
	error_6=abs(power_6-1000*nlw[i])/100
	error_7=abs(power_7-1000*nlw[i])/100
	error_8=abs(power_8-1000*nlw[i])/100
	error_9=abs(power_9-1000*nlw[i])/100

	if min(error_1,error_2,error_3,error_4,error_5,error_6,error_7,error_8,error_9)==error_1:
		power=0.01
	elif min(error_1,error_2,error_3,error_4,error_5,error_6,error_7,error_8,error_9)==error_2:
		power=.1
	elif min(error_1,error_2,error_3,error_4,error_5,error_6,error_7,error_8,error_9)==error_3:
		power=1
	elif min(error_1,error_2,error_3,error_4,error_5,error_6,error_7,error_8,error_9)==error_4:
		power=10
	elif min(error_1,error_2,error_3,error_4,error_5,error_6,error_7,error_8,error_9)==error_5:
		power=100
	elif min(error_1,error_2,error_3,error_4,error_5,error_6,error_7,error_8,error_9)==error_6:
		power=1000
	elif min(error_1,error_2,error_3,error_4,error_5,error_6,error_7,error_8,error_9)==error_7:
		power=10000
	elif min(error_1,error_2,error_3,error_4,error_5,error_6,error_7,error_8,error_9)==error_8:
		power=100000
	else:
		power=1000000	

	value=(nmp[i]/100.0)*power
	new_nmp.append(value)

#Converting the nmp channel from W to kw
new1_nmp = np.array(new_nmp) / 1e3
    
imin = np.argmin(new1_nmp)
print 'min of nmp: @ %i = %.2f' % (imin, new1_nmp[imin])

#Trapozodial method for integration:knowing that the increment is 1 second
area1=trapz(new1_nmp, dx=1)
print ("NMP Channel",area1)

area2=trapz(nlw, dx=1)
print ("NLW Channel",area2)


# only plot the power larger than 5 kw
# nnot = []
# for index, item in enumerate(new1_nmp):
# 	if item > 5:
# 		nnot.append(index)

time = []
nmp = []
for i in range(len(new1_nmp)):
    if new1_nmp[i] > 5.:
        time.append(total_time[i])
        nmp.append(new1_nmp[i])
print 'min of nmp = %.2f' % min(nmp)
print 'start at time %.2e min' % ((time[1]-time[0])/60.)
plt.plot((np.array(time)-time[0]) / 60., nmp, 'k-')
plt.grid()
plt.xlabel('Time (min)')
plt.ylabel('Power (kW)')
plt.savefig('power.pdf')

plt.figure()
temp = []
with open('../data/wutang.txt') as f:
    for i, line in enumerate(f):
        tmp = line.split()
        for item in tmp:
            if ';04,' in item[-4 : ]:
                loc = item.index(',')
                temp.append(float(item[0 : loc]))
total_time = np.array(total_time)
plt.plot((np.array(total_time)-total_time[0]) / 60., temp, 'k-')
plt.xlabel('Time (min)')
plt.ylabel(r'Fuel temperature ($^o$C)')
plt.grid()
plt.savefig('fuel_temp.png')

# ind_s = nnot[0]
# ind_e = nnot[-1]
# 
# print ind_s, ind_e
# 
# nl = nlw[ind_s : ind_e]
# nn =  new1_nmp[ind_s : ind_e]
# tt = total_time[ind_s : ind_e]
# 
# print 'min nn = %.2f' % min(nn)
# print len(tt), len(total_time)
# plt.figure()
# plt.plot(tt,nn)
# plt.savefig('plot1.pdf')
# 
# plt.figure()
# tt =[(item - tt[0]) / 60 for item in tt]
# plt.plot(tt,nl)
# plt.xlabel('Time(min)')
# plt.ylabel('Power(kW)')
# plt.xlim([0, 43])

