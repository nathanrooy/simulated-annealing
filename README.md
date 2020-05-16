# simple simulated annealing
This repo contains a very simple implementation of <a target="_blank" href="https://en.wikipedia.org/wiki/Simulated_annealing">simulated annealing</a> based on the tutorial available [here].

## Installation
You can either download/clone this repo or pip install it as follows.
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
For combinatorial problems such as the traveling salesman problem, usage is just as easy. This time however, we'll just code out an example tsp cost function. First we'll calculate distances using a Euclidean approach.
```python
def calc_euclidean(p1, p2):    
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5
```
Next, the actual tsp class can be created:
```python
class tsp():
    def __init__(self, dist_func, close_loop=True):
        self.dist_func = dist_func
        self.close_loop = close_loop
    
    def dist(self, xy):
        # sequentially calculate distance between all tsp nodes
        dist = 0
        for i in range(len(xy)-1): 
            dist += self.dist_func(xy[i+1], xy[i])

        # close the tsp loop by calculating the distance 
        # between the first and last points
        if self.close_loop:
            dist += self.dist_func(xy[0], xy[-1])
        
        return dist
```
Initialize the tsp cost function
```python
tsp_dist = tsp(dist_func=calc_euclidean, close_loop=True).dist
```




## Cooling Schedules
There are several cooling schedules available with this implementation. They are as follows:
- linear
- exponential
- logarithmic
- quadratic

## Examples

