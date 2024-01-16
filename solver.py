import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
import time

'''
The geometry of this simulation case:
1 simulation field: 
    Y-axis: -3 to 3cm
    X-axis: -8 to 12cm
2 solenoid:
    length: +- 5cm
    radius 1cm
    central line: y = 0
3 steel
    radius 0.9cm
    length 3cm
    co-axis with solenoid
'''
'''
electromagnetic field parameter
current: 5 A/mm
mu0 4pie-7
mur 1000
'''

# constant
mu0 = 4*np.pi*10**(-7)
mur = 1000

#geometry parameter
radiusSolenoid = 10e-3
lengthSolenoid = 50e-3
currentDensity = 5e3
fieldLeft = -80e-3
fieldRight = 120e-3
fieldUp = 30e-3
fieldDown = -30e-3
fieldThick = 30e-3

#Mesh Parameter
# current algorithm does not use it 
Nxs = 800
dx = lengthSolenoid*2/Nxs
Ntheta = 150
dtheta = (2*np.pi)/Ntheta

# the grid for the whole calculation field
Nx = 40
Ny = 20
Nz = 5
##
'''
def db(detectPosition,theta, x):
    #Generate dl
    dl = radiusSolenoid*dtheta*np.array([0,np.sin(theta+np.pi/2),np.cos(theta+np.pi/2)])
    position = np.array([x,radiusSolenoid*np.sin(theta),radiusSolenoid*np.cos(theta)])
    dB = mu0/(4*np.pi)*currentDensity*dx*np.cross(dl,detectPosition-position)/(np.linalg.norm(detectPosition-position)**3)
    return dB

def Bsolver(detectPosition):
    B = np.array([0,0,0])
    for x in np.linspace(-lengthSolenoid,lengthSolenoid,Nxs):
        for theta in np.linspace(0,2*np.pi,Ntheta):
            B = B + db(detectPosition,theta,x)

    return B

def fieldB(Pmin=None,Pmax=None):

    u = np.zeros((Nx+1,Ny+1))
    for x in np.linspace(fieldLeft,fieldRight,Nx+1):
        for y in np.linspace(fieldDown,fieldUp,Ny+1):
            B = Bsolver(np.array([x,y,0]))
            nx = (x-fieldLeft)/((fieldRight-fieldLeft)/Nx)
            ny = (y-fieldDown)/((fieldUp-fieldDown)/Ny)
            if Pmin != None:
                if np.all(Pmin < np.array([x,y,0])) and np.all(np.array([x,y,0])<=Pmax):
                    B = mur*B
            u[int(nx),int(ny)] = np.linalg.norm(B)
            print((x,y))
    return u


#Bfield = fieldB()
'''




def func(theta):
    d = mu0*(currentDensity*radiusSolenoid*np.array([-Z*np.cos(theta)-Y*np.sin(theta)+radiusSolenoid,
                                                              np.sin(theta)*(X-x1),
                                                              np.cos(theta)*(X-x1)]))/(4*np.pi)
    l = np.linalg.norm(np.array([X-x1,Y-radiusSolenoid*np.sin(theta),Z-radiusSolenoid*np.cos(theta)]))**3
    ans = d/l
    return ans

def func1(x):
    global x1
    x1 = x
    #print(x1)
    return integrate.quad_vec(func,0,2*np.pi)[0]


def integ1(x,y,z):
    global X,Y,Z 
    X,Y,Z = x,y,z
    return np.linalg.norm(integrate.quad_vec(func1,-lengthSolenoid,lengthSolenoid)[0])

def fieldCalc(Pmin = None,Pmax = None):
    u = np.zeros((Nx+1,Ny+1))
    i = 0
    j = 0
    xc = np.linspace(fieldLeft,fieldRight,Nx+1)
    yc = np.linspace(fieldDown,fieldUp,Ny+1)
    for i in np.arange(Nx+1):
        for j in np.arange(Ny+1):
            B = integ1(xc[i],yc[j],0)
            position = np.array([xc[i],yc[j],0])
            if Pmin != None:
                if np.all(Pmin<position) and np.all(position<Pmax):
                    B = B*mur
            u[int(i),int(j)] = B
            print((i,j))
    return u

x1,X,Y,Z = 0,0,0,0 #initialize crucial variables
start = time.time()
Bfield = fieldCalc()
end = time.time()
print(end-start)

plt.imshow(Bfield, cmap='viridis', interpolation='nearest')
plt.colorbar()
plt.show()
'''

Calculation example for this solver

print(integ1(0.5,0,0,-lengthSolenoid,lengthSolenoid))
start = time.time()
position = np.linspace(fieldLeft,fieldRight,100)
B = np.array([])
for j in position:
    B = np.append(B,integ1(j,0,0,-lengthSolenoid,lengthSolenoid))
end = time.time()

B_theo = np.array([])
for x in position:
  b = mu0*250*20/2*((x+lengthSolenoid)/((x+lengthSolenoid)**2+radiusSolenoid**2)**0.5-(x-lengthSolenoid)/((x-lengthSolenoid)**2+radiusSolenoid**2)**0.5)
  B_theo = np.append(B_theo, b)

print(end-start)
plt.plot(position,B_theo)
plt.plot(position,B)
plt.show()

#print(integ(0,0,0,-lengthSolenoid,lengthSolenoid))
'''