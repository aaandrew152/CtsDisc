from wrapper import GameDynamicsWrapper

from dynamics.wright_fisher import WrightFisher

from games.atomHuniE import AtomHUniE
from games.stateDep import StateDep
from games.discrete import Discrete
from games.uniHuniE import UniHuniE
from games.normalHUniE import NormalHuniE

import unittest

uni_state = [[0 for _ in range(11)]]
uni_state[0][4] += 100

atom_state = [[0 for _ in range(11)]]
atom_state[0][4] += 100

normal_state = [[0 for _ in range(19)]]
normal_state[0][3] += 100

p_stable = dict(a=4, b=0, c=1, d=4, errorRange=1.1)
p_unstable = dict(a=4, b=0, c=3, d=4, errorRange=1.1)


class TestCase(unittest.TestCase):
    def setUp(self):
        import logging
        logging.basicConfig(filename='debug.log', level=logging.DEBUG)

    def test_uni_unstab(self):
        s = GameDynamicsWrapper(UniHuniE, WrightFisher, dynamics_kwargs=dict(selection_strength=0.25))
        #s.simulate(num_gens=190, graph=dict(shading='redblue', options=['no_legend', 'meanStratLine', 'payoffLine', 'area', 'no_axis', 'no_text']), start_state=uni_state)

    def test_many_uni_unstab(self):  # Shows no threshold equilibrium norm exists in the atom case when p is high
        s = GameDynamicsWrapper(UniHuniE, WrightFisher, dynamics_kwargs=dict(selection_strength=0.25))
        #s.simulate_many(num_iterations=500, num_gens=190, graph=dict(shading='redblue', options=['area', 'no_legend', 'no_axis']), start_state=uni_state)

    def test_disc_unstab(self):
        s = GameDynamicsWrapper(Discrete, WrightFisher, game_kwargs=p_unstable, dynamics_kwargs=dict(selection_strength=0.25))
        #s.simulate(num_gens=190, graph=dict(shading='redblue', options=['no_legend', 'area', 'meanStratLine', 'payoffLine', 'no_axis', 'no_text']), start_state=atom_state)

    def test_many_disc_unstab(self):  # Shows no threshold equilibrium norm exists in the atom case when p is high
        s = GameDynamicsWrapper(Discrete, WrightFisher, game_kwargs=p_unstable, dynamics_kwargs=dict(selection_strength=0.25))
        #s.simulate_many(num_iterations=500, num_gens=190, graph=dict(shading='redblue', options=['area', 'no_legend', 'no_axis']), start_state=atom_state)

    def test_disc_stab(self):
        s = GameDynamicsWrapper(Discrete, WrightFisher, game_kwargs=p_stable, dynamics_kwargs=dict(selection_strength=0.25))
        #s.simulate(num_gens=190, graph=dict(shading='redblue', options=['no_legend', 'area', 'meanStratLine', 'payoffLine', 'no_axis', 'no_text']), start_state=atom_state)

    def test_many_disc_stab(self):  # Ascertains the unique equilibrium norm in the atom case for average p is stable.
        s = GameDynamicsWrapper(Discrete, WrightFisher, game_kwargs=p_stable, dynamics_kwargs=dict(selection_strength=0.25))
        #s.simulate_many(num_iterations=500, num_gens=190, graph=dict(shading='redblue', options=['area', 'no_legend', 'no_axis']), start_state=atom_state)

    def test_normal(self):  # Checks for stability of normal threshold equilibrium
        s = GameDynamicsWrapper(NormalHuniE, WrightFisher, dynamics_kwargs=dict(selection_strength=0.23))
        s.simulate(num_gens=500, graph=dict(shading='expandrb', options=['area', 'meanStratLine', 'payoffLine', 'no_legend', 'no_axis', 'no_text']), start_state=normal_state)

    def test_many_normal(self):  # Checks for stability of normal threshold equilibrium
        s = GameDynamicsWrapper(NormalHuniE, WrightFisher, dynamics_kwargs=dict(selection_strength=0.23))
        #s.simulate_many(num_iterations=500, num_gens=500, graph=dict(shading='expandrb', options=['area', 'no_legend', 'no_axis']), start_state=normal_state)


if __name__ == '__main__':
    unittest.main()