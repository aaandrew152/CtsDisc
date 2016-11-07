from wrapper import GameDynamicsWrapper

from dynamics.wright_fisher import WrightFisher

from games.uniHuniE import UniHuniE
from games.normalHuniE import NormalHuniE
from games.discrete import Discrete

import unittest

state = [[0 for x in range(19)]]
state[0][1] += 100

class TestCase(unittest.TestCase):
    def setUp(self):
        import logging
        logging.basicConfig(filename='debug.log', level=logging.DEBUG)

    def test_single_simulation(self):
        s = GameDynamicsWrapper(NormalHuniE, WrightFisher, dynamics_kwargs=dict(selection_strength=0.25))
        #s.simulate(num_gens=5000, graph=dict(shading='expandRB', options=['area', 'meanStratLine', 'payoffLine']), start_state=state)


    def normal_graph(self):
        s = GameDynamicsWrapper(NormalHuniE, WrightFisher, dynamics_kwargs=dict(selection_strength=0.25))
        #s.simulate(num_gens=5000, graph=dict(shading='expandRB', options=['area', 'meanStratLine', 'payoffLine']), start_state=state)

    def normal_threshold_is_unstable_over_many_runs(self):  # Ascertains the unique equilibrium norm in the normal case is unstable.
        s = GameDynamicsWrapper(NormalHuniE, WrightFisher, dynamics_kwargs=dict(selection_strength=0.25))
        #print(s.simulate_many(num_iterations=500, num_gens=5000, graph=False, burn=4000, start_state=state))
if __name__ == '__main__':
    unittest.main()