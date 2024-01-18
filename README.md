# Coilgun Design and Manufacture Project

Belonging to WFLA Physics Society

## Learning Map

- Basic coding ability
- General understanding of coilgun
- Differential equation
- Linear algebra: understanding matrix
- Electromagnetic simulation
- Optimization Theory

## For those who cannot read code

### Coding Environment

If you have VPN, please visit site [Colab](https://colab.google/)

If you do not have VPN, please visit [Repl](repl.it) or [Paddle](https://aistudio.baidu.com/index)

These three are online coding platform for python.

If you want to install python environment, pleases go to [VScode](https://code.visualstudio.com/) and [python](https://www.python.org/) to download python and VScode.


### Instruction

Python is strongly recommended in the project.

Please read `Python入门I.ipynb`,`Python入门I.ipynb`and`type_hint.ipynb`.

These two notebook are brief introduction of basic grammar of Python.Thanks to **Computerization** for providing instruction of python.

## For those who can read code

You guys may play an important role in this part of design.

The core of this design is to simulate electromagnetic environment and implementing optimization.

Some opensource python library on Github, including [FDTD](https://github.com/flaport/fdtd), [EMpy](https://github.com/lbolla/EMpy), are friendly for users.

Besides, it is necessary to learn some numerical solutions of differential equation, such as Runge-Kuta method(RK-4) is the most classic method and forward/backward finite difference method. Some python libraries have already had solvers. However, it is a wise choice to learn a little bit of linear algebra for better understanding. 


## Static Magnetic Field Simulation

### Why Static Magnetic Field Simulation?

In this simulation, a great assumption is made that the behavior of the system is not effected by the velocity of projectile. Therefore, a static magnetic field simulation can be a reasonable choice. It is essential to realize the limitation of this design method.

### Geometry model

This simulation mainly focuses on interaction between one stage of solenoid and the projectile.

![Alt text](geometry.png)

### Physics Principle and Numerical Method

This section aims to discuss numerical method in simulating static magnetic field. The basic principle is Biot–Savart law. $\mu_0 = 4\pi \times 10^{-7}N\cdot A^{-2}$ is the vacuum permeability. $I$ is the current carried in the wire. $d\vec{l}$ is differential length element vector. $\vec{e}_r$ is the unit vector pointing from the position of  $d\vec{l}$ to the given point.

$$ d\vec{B} = \frac{\mu_0}{4\pi}\cdot\frac{Id\vec{l}\times \vec{e_r}}{\left | \vec{r}  \right | ^2}  =\frac{\mu_0}{4\pi}\cdot\frac{Id\vec{l}\times \vec{r}}{\left | \vec{r}  \right | ^3} $$

This law applies to static magnetic field, which means that the current in the wire changes slowly or does not change over time. Thus, by integration, the magnetic flux density at certain point, known as magnetic field strength in IB, is:

$$\vec{B} = \int_C \frac{\mu_0}{4\pi}\cdot\frac{Id\vec{l}\times \vec{r}}{\left | \vec{r}  \right | ^3}$$

In this case, due to the shape of wire, solenoid whose radius is a constant, 2 parameters is required to describe the position of $d\vec{l}$. The coordination is $(x,rsin\theta,rcos\theta)$. Thus, the overall integration equation is shown below. The given point is $(x_1,y_1,z_1)$. $L$ and $R$ is the left bound of solenoid and $R$ is the right bound of solenoid.

$$\vec{B}_{x_1y_1z_1}=  \mu_r \int _L ^R \int_0 ^{2\pi} \frac{\mu_0}{4\pi}\cdot\frac{Jdx\cdot rd\theta \begin{pmatrix}
 0\\-cos\theta
 \\sin \theta
\end{pmatrix}\times \begin{pmatrix}
 x_1-x\\y_1-rsin\theta
 \\z_1 -rcos\theta
\end{pmatrix}}{\left |\begin{pmatrix}
 x_1-x\\y_1-rsin\theta
 \\z_1 -rcos\theta

\end{pmatrix}\right |^3}  $$

This integration computation method has been implemented into the function `field3CalcDMesh` in `solver.py`.

`fieldCalc3DMesh` has nine inputs: `xrange,yrange,zrange` require tuple-like inputs to define the computing area.`Nx，Ny,Nz` define the grid number on each side. These parameters directly determine the precision of simulation of this field. `x,r,length` are parameters to determine the position, length and radius of projectile.

This function would return two fields: B and H. two fields can work with given `xrange,yrange,zrange` to map the distribution of magnetude of field to the real model instead of index.

### Energy Stored in Magnetic Field

According to the previous section, the distribution of B field and H field can be obtained from solver. Next task is to simulate the energy stored in the magnetic field. Strictly speaking, the official name of B is magnetic flux density and the magnetic field strength is H. The energy is derived from the equation below.

$$E = \int_V \vec{B} \cdot \vec{H} dV $$

To discrete the whole integration calculation, the calculating area is cutted into large amounts of small volume to act as $dV$. Each small volume is considered to have a specific B value and H value. Product these three things together and add all values up. Thus, the total energy stored in this magnetic field energy.

In the simulation, this process is achieved by `energySolver1` function from `solver.py`. 

The input is similar to the`fieldCalc3DMesh`. `xrange,yrange,zrange` require tuple-like inputs to define the computing area.`Nx，Ny,Nz` define the grid number on each side. These parameters directly determine the precision of simulation of this field.

However, it is recommended to refine the mesh by the function `refineField` to linear interpolation the value and increase the accuracy of the whole calculation process.

The energy of magnetic field can be 

**Inductance of Coil**

This feature of the Coil may be discussed in detail in the part of circuit simulation. However, this value is closely relevant to the energy stored in the magnetic field.

According to the formula:

$$E = \frac{1}{2}LI^2$$

When the energy and current is known, it is easy to deduce the inductance of the system of coil and projectile. Apparently, under the fixed condition, the inductance is only relevant to the position of projectile.

### Post Processing

This section is used to process data and visualize the computating result. To process data, the linear interpolation is used to refine the grid so that the change of magnitube of strength of field can be smooth. The linear interpolation and visualization functions have been integrated together in `fieldVisual` function from `postProcess.py`. The following two pictures are examples of linear interpolation.

In python, lots of reliable and robust visualization libraries are available such as `matplotlib.pyplot`,`seaborn` etc. In this case, `matplotlib.pyplot` is used to visualize the field.

![linear interpolation](./src/linearVisual.png)

![Alt text](./src/preciseSimulation.png)

### Evaluation

Even though this computation model seems fitting the current requirement pretty well, two significant assumption are ignored.

Firstly, in this simulation, a great assumption is made that the behavior of the system is not effected by the velocity of projectile, challenging the reliability of simulation.

Secondly, the integration model assumes that the solenoid is tightly wounded and there is not 'magnetic leak'. This enables the model to neglect the radius of wire and layer number due to geometry restriction.1

## Circuit simulation

This part of simulation is focusing on the circuit behavior in the coigun, including change of voltage over capacitors, current and performance of MOS/IGBT.

### Estimate Resistance

In the big current situation, the resistance of wire, coil and capacity cannot be ignored. The resistance of wire and coil is easy to calculate by the formula.

$$R = \rho \frac{L}{\pi r^2}$$

The resistance of capacity, from inner conductor, can be estimated by the parameter ESR, equivalent series resistance.Thus, resistance in the circuit can be calculated.

### Estimate Inductance

This method has been partially discussed in previous. This section mainly introduce the impact of inductance over the whole circuit.

$$\varepsilon = -L\frac{dI}{dt}$$

When the current changes, the coil would generate a negative EMF to hinder the change of current. This equation can be directly applied into Kirchhoff Circuit Laws.

### Physical Principal and Equation

The governing equation in this simulation is the Kirchoff Circuit Law. The sum of potential change in a loop is zero. This Law implies the conservation of energy.

$$\Sigma_C U = 0$$

More specifically, in this model, the differential equation is:

$$\frac{Q}{C}-L(x)\frac{d^2Q}{dt^2}+R\frac{dQ}{dt} = 0$$

$L(x)$ is derived from the simulation result of previous part.

### Numerical Method and API

The solution of differential equation can use several method. The easiet way is theoretical solution, but this method only works well with the constant $L(x)$.

Runge-Kuta method is a robust numerical method to solve the differential method. The formula is:

$$X'=f(X,t)$$
$$k_1 = f(X_k,t_k)$$
$$k_2 = f(X_k+0.5\Delta t\cdot k_1,t_k+0.5\Delta t)$$
$$k_3 = f(X_k+0.5\Delta t\cdot k_2,t_k+0.5\Delta t)$$
$$k_4 = f(X_k+\Delta t \cdot k_3,t_k+\Delta t)$$

$$X_{k+1} = X_k+\frac{\Delta t}{6}(k_1+2k_2+2k_3+k_4)$$

This function has been implemented by function `FDTDSolver` from `solver.py`. This solver requires to input initial condition, time step length, and loop number.

## Coupled solver

🤡

### Differential Equation

### Solver API

## Optimization Theory

Consider a function

$$f(\mathbf{x})=r$$

$\mathbf{x}$ is a n-dimension vector and the output is $r \in \mathbb{R}$. To apply this scenario into coilgun design project, we can simply assume some specific parameters and consider other related input. $r$ can be the efficiency of the coilgun.

Generally speaking, it is wise to design the function to be convex function(i.e. $\forall \mathbf{x},\exists \mathbf{x_0} \Rightarrow  f(\mathbf{x_0})\ge X$, function has lower bound). 



## Coding

From the perspective of python, many libraries have been available and useful in simulation. `scipy`and`numpy` are two strong liraries for simulation by array, grid and optimization algorithm. Besides, it is recommended to use `cupy` to gain more computation resources.

## NOTES

1. Currently, the solver still does not support parallel computation by dispatch the computation field, or the computation field has to be divided manually. Data from different field cannot be stacked together properly.

2. The static magnetic field solver does not suppot geometry of solenoid. Further discretization method and integration method is necessary.

3. The solver `FDTDSolver` has not been tested.

4. The coupled solver currently cannot be developed due to limitation of static magnetic solver.

5. The structure of `fieldCalc3DMesh` solver shoule be adjusted. 
