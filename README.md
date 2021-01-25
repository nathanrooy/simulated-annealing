# simple simulated annealing
[![gh-actions-ci](https://img.shields.io/github/workflow/status/nathanrooy/simulated-annealing/ci?style=flat-square)](https://github.com/nathanrooy/simulated-annealing/actions?query=workflow%3Aci)
[![GitHub license](https://img.shields.io/github/license/nathanrooy/simulated-annealing?style=flat-square)](https://github.com/nathanrooy/simulated-annealing/blob/master/LICENSE)
[![codecov](https://img.shields.io/codecov/c/github/nathanrooy/simulated-annealing.svg?style=flat-square)](https://codecov.io/gh/nathanrooy/simulated-annealing)


This repo contains a very simple implementation of <a target="_blank" href="https://en.wikipedia.org/wiki/Simulated_annealing">simulated annealing</a> based on the tutorial available [<a target="_blank" href="https://nathanrooy.github.io/posts/2020-05-14/simulated-annealing-with-python/">here</a>].

## Installation
You can either download/clone this repo or pip install it as follows:
```sh
pip install git+https://github.com/nathanrooy/simulated-annealing
```

## Usage: continuous optimization
There are two modes of optimization currently available with this implementation of simulated annealing: `continuous` and `combinatorial`. We'll cover the continuous case first but prior to starting we'll need to specify a cost function. For this, we'll install the <a target="_blank" href="https://github.com/nathanrooy/landscapes">Landscapes</a> optimization test function library with either of the following commands:
```sh
pip install landscapes
```
or 
```sh
pip install git+https://github.com/nathanrooy/landscapes
```
Now In a Python terminal, import the necessary dependencies. We'll use the `sphere` function from Landscapes to start off with since it's smooth and convex.
```python
>>> from simulated_annealing import sa
>>> from landscapes.single_objective import sphere
```
Next, let's specify the initial values and optimize. The value `x0` in this case is simply a random starting point with three degrees of freedom.
```python
>>> x0 = [1, 2, 3]
>>> opt = sa.minimize(sphere, x0, opt_mode='continuous', step_max=1000, t_max=1, t_min=0)
```
The results can be viewed with the following:
```python
>>> opt.results()
```
Which will yield something fairly close to this:
```python
+------------------------ RESULTS -------------------------+

      opt.mode: continuous
cooling sched.: linear additive cooling


  initial temp: 1
    final temp: 0.001000
     max steps: 1000
    final step: 1000

  final energy: 0.007882

+-------------------------- END ---------------------------+
```
For additional results, use `opt.best_state` to view the optimal parameters:
```python
>>> opt.best_state
[0.006638773548345078, -0.08591710990585566, -0.02136864187181653]
```
As well as `opt.best_energy` to display the cost function value with these parameters:
```python
>>> opt.best_energy
0.007882441944247037
```
## Usage: combinatorial optimization
For combinatorial problems such as the traveling salesman problem, usage is just as easy. First, let's define a method for calculating the distance between our points. In this case, Euclidean distance is used, but it can be anything...
```python
def calc_euclidean(p1, p2):    
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5
```
Next, let's prepare some points. In the intrest of simplicity, we'll just generate 6 points on the perimiter of the unit circle.
```python
from math import cos
from math import sin
from math import pi
n_pts = 6
d_theta = (2 * pi) / n_pts
theta = [d_theta * i for i in range(0, n_pts)]
x0 = [(cos(r), sin(r)) for r in theta]
```
Now, prepeare the cost function.
```python
from landscapes.single_objective import tsp
cost_func = tsp(calc_euclidean, close_loop=True).dist
```
Because we generated our perimiter points in rotational order, `x0` is already the optimal solution. We can check this with:
```python
>>> cost_func(x0)
>>> 6.0
```
Just under two pi...

Now let's optimize this while remembering to shuffle the points prior to running.
```python
from random import shuffle
shuffle(x0)
opt = sa.minimize(cost_func, x0, opt_mode='combinatorial', step_max=1000, t_max=1, t_min=0)
```
The results should look something like the following:
```python
>>> opt.results()
+------------------------ RESULTS -------------------------+

      opt.mode: combinatorial
cooling sched.: linear additive cooling


  initial temp: 1
    final temp: 0.001000
     max steps: 1000
    final step: 1000

  final energy: 6.000000

+-------------------------- END ---------------------------+
```

## Cooling Schedules
There are several cooling schedules available with this implementation. They are as follows: `linear`, `exponential`, `logarithmic`, and `quadratic`. They can be specified as using the `cooling_schedule=` input as follows:
</br>
</br>
`opt = sa.minimize(cost_func, x0, opt_mode='combinatorial', cooling_schedule='linear', ...)`

