from nice_plot import *

aarray = np.random.rand(6, 4)
print aarray
plt.imshow(aarray, cmap = 'Blues', origin='lower', interpolation='none', 
           aspect = 'equal')
plt.colorbar()
plt.xticks(range(4), np.ones(4))
plt.xlabel('Time')
plt.savefig('imshow.pdf')