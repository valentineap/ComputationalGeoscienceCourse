import numpy as np
import matplotlib.pyplot as plt

def simulateDecay(tstep,nTimestep,n0=10000):
    halfLife = {'Rn':3.96,'Pb211':36.1*60,'Bi':2.14*60,'Tl':4.77*60}
    energyRelease = {'Rn':6.946+7.527, 'Pb211':1.367,'Bi':6.751,'Tl':1.418}
    decayRate = {}
    for el,tHalf in halfLife.items():
        decayRate[el] = np.log(2)/tHalf

    time = np.arange(nTimestep)*tstep
    n = {'Rn':np.zeros(nTimestep),
         'Pb211':np.zeros(nTimestep),
         'Bi':np.zeros(nTimestep),
         'Tl':np.zeros(nTimestep),
         'Pb':np.zeros(nTimestep)}
    n['Rn'][0] = n0
    energy = np.zeros(nTimestep)
    for i in range(0,nTimestep-1):
        Rn2Pb = n['Rn'][i]*decayRate['Rn']*tstep
        Pb2Bi = n['Pb211'][i]*decayRate['Pb211']*tstep
        Bi2Tl = n['Bi'][i]*decayRate['Bi']*tstep
        Tl2Pb = n['Tl'][i]*decayRate['Tl']*tstep
        n['Rn'][i+1] = n['Rn'][i] - Rn2Pb
        energy[i+1]+=Rn2Pb*energyRelease['Rn']
        n['Pb211'][i+1] = n['Pb211'][i]+Rn2Pb-Pb2Bi
        energy[i+1]+=Pb2Bi*energyRelease['Pb211']
        n['Bi'][i+1] = n['Bi'][i] + Pb2Bi-Bi2Tl
        energy[i+1]+=Bi2Tl*energyRelease['Bi']
        n['Tl'][i+1] = n['Tl'][i]+Bi2Tl-Tl2Pb
        energy[i+1]+=Tl2Pb*energyRelease['Tl']
        n['Pb'][i+1] = n['Pb'][i] +Tl2Pb
    return time,n,energy
def plotDecay(time,n,figsize=(10,8)):
    plt.figure(figsize=figsize)
    plt.plot(time ,n['Rn'],label='${}^{219}$Rn')
    plt.plot(time, n['Pb211'],label='${}^{211}$Pb')
    plt.plot(time,n['Bi'],label='${}^{211}$Bi')
    plt.plot(time,n['Tl'],label='${}^{207}$Tl')
    plt.plot(time,n['Pb'],label='${}^{207}$Pb')
    plt.legend()
    plt.xticks(np.arange(0,time[-1],3600),np.arange(0,time[-1],3600)/3600)
    plt.yticks([0,n['Rn'][0]*0.5,n['Rn'][0]],[0,50,100])
    plt.xlabel('Time / hours')
    plt.ylabel('% atoms')
    plt.show()
def plotEnergy(time,e,figsize=(10,8)):
    plt.figure(figsize=figsize)
    plt.plot(time ,e)
    plt.legend()
    plt.xticks(np.arange(0,time[-1],3600),np.arange(0,time[-1],3600)/3600)
    plt.xlabel('Time / hours')
    plt.ylabel('Total Energy Released / MeV')
    plt.yscale('log')
    plt.show()
def calculateAge(n,Pb211ratio):
    nTimestep = n['Pb'].size
    for i in range(0,nTimestep):
        if n['Pb'][i]>0:
            if n['Pb211'][i]/n['Pb'][i]<Pb211ratio:
                break
    print("%i:%i:%04.1f"%(int(time[i]//3600),int(time[i]%3600)//60,(time[i]%3600)%60))