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

def cutPortion(fmin,fmax,npts,data,low_cut,high_cut):
    fvals = np.linspace(fmax,fmin,npts)
    
    x = fvals[(fvals>low_cut)&(fvals<high_cut)]
    y = data[(fvals>low_cut)&(fvals<high_cut)]
    
    plt.plot(x,y)
    
    return x, y
    
def fitBackground(x,y,roi):
    
    x1 = x[(x>roi[0])&(x<roi[1])]
    y1 = y[(x>roi[0])&(x<roi[1])]

    x2 = x[(x>roi[2])&(x<roi[3])]
    y2 = y[(x>roi[2])&(x<roi[3])]

    x_bas = np.hstack((x1,x2))
    y_bas = np.hstack((y1,y2))

    p = np.polyfit(x_bas,y_bas,1)



    plt.plot(x,y,"k.",label="signal")
    plt.plot(x_bas,y_bas,"b.",label="anchors for fit")
    plt.plot(x,np.polyval(p,x),"r-",label="baseline")
    plt.legend()
    return np.polyval(p,x)

def trapz(x, y):
    # Trapezoidal integration rule
    n = len(x)
    
    r = 0.0

    for i in range(1,n):
        r += (x[i] - x[i-1]) * (y[i] + y[i-1])
    trapz_int = r/2.0
    return trapz_int