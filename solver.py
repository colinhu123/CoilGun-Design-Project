import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
import time
from scipy.interpolate import griddata

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
rho_copper = 1.7e-8


#geometry parameter of field
fieldLeft = -80e-3
fieldRight = 120e-3
fieldUp = 30e-3
fieldDown = -30e-3
fieldThick = 30e-3

#geometry parameters of solenoid and components in circuit
radiusSolenoid = 10e-3
lengthSolenoid = 50e-3
currentDensity = 5e3

ESR = 1.1 #ohm
radiusWire = 3e-3 #mm
C = 1000e-6 #F


#Mesh Parameter
# current algorithm does not use it 
Nxs = 800
dx = lengthSolenoid*2/Nxs
Ntheta = 150
dtheta = (2*np.pi)/Ntheta

# the grid for the whole calculation field
Nx = 40
Ny = 10
Nz = 2
##
'''

This part of code is abandoned due to its poor performance. 
However, its straightforward style of integration makes it easy to read.

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
    d = (currentDensity*radiusSolenoid*np.array([-Z*np.cos(theta)-Y*np.sin(theta)+radiusSolenoid,
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

def fieldCalc(x = None,r = None,length = None):
    u = np.zeros((Nx+1,Ny+1))
    v = np.zeros((Nx+1,Ny+1))
    i,j = 0,0
    xc = np.linspace(fieldLeft,fieldRight,Nx+1)
    yc = np.linspace(fieldDown,fieldUp,Ny+1)
    for i in np.arange(Nx+1):
        for j in np.arange(Ny+1):
            H = integ1(xc[i],yc[j],0)
            position = np.array([xc[i],yc[j],0])
            if x != None:
                if position[0]>x and position[0]<x+length:
                    if np.linalg.norm(np.array([yc[j],0]))<r:

                        B = H*mur*mu0
                    else:
                        B = H*mu0
                else:
                    B = H*mu0
            else:
                B = H*mu0
            u[int(i),int(j)] = B
            v[int(i),int(j)] = H
    return u,v

def fieldCalc3D(x = None,r = None,length = None):
    u = np.zeros((Nx+1,Ny+1,Nz+1))
    v = np.zeros((Nx+1,Ny+1,Nz+1))
    i,j,k = 0,0,0
    xc = np.linspace(fieldLeft,fieldRight,Nx+1)
    yc = np.linspace(0,fieldUp,Ny+1)
    zc = np.linspace(0,fieldThick,Nz+1)
    for i in np.arange(Nx+1):
        for j in np.arange(Ny+1):
            for k in np.arange(Nz+1):
                H = integ1(xc[i],yc[j],zc[k])
                position = np.array([xc[i],yc[j],zc[k]])
                if x != None:
                    if position[0]>x and position[0]<x+length:
                        if np.linalg.norm(np.array([yc[j],zc[k]]))<r:
                            B = H*mur*mu0
                        else:
                            B = H*mu0
                    else:
                        B = H*mu0
                else:
                    B = H*mu0
                u[int(i),int(j),int(k)] = B
                v[int(i),int(j),int(k)] = H
    return u,v

def fieldCalc3DMesh(xrange,yrange,zrange,Nx,Ny,Nz,x = None,r = None,length = None):
    u = np.zeros((Nx+1,Ny+1,Nz+1))
    v = np.zeros((Nx+1,Ny+1,Nz+1))
    i,j,k = 0,0,0
    fieldLeft = xrange[0]
    fieldRight = xrange[1]
    fieldDown = yrange[0]
    fieldUp = yrange[1]
    fieldFront = zrange[1]
    fieldBack = zrange[0]
    xc = np.linspace(fieldLeft,fieldRight,Nx+1)
    yc = np.linspace(fieldDown,fieldUp,Ny+1)
    zc = np.linspace(fieldBack,fieldFront,Nz+1)
    for i in np.arange(Nx+1):
        for j in np.arange(Ny+1):
            for k in np.arange(Nz+1):
                H = integ1(xc[i],yc[j],zc[k])
                position = np.array([xc[i],yc[j],zc[k]])
                if x != None:
                    if position[0]>x and position[0]<x+length:
                        if np.linalg.norm(np.array([yc[j],zc[k]]))<r:
                            B = H*mur*mu0
                        else:
                            B = H*mu0
                    else:
                        B = H*mu0
                else:
                    B = H*mu0
                u[int(i),int(j),int(k)] = B
                v[int(i),int(j),int(k)] = H
                print((i,j,k))
    return u,v


x1,X,Y,Z = 0,0,0,0 #initialize crucial variable

#fieldCalc3DMesh((50e-3,100e-3),(0,40e-3),(0,25e-3),10,4,4)
# This line is the test of fieldCalc3DMesh



def energySolver(Bfield,Hfield,xrange,yrange,zrange,Nx,Ny,Nz):
    E = 0
    if np.shape(Bfield) == np.shape(Hfield):
        Vtotal = (xrange[1]-xrange[0])*(yrange[1]-yrange[0])*(zrange[1]-zrange[0])
        dV = Vtotal/(Nx*Ny*Nz)
        for i in range(1,Nx+1):
            for j in range(1,Ny+1):
                for k in range(1,Nz+1):
                    dE = Bfield[i,j,k]*Hfield[i,j,k]*dV
                    E += dE
        i,j,k = 0,0,0
        for i in [0,Nx+1]:
            for j in [0,Ny+1]:
                for k in [0,Nz+1]:
                    dE = Bfield[i,j,k]*Hfield[i,j,k]*dV*0.5
                    E += dE
        return E
    else:
        raise ValueError("The size of B and H field is not consistent.")
    
def refineField(field,refineCoef):#这个函数慎用，我也没搞清楚到底是怎么工作的，且未经过完整测试
    shape = np.shape(field)
    nx = shape[0]
    ny = shape[1]
    nz = shape[2]
    x = np.linspace(0, nx-1, nx)  # Assuming x coordinates from 0 to 40
    y = np.linspace(0, ny-1, ny)  # Assuming y coordinates from 0 to 15
    z = np.linspace(0, nz-1, nz)
    X, Y,Z = np.meshgrid(x, y,z)
    x_new = np.linspace(0, nx-1, refineCoef)
    y_new = np.linspace(0, ny-1, refineCoef)
    z_new = np.linspace(0, nz-1, refineCoef)
    X_new, Y_new, Z_new = np.meshgrid(x_new, y_new, z_new)
    #field = np.transpose(f)
    # Perform linear interpolation using griddata
    fieB_interp = griddata((X.flatten(), Y.flatten(), Z.flatten()), field.flatten(), (X_new, Y_new,Z_new), method='linear')
    return fieB_interp

def energySolverv1(Bfield,Hfield,xrange,yrange,zrange,Nx,Ny,Nz):
    E = 0
    if np.shape(Bfield) == np.shape(Hfield):
        Vtotal = (xrange[1]-xrange[0])*(yrange[1]-yrange[0])*(zrange[1]-zrange[0])
        dV = Vtotal/(Nx*Ny*Nz)
        E_matrix = Bfield*Hfield*dV
        E = np.sum(E_matrix)
        return E
    else:
        raise ValueError("The size of B and H field is not consistent.")
    

## solver and relative function of circuit simulation.
    

def resistance(n,r):
    R = rho_copper*n*2*np.pi*radiusSolenoid/(np.pi*r**2)
    R += ESR*1.3 #1.3 is an experience coefficient
    return R

def L(x):
    return 1e-6

def FDTDSolver(initialState,dt,func,Iternum):
    '''
    initialState: the valules of key state variable for this system
    dt: the time step
    func: function. Input: state variable array, output change rate
    '''
    tl = np.array([])
    Xl = np.array([])
    X =initialState

    for i in range(Iternum):
        tl = np.append(tl,i*dt)
        Xl = np.append(Xl,X)
        k1 = func(X)
        k2  = func(X+0.5*dt*k1)
        k3 = func(X+0.5*dt*k2)
        k4 = func(X+dt)
        X = X+dt*(k1+2*k2+2*k3+k4)/6

    return tl,Xl



'''
# Test for the
start = time.time()
Bfield,Hfield = fieldCalc3D(60e-3,8e-3,40e-3)
end = time.time()
print(end-start)

sli = Bfield[:,:,0]

plt.imshow(np.log10(sli), cmap='viridis', interpolation='nearest')
plt.colorbar()
plt.show()


Calculation example for this solver
This example described the situation that a solenoid with surface current density
5000A/m. the output is the distribution of magnitude of magnetic flux density
along x-aixs. The theoretical solution for this function has been displayed in
the for-loop after `B_theo = np.array([])`

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
