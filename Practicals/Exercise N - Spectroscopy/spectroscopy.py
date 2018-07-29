import numpy as np
import matplotlib.pyplot as plt
import datetime
import re

def movingWindow(x,y,n):
    ny = y.shape[0]
    out = np.zeros(ny - 2*n)
    for i in range(n,ny-n):
        out[i-n] = np.mean(y[i-n:i+n+1])
    return x[n:ny-n],out

def loadSpectralData(filename):
    data =  np.loadtxt(filename)
    npts = int(data[0])
    fmax = data[1]
    fmin = data[2]
    return fmin,fmax,npts,data[6:]

def plotSpectralData(fmin,fmax,npts,data,filename=None,figsize=(8,6),window=None):
    plt.figure(figsize=figsize)
    fvals = np.linspace(fmax,fmin,npts)
    plt.plot(fvals,data,'r')
    if window is not None:
        fwin,dwin = movingWindow(fvals,data,window)
        plt.plot(fwin,dwin,'k--')
    plt.xlim(fmax,fmin)
    plt.xlabel('Wavenumber (cm${}^{-1}$)')
    plt.ylabel('Reflectance (%)')
    if filename is not None:
        a,b = filename.split('_')
        info = re.match(r'(\d+[a-z]{3})(?P<location>.*?)panel(?P<panel>\d?)s(?P<sample>\d+)',a)
        experimentDate = datetime.datetime.strptime(b.replace('.asp',''),'%Y-%m-%dT%H-%M-%S')
        plt.text(0.1,0.9,experimentDate.strftime('Recorded: %a, %d %b %Y at %X'),transform=plt.gca().transAxes)
        plt.text(0.1,0.85,"Location: %s   Panel: %s   Sample: %s"%(info.group('location'), 
                                                              info.group('panel'), 
                                                              info.group('sample')),transform=plt.gca().transAxes)
        plt.text(0.1,0.8,"Filename: "+filename,transform=plt.gca().transAxes)
    plt.show()
