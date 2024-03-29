# 电炮大纲

### 目录
- 什么是电炮
- 基础知识
- 电炮分类
- 研究现状
- 安全因素
- 法律风险
- 项目划分

#### 什么是电炮

电磁炮是利用电磁发射技术制成的一种先进**动能**杀伤*武器*。与传统大炮将火药燃气压力作用于弹丸不同，电磁炮是利用电磁系统中**电磁场产生的安培力**来对金属炮弹进行加速，使其达到打击目标所需的动能，与传统的火药推动的大炮，电磁炮可大大提高弹丸的速度和射程。


## 方案选型

磁阻式电磁炮

电容储能

## 11.1

研讨会内容：

1. 磁阻式加速原理
2. 电路构建及特性
3. 测量装置


### 1 磁阻式加速原理

#### 1.1 磁场能量

$$E_m = \frac{1}{2}\int_V \vec{B} \cdot \vec{H} dV= \frac{1}{2} \sum_{i=1}^{n}I_i\Phi_i$$

对于一个磁场，其分布在空间中体积$V$,对空间中每一个点求磁场H和磁场B点乘，最后累加起来便是这个磁场的能量。值得注意的是，磁场B和磁场H并没有强制相同的关系，也许一个磁场中可以H相同他但B不相同。

#### 1.2 磁场中铁磁体受力

根据功能原理$E$为一个系统的总能量

$$dE = -dW = -\vec{F} \cdot d\vec{x}$$

所以能够很容易的推出受力大小

$$F = -\frac{dE}{dx}$$

考虑螺线管中的磁场，首先，根据H的环路定律很容易得出

$$\oint _L \vec{H}\cdot d\vec{x} = \sum I_{in} $$

螺线管中无论如何填充物质，包括顺磁性，逆磁性或是铁磁性的物质（当然，这里讨论的是静磁场），其磁场H的大小是不会发生改变的。假设螺线管密度为$N$,量纲为匝/米，则可以容易得出

$$H = NI$$

随后按照$H$和$B$的关系

$$H = \mu_0\mu_r B$$

对整个磁场进行积分，得出磁场的总能量即可。随后便是喜闻乐见的$\frac{dE}{dx}$环节，轻松优雅的解出磁场力的大小

在这里放出一个简单的结论

$$F = \frac{1}{2}\chi_m H^2 A\mu_0 = \frac{1}{2}\chi_m\mu_0[NI(t)]^2A$$

$\chi_m = \frac{\mu_r-1}{\mu_0}$,物质的磁化率。

$N$是线圈的总匝数

$A$是截面积。

```
值得注意的是，再实际手算的过程中，为了简化，完全会忽略磁漏和螺线管外的磁场。当然，真实情况是：当绕线不太密的时候，有一部分磁场会从导线间的空隙漏出去；同时，螺线管外部有少量的磁场，但是通常是以指数式下降的磁场。因此，以上的讨论就是针对于 无穷长，密绕螺线管中一段有电流的情景。
```

#### 1.3 有限长线圈对铁磁体的加速

由于当弹体一部分在线圈外，由于铁磁体的特性，会有一部分磁漏，导致受力的减小。可以看到，在离线圈中心外一点的地方受力最大。

同时，值得注意的是，从这个例子中可以看出磁阻炮并不需要很高的的$\frac{dI}{dt}$,也可以发现铁磁体只能被拉动，无法被推动。基于此，为了使效率最大，当弹体到达中心时，线圈中电流应当为0。

#### 1.4 更加高级的方法*

一个磁场的总能量如下：

$$W_m(x) = \frac{1}{2}L(x)I(x)^2$$

$$\frac{dW_m}{dx} = \frac{1}{2} L_0(x)I^2$$

对此，建立动力学运动方程

$$m\frac{d^2x}{dt^2} = \frac{1}{2}L_0(x)I^2-\mu mg-\gamma (\frac{dx}{dt})^n$$



### 2 电路构建及特性

#### 2.1 供能方式

现在已经有很多种电源或者电能储能方式，最常见的是市电的交流电，经过整流、稳压输出直流电。但是，电炮中要求的电流相对较大，而对电压没有特别的要求，这导致了通常的电源方案并不合理。现实中常见的电源能够输出电流能力有限。当然，还有方案采用电池，电感，这些方案分别将电能转化为化学能和磁场能，化学能转换效率低，磁场能放电不干脆，因此都不适用。因此，剩下来的方案便是电容储能，将电能存储为电场能，接通的时候能够迅速放出大电流，干脆利落。但现实终究不是完美的，电容储能能量密度极低，体积大，笨重。

电容本身具有特性如下：

$$C = \frac{Q}{V}$$
$I = \frac{dQ}{dt}$据此，一个简单的电容-电阻充电回路中，电流的变化是一阶的（指数函数）。

#### 2.2 加速电路

如前文所提及，线圈在这个情境中用于对线圈加速；前文也提及要电流能够及时的在恰当位置为零。但理想很丰满，现实很骨感，线圈有的特性导致了这一目标实现是又难度的。

线圈具有阻碍电流变化的特性，这颗源自于密绕的线圈，一部分导线流过电流，产生了磁场，在其他匝上感生出了电流，这些电流与本来的电流相叠加。在经过电流变化时，线圈上会感生出一个相反的电压。

$$\varepsilon = -L \frac{dI}{dt} $$

$L$是针对这一线圈的“电感系数”，与线圈的几何形状，导线的特性有关。这里的线圈也可以叫做电感。

会看到现实情境中，当线圈缠绕的太多时，电感系数较大，电流无法快速归零，显然，这是不想要的。因此，在考虑线圈时，需要考虑电感的特性。

更加严重的一件事情是，当电感作为加速期间、电容作为储能器件时，电路中的电流会变为周期性的震荡（二阶微分方程的通解），甚至电流会反向给电容充电！

##### 2.2.1

很常见的，根据前文第1节的驱动力的公式，需要大电流，在这里可以看到放电电路的系统电阻，这来自于充电电容的内阻，线圈的电阻，接触电阻等等，这些共同制约了系统最大电路。

#### 2.3充电电路

![充放电电路](/Charge.png "Magic Gardens")

可以在这个电路图中看到左边的回路是充电电路。在实际充电过程中，开关1先闭合，储能电容开始充电，到达稳态，充电完成之后，断开开关1，闭合开关2，开始放电，大电流涌过发射线圈，产生强磁场，拉动弹体。

在充电电路中，需要考虑电压的选择和充电功率（这直接决定了充电电源的拓扑 形式！）。

#### 2.4 更加细致的考虑这个电路*

为了更加细致地考察放电电路，我们选择对其建立方程。

当然，首先考虑初值：
$$t=0,V_c = V_0,I = 0$$

$V_c$ 是电容两端的电压。$I$定义为总回路中的电流。

根据基尔霍夫定律，很容易得出

$$V_c = V_R + V_i$$

$$V(t) = R_1I(t)+\frac{d[L(x)I(t)]}{dt} = R_1I(t)+L(x)\frac{dI(t)}{dt}+I(t)\frac{dL(x)}{dt}$$

通过简单的变形就能得到如下的微分方程

$$CL(x)\frac{d^2[U(t)]}{dt^2}+C[R_1+\frac{d[L(x)]}{dx}\frac{dx}{dt}]\frac{d[U(t)]}{dt}+U(t)=0$$

$L(x)$是弹丸在$x$位置时，加速线圈的电感总量。


### 3检测方法

**光电门**

*视频法*

*声音法*



