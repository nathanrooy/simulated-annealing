#------------------------------------------------------------------------------+
#
#   Nathan A. Rooy
#   Simple Simulated Annealing
#   2019 - DEC
#
#------------------------------------------------------------------------------+

#--- IMPORT DEPENDENCIES ------------------------------------------------------+

from random import randint
from random import random
from math import exp
from math import log

#--- MAIN ---------------------------------------------------------------------+

class minimize():
    '''Simple Simulated Annealing
    '''

    def __init__(self, func, x0, opt_mode, cooling_schedule='linear', step_max=1000, t_min=0, t_max=100, bounds=[], alpha=None, damping=1):

        # checks
        assert opt_mode in ['combinatorial','continuous'], 'opt_mode must be either "combinatorial" or "continuous"'
        assert cooling_schedule in ['linear','exponential','logarithmic', 'quadratic'], 'cooling_schedule must be either "linear", "exponential", "logarithmic", or "quadratic"'


        # initialize starting conditions
        self.t = t_max
        self.t_max = t_max
        self.t_min = t_min
        self.step_max = step_max
        self.opt_mode = opt_mode
        self.hist = []
        self.cooling_schedule = cooling_schedule

        self.cost_func = func
        self.x0 = x0
        self.bounds = bounds[:]
        self.damping = damping
        self.current_state = self.x0
        self.current_energy = func(self.x0)
        self.best_state = self.current_state
        self.best_energy = self.current_energy


        # initialize optimization scheme
        if self.opt_mode == 'combinatorial': self.get_neighbor = self.move_combinatorial
        if self.opt_mode == 'continuous': self.get_neighbor = self.move_continuous


        # initialize cooling schedule
        if self.cooling_schedule == 'linear':
            if alpha != None:
                self.update_t = self.cooling_linear_m
                self.cooling_schedule = 'linear multiplicative cooling'
                self.alpha = alpha

            if alpha == None:
                self.update_t = self.cooling_linear_a
                self.cooling_schedule = 'linear additive cooling'

        if self.cooling_schedule == 'quadratic':
            if alpha != None:
                self.update_t = self.cooling_quadratic_m
                self.cooling_schedule = 'quadratic multiplicative cooling'
                self.alpha = alpha

            if alpha == None:
                self.update_t = self.cooling_quadratic_a
                self.cooling_schedule = 'quadratic additive cooling'

        if self.cooling_schedule == 'exponential':
            if alpha == None: self.alpha =  0.8
            else: self.alpha = alpha
            self.update_t = self.cooling_exponential

        if self.cooling_schedule == 'logarithmic':
            if alpha == None: self.alpha =  0.8
            else: self.alpha = alpha
            self.update_t = self.cooling_logarithmic


        # begin optimizing
        self.step, self.accept = 1, 0
        while self.step < self.step_max and self.t >= self.t_min and self.t>0:

            # get neighbor
            proposed_neighbor = self.get_neighbor()

            # check energy level of neighbor
            E_n = self.cost_func(proposed_neighbor)
            dE = E_n - self.current_energy

            # determine if we should accept the current neighbor
            if random() < self.safe_exp(-dE / self.t):
                self.current_energy = E_n
                self.current_state = proposed_neighbor[:]
                self.accept += 1

            # check if the current neighbor is best solution so far
            if E_n < self.best_energy:
                self.best_energy = E_n
                self.best_state = proposed_neighbor[:]

            # persist some info for later
            self.hist.append([
                self.step,
                self.t,
                self.current_energy,
                self.best_energy])

            # update some stuff
            self.t = self.update_t(self.step)
            self.step += 1

        # generate some final stats
        self.acceptance_rate = self.accept / self.step


    def move_continuous(self):
        # preturb current state by a random amount
        neighbor = [item + ((random() - 0.5) * self.damping) for item in self.current_state]

        # clip to upper and lower bounds
        if self.bounds:
            for i in range(len(neighbor)):
                x_min, x_max = self.bounds[i]
                neighbor[i] = min(max(neighbor[i], x_min), x_max)

        return neighbor


    def move_combinatorial(self):
        '''Swaps two random nodes along path
        Not the most efficient, but it does the job...
        '''
        p0 = randint(0, len(self.current_state)-1)
        p1 = randint(0, len(self.current_state)-1)

        neighbor = self.current_state[:]
        neighbor[p0], neighbor[p1] = neighbor[p1], neighbor[p0]

        return neighbor


    def results(self):
        print('+------------------------ RESULTS -------------------------+\n')
        print(f'      opt.mode: {self.opt_mode}')
        print(f'cooling sched.: {self.cooling_schedule}')
        if self.damping != 1: print(f'       damping: {self.damping}\n')
        else: print('\n')

        print(f'  initial temp: {self.t_max}')
        print(f'    final temp: {self.t:0.6f}')
        print(f'     max steps: {self.step_max}')
        print(f'    final step: {self.step}\n')

        print(f'  final energy: {self.best_energy:0.6f}\n')
        print('+-------------------------- END ---------------------------+')

    # linear multiplicative cooling
    def cooling_linear_m(self, step):
        return self.t_max /  (1 + self.alpha * step)

    # linear additive cooling
    def cooling_linear_a(self, step):
        return self.t_min + (self.t_max - self.t_min) * ((self.step_max - step)/self.step_max)

    # quadratic multiplicative cooling
    def cooling_quadratic_m(self, step):
        return self.t_min / (1 + self.alpha * step**2)

    # quadratic additive cooling
    def cooling_quadratic_a(self, step):
        return self.t_min + (self.t_max - self.t_min) * ((self.step_max - step)/self.step_max)**2

    # exponential multiplicative cooling
    def cooling_exponential_m(self, step):
        return self.t_max * self.alpha**step

    # logarithmical multiplicative cooling
    def cooling_logarithmic_m(self, step):
        return self.t_max / (self.alpha * log(step + 1))


    def safe_exp(self, x):
        try: return exp(x)
        except: return 0

#--- END ----------------------------------------------------------------------+
