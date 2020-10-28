# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 20:41:14 2020

@author: llucv
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import matplotlib.gridspec as gridspec
e=np.e
pi=np.pi

print(e)
print(pi)
print(e**(1j*pi))

def ona_plana(x,y,t,c,x0):
    if x>x0:
        valor=0
    elif x>c*t:
        valor=0
    else:
        valor=e**(1j*(x-c*t))
    return valor

def ona_esf(x,y,x0,y0,t,c):
    r=((x-x0)**2+(y-y0)**2)**(1/2)
    if x<x0:
        valor=0
    elif (r+x0)>c*t:
        valor=0
    else:
        valor=e**(1j*(r-c*t+x0))
    return valor

def intensitat(psi):
    val=(abs(psi))**2
    return val

Lab=np.zeros((101,201),dtype=np.complex_)
Int=np.zeros((101,201))
Ona=np.zeros((101,201))
x=np.zeros((201))
y=np.zeros((101))

xmax=50*pi
ymax=25*pi
pas=ymax/100
print(xmax,ymax,pas)

for i in range(201):
    x[i]=pas*i
    if i<101:
        y[i]=pas*i
        
print(x[0],x[200])
print(y[0],y[100])

""" 
Primer cas: 
fixem el temps per representar una situació instantània
"""
t=350
x0=40
y1=55
y2=15
c=1

print(ona_esf(45,5,x0,y1,t,c))

for i in range(201):
    for j in range(101):
        Lab[j,i]=ona_plana(x[i],y[j],t,c,x0)\
                 +ona_esf(x[i],y[j],x0,y1,t,c)\
                     +ona_esf(x[i],y[j],x0,y2,t,c)
        Int[j,i]=intensitat(Lab[j,i])
        Ona[j,i]=Lab[j,i].real
        
print(Ona.min(),Ona.max())

plt.pcolormesh(x,y,Ona,vmin=Ona.min(),vmax=Ona.max())
plt.show()
plt.pcolormesh(x,y,Int,vmin=Int.min(),vmax=Int.max())
plt.show()

x0=40
c=1
y1=55
y2=15

fig = plt.figure()
ax1 = plt.subplot()

def animate(frame):
    t=frame
    for i in range(201):
     for j in range(101):
        Lab[j,i]=ona_plana(x[i],y[j],t,c,x0)\
                 +ona_esf(x[i],y[j],x0,y1,t,c)\
                     +ona_esf(x[i],y[j],x0,y2,t,c)
        Int[j,i]=intensitat(Lab[j,i])
        Ona[j,i]=Lab[j,i].real
    plt.pcolormesh(x,y,Ona,vmin=-2,vmax=+2)

anim = ani.FuncAnimation(fig, animate, 
                               frames = 100, 
                               blit = False, interval=1)

plt.show()




