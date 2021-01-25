import unittest
from simulated_annealing import sa


def sphere(x):
    return sum([v**2 for v in x])


class test_integration(unittest.TestCase):

    def test_everything(self):
        x0 = [1, 2, 3]
        opt = sa.minimize(sphere, x0, opt_mode='continuous', step_max=1000, t_max=1, t_min=0)
        self.assertEqual(len(x0), len(opt.best_state))
        self.assertLess(opt.best_energy, sphere(x0))
