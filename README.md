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

These two notebook are brief introduction of basic grammar of Python.


## For those who can read code

You guys may play an important role in this part of design.

The core of this design is to simulate electromagnetic environment and implementing optimization.

Some opensource python library on Github, including [FDTD](https://github.com/flaport/fdtd), [EMpy](https://github.com/lbolla/EMpy), are friendly for users.

Besides, it is necessary to learn some numerical solutions of differential equation, such as Runge-Kuta method(RK-4) is the most classic method and forward/backward finite difference method. Some python libraries have already had solvers. However, it is a wise choice to learn a little bit of linear algebra for better understanding. 

## Static Magnetic Field Simulation

### Geometry model

This simulation mainly focuses on interaction between one stage of solenoid and the projectile. The specific geometry parameters and relative magnetic permeability are defined in the file`solver`.

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

### Post Processing

This section is used to process data and visualize the computating result. To process data, the linear interpolation is used to refine the grid so that the change of magnitube of strength of field can be smooth. The linear interpolation and visualization functions have been integrated together in `fieldVisual` function from `postProcess.py`. The following two pictures are examples of linear interpolation.

In python, lots of reliable and robust visualization libraries are available such as `matplotlib.pyplot`,`seaborn` etc. In this case, `matplotlib.pyplot` is used to visualize the field.

![linear interpolation](./src/linearVisual.png)

![Alt text](./src/preciseSimulation.png)

## Optimization Theory

Consider a function

$$f(\mathbf{x})=r$$

$\mathbf{x}$ is a n-dimension vector and the output is $r \in \mathbb{R}$. To apply this scenario into coilgun design project, we can simply assume some specific parameters and consider other related input. $r$ can be the efficiency of the coilgun.Generally speaking, it is wise to design the function to be convex function(i.e. $\forall \mathbf{x},\exists \mathbf{x_0} \Rightarrow  f(\mathbf{x_0})\ge X$, function has lower bound). There are some python libraries supporting different optimization method.

## Coding

From the perspective of python, many libraries have been available and useful in simulation. `scipy`and`numpy` are two strong liraries for simulation by array, grid and optimization algorithm. Besides, it is recommended to use `cupy` to gain more computation resources.

## NOTES

Currently, the solver still does not support parallel computation by dispatch the computation field, or the computation field has to be divided manually. Data from different field cannot be stacked together properly.
