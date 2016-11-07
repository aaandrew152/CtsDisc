__author__ = 'elubin'
from games.Cwol import CWOL
#from cwol_onlyl import CWOLOnlyL
from wrapper import GameDynamicsWrapper, VariedGame
from dynamics.moran import Moran
from dynamics.wright_fisher import WrightFisher

import unittest

class TestCase(unittest.TestCase):
    def setUp(self):
        import logging
        logging.basicConfig(filename='debug.log', level=logging.DEBUG)
    
    def test_single_simulation_moran(self):
        s = GameDynamicsWrapper(CWOLOnlyL, Moran, dynamics_kwargs=dict(pop_size=3000), game_kwargs=dict(a=0.2, equilibrium_tolerance=.5))
        s.simulate(num_gens=30000)
    
    def test_many_simulation(self):
        s = GameDynamicsWrapper(CWOL, WrightFisher, dynamics_kwargs=dict(), game_kwargs=dict(a=10, equilibrium_tolerance=.2))
        print (s.simulate_many(num_iterations=10, num_gens=150))
    
    def test_vary_one(self):
        s = VariedGame(CWOL, WrightFisher)
        s.vary_param('a', (0, 2, 60), num_gens=250, num_iterations=5)
    
    def test_vary_dependent(self):#Currently not working in Python 3.0
        s = VariedGame(CWOL, WrightFisher, game_kwargs=dict(equilibrium_tolerance=0.1))
        s.vary(game_kwargs=[{'c_low': (3, 12, 50)}, {'c_high': lambda o: (7.88 - o.c_low * o.p) / (1 - o.p)}], num_iterations=10, graph=True)
    
    def test_3d_graph(self):
        s = VariedGame(CWOL, WrightFisher)
        s.vary_2params('a', (0, 2, 30), 'b', (0, 5, 30), num_iterations=2, num_gens=150)
    
    def test_validate_classifier(self):
        CWOL.validate_classifier(timeout=300, tolerance=0.05)

if __name__ == '__main__':
    unittest.main()
        