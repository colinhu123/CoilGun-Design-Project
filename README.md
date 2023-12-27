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

## Optimization Theory

Consider a function

$$f(\mathbf{x})=r$$

$\mathbf{x}$ is a n-dimension vector and the output is $r \in \mathbb{R}$. To apply this scenario into coilgun design project, we can simply assume some specific parameters and consider other related input. $r$ can be the efficiency of the coilgun.Generally speaking, it is wise to design the function to be convex function(i.e. $\forall \mathbf{x},\exists \mathbf{x_0} \Rightarrow  f(\mathbf{x_0})\ge X$, function has lower bound). There are some python libraries supporting different optimization method.

## Coding

From the perspective of python, many libraries have been available and useful in simulation. `scipy`and`numpy` are two strong liraries for simulation by array, grid and optimization algorithm. Besides, it is recommended to use `cupy` to gain more computation resources.
