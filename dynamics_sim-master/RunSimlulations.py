from wrapper import GameDynamicsWrapper

from dynamics.wright_fisher import WrightFisher

from games.atomHuniE import AtomHUniE
from games.stateDep import StateDep
from games.discrete import Discrete
from games.uniHuniE import UniHuniE
from games.normalHUniE import NormalHuniE

import unittest

# Starting strategy distributions
uni_state = [[0 for _ in range(11)]]
uni_state[0][4] += 100

atom_state = [[0 for _ in range(11)]]
atom_state[0][4] += 100

normal_below_state = [[0 for _ in range(19)]]
normal_below_state[0][14] += 100

normal_above_state = [[0 for _ in range(19)]]
normal_above_state[0][7] += 100

# Levels of p
p_stable = dict(a=4, b=0, c=1, d=4, errorRange=1.1)
p_unstable = dict(a=4, b=0, c=3, d=4, errorRange=1.1)
p_uniform = dict(a=4, b=0, c=2, d=4, errorRange=1/5)
p_normal = dict(a=40, b=0, c=2.5, d=30, errorRange=0.5)


class TestCase(unittest.TestCase):
    def setUp(self):
        import logging
        logging.basicConfig(filename='debug.log', level=logging.DEBUG)

    def test_uni_unstab(self):  # Single Run: No threshold equilibrium norm exists in the uniform case when p is high
        s = GameDynamicsWrapper(UniHuniE, WrightFisher, game_kwargs=p_uniform, dynamics_kwargs=dict(selection_strength=0.25))
        s.simulate(num_gens=190, graph=dict(shading='redblue', options=['no_legend', 'meanStratLine', 'payoffLine', 'area', 'no_axis', 'no_text']), start_state=uni_state)

    def test_many_uni_unstab(self):  # Average Run: No threshold equilibrium norm exists in the uniform case when p is high
        s = GameDynamicsWrapper(UniHuniE, WrightFisher, game_kwargs=p_uniform, dynamics_kwargs=dict(selection_strength=0.25))
        s.simulate_many(num_iterations=500, num_gens=190, graph=dict(shading='redblue', options=['area', 'no_legend', 'no_axis']), start_state=uni_state)

    def test_disc_unstab(self):  # Single Run: No threshold equilibrium norm exists in the discrete case when p is high
        s = GameDynamicsWrapper(Discrete, WrightFisher, game_kwargs=p_unstable, dynamics_kwargs=dict(selection_strength=0.25))
        s.simulate(num_gens=190, graph=dict(shading='redblue', options=['no_legend', 'area', 'meanStratLine', 'payoffLine', 'no_axis', 'no_text']), start_state=atom_state)

    def test_many_disc_unstab(self):  # Average Run: No threshold equilibrium norm exists in the discrete case when p is high
        s = GameDynamicsWrapper(Discrete, WrightFisher, game_kwargs=p_unstable, dynamics_kwargs=dict(selection_strength=0.25))
        s.simulate_many(num_iterations=500, num_gens=190, graph=dict(shading='redblue', options=['area', 'no_legend', 'no_axis']), start_state=atom_state)

    def test_disc_stab(self):  # Single Run: Threshold equilibrium norm exists in the discrete case when p is moderate
        s = GameDynamicsWrapper(Discrete, WrightFisher, game_kwargs=p_stable, dynamics_kwargs=dict(selection_strength=0.25))
        s.simulate(num_gens=190, graph=dict(shading='redblue', options=['no_legend', 'area', 'meanStratLine', 'payoffLine', 'no_axis', 'no_text']), start_state=atom_state)

    def test_many_disc_stab(self):  # Average Run: Threshold equilibrium norm exists in the discrete case when p is moderate
        s = GameDynamicsWrapper(Discrete, WrightFisher, game_kwargs=p_stable, dynamics_kwargs=dict(selection_strength=0.25))
        s.simulate_many(num_iterations=500, num_gens=190, graph=dict(shading='redblue', options=['area', 'no_legend', 'no_axis']), start_state=atom_state)

    def test_normal_below(self):  # Single Run: Normal with starting state below
        s = GameDynamicsWrapper(NormalHuniE, WrightFisher, game_kwargs=p_normal, dynamics_kwargs=dict(selection_strength=0.25))
        s.simulate(num_gens=500, graph=dict(shading='expandrb', options=['area', 'meanStratLine', 'payoffLine', 'no_legend', 'no_axis', 'no_text']), start_state=normal_below_state)

    def test_many_normal(self):  # Average Run: Normal with starting state below
        s = GameDynamicsWrapper(NormalHuniE, WrightFisher, game_kwargs=p_normal, dynamics_kwargs=dict(selection_strength=0.25))
        s.simulate_many(num_iterations=500, num_gens=500, graph=dict(shading='expandrb', options=['area', 'no_legend', 'no_axis']), start_state=normal_below_state)

    def test_normal_above(self):  # Single Run: Normal with starting state below
        s = GameDynamicsWrapper(NormalHuniE, WrightFisher, game_kwargs=p_normal, dynamics_kwargs=dict(selection_strength=0.25))
        s.simulate(num_gens=500, graph=dict(shading='expandrb', options=['area', 'meanStratLine', 'payoffLine', 'no_legend', 'no_axis', 'no_text']), start_state=normal_above_state)

    def test_many_normal_above(self):  # Average Run: Normal with starting state above
        s = GameDynamicsWrapper(NormalHuniE, WrightFisher, game_kwargs=p_normal, dynamics_kwargs=dict(selection_strength=0.25))
        s.simulate_many(num_iterations=500, num_gens=500, graph=dict(shading='expandrb', options=['area', 'no_legend', 'no_axis']), start_state=normal_above_state)


if __name__ == '__main__':
    unittest.main()