import numpy as np 
from matplotlib import pyplot as plt 
"""
------------------VARIAZIONE DEL NUMERO DI BLOCCHI------------------------------
"""

plt.figure()
times = np.array([
    [5.333, 5.906, 5.260, 5.270, 5.238],
    [26.444,25.892, 30.473,24.635, 24.789],
    [46.848, 46.734,47.001,48.495, 46.758],
    [68.816,72.816,70.597,68.550,68.480],
    [91.651,90.456,90.196,90.456,90.456],
    [113.866,112.241,112.549,112.549,112.549],
    [135.194,133.962,133.835,133.962,133.962]
])

times_std = np.array([
    [2.195, 2.297, 2.252],
    [2.298,2.276,2.299],
    [2.267,2.172,2.283],
    [2.457,2.315,2.276],
    [2.195,2.229,2.235],
    [2.206,2.209,2.232],
    [2.214,2.102,2.158]
])


mean_time = np.mean(times,axis=1)
mean_time_std = np.mean(times_std,axis=1)
plt.title('Variazione tempo di completamento simulatore a blocchi,\nal variare del numero di blocchi\n(Vicinato = 7 iterazioni = 100 Env= 50x50_60)')
plt.grid(True)
plt.xlabel('Numero di blocchi')
plt.ylabel('Tempo di completamento (sec)')
plt.tight_layout()
plt.plot([1,10,20,30,40,50,60],mean_time,marker = 's',markersize=7,label='Simulatore Smart a blocchi')
plt.plot([1,10,20,30,40,50,60],mean_time_std,marker = 'o',markersize=7,label='Simulatore Standard a blocchi')
plt.legend(loc='best')
#plt.show()
plt.savefig('../Results/Plots/variazione_sim_blocchi.png')


plt.figure()
mean_time = np.mean(times,axis=1)
mean_time_std = np.mean(times_std,axis=1)
plt.title('Variazione rapporto tempo(sim_block_smart)/tempo(sim_block_std),\nal variare del numero di blocchi\n(Vicinato = 7 iterazioni = 100 Env= 50x50_60)')
plt.grid(True)
plt.xlabel('Numero di blocchi')
plt.ylabel('Tempo_Smart / Tempo_Standard')
plt.tight_layout()
plt.plot([1,10,20,30,40,50,60],mean_time/mean_time_std,marker = 's',markersize=7,label='t(sim_smart)/t(sim_std)')
#plt.plot([10,20,30,40,50,60],mean_time_std,marker = 'o',markersize=7,label='Simulatore Standard')
plt.legend(loc='best')
#plt.show()
plt.savefig('../Results/Plots/variazione_sim_blocchi_rel.png')

"""
------------------VARIAZIONE DI K------------------------------
"""

plt.figure()
times = np.array([
    [113.916,114.544,114.071],
    [113.707, 114.214, 114.776],
    [114.065,114.175,115.759],
    [114.097,112.856,114.339],
    [114.118,116.107,114.157]
])

times_std = np.array([
    [1.691,1.776,1.782],
    [2.086,1.908,1.933],
    [1.993,1.940,1.930],
    [1.935,2.001,2.011],
    [2.083,2.061,2.098]
])


mean_time = np.mean(times,axis=1)
mean_time_std = np.mean(times_std,axis=1)
plt.title('Variazione tempo di completamento simulatore classico,\nal variare del raggio del vicinato\n(iterazioni = 100 Env= 50x50_60)')
plt.grid(True)
plt.xlabel('Raggio del vicinato')
plt.ylabel('Tempo di completamento (sec)')
plt.tight_layout()
plt.plot([3,5,7,9,11],mean_time,marker = 's',markersize=7,label='Simulatore Smart')
plt.plot([3,5,7,9,11],mean_time_std,marker = 'o',markersize=7,label='Simulatore Standard')
plt.legend(loc='best')
#plt.show()
plt.savefig('../Results/Plots/variazione_sim_vicinato.png')


plt.figure()
mean_time = np.mean(times,axis=1)
mean_time_std = np.mean(times_std,axis=1)
plt.title('Variazione rapporto tempo(sim_smart)/tempo(sim_std),\nal variare del raggio del vicinato\n(iterazioni = 100 Env= 50x50_60)')
plt.grid(True)
plt.xlabel('Raggio del vicinato')
plt.ylabel('Tempo_Smart / Tempo_Standard')
plt.tight_layout()
plt.plot([3,5,7,9,11],mean_time/mean_time_std,marker = 's',markersize=7,label='t(sim_smart)/t(sim_std)')
#plt.plot([10,20,30,40,50,60],mean_time_std,marker = 'o',markersize=7,label='Simulatore Standard')
plt.legend(loc='best')
#plt.show()
plt.savefig('../Results/Plots/variazione_sim_vicinato_rel.png')


"""
------------------VARIAZIONE DEL NUMERO DI AGENTI------------------------------
"""

plt.figure()
times = np.array([
    [26.314,27.730,28.420],
    [52.525,50.043,51.438],
    [73.483,73.552,72.837],
    [97.779,96.958,96.690],
    [113.708,116.771,113.764],
    [136.004, 138.957, 138.013]
])

times_std = np.array([
    [0.872,0.889,0.930],
    [1.148,1.135,1.154],
    [1.489,1.416,1.498],
    [1.786,1.825,1.770],
    [1.984,1.884,1.970],
    [2.196,2.091,2.179]
])


mean_time = np.mean(times,axis=1)
mean_time_std = np.mean(times_std,axis=1)
plt.title('Variazione tempo di completamento simulatore classico,\nal variare del numero di agenti\n(Vicinato = 7 iterazioni = 100 Env= 50x50_*)')
plt.grid(True)
plt.xlabel('Numero di agenti')
plt.ylabel('Tempo di completamento (sec)')
plt.tight_layout()
plt.plot([10,20,30,40,50,60],mean_time,marker = 's',markersize=7,label='Simulatore Smart')
plt.plot([10,20,30,40,50,60],mean_time_std,marker = 'o',markersize=7,label='Simulatore Standard')
plt.legend(loc='best')
#plt.show()
plt.savefig('../Results/Plots/variazione_sim_agenti.png')

plt.figure()
mean_time = np.mean(times,axis=1)
mean_time_std = np.mean(times_std,axis=1)
plt.title('Variazione rapporto tempo(sim_smart)/tempo(sim_std),\nal variare del numero di agenti\n(Vicinato = 7 iterazioni = 100 Env= 50x50_*)')
plt.grid(True)
plt.xlabel('Numero di agenti')
plt.ylabel('Tempo_Smart / Tempo_Standard')
plt.tight_layout()
plt.plot([10,20,30,40,50,60],mean_time/mean_time_std,marker = 's',markersize=7,label='t(sim_smart)/t(sim_std)')
#plt.plot([10,20,30,40,50,60],mean_time_std,marker = 'o',markersize=7,label='Simulatore Standard')
plt.legend(loc='best')
#plt.show()
plt.savefig('../Results/Plots/variazione_sim_agenti_rel.png')