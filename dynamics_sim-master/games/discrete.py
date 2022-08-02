from games.game import Game, SymmetricNPlayerGame
from games.payoff_matrices.discrete import generatePayoffs

n = 8  # Number of distinct values 98
m = n + 1
stratOptions = ['Punish iff S > ' + str(value) for value in range(0, m+2)]

class Discrete(SymmetricNPlayerGame):
    DEFAULT_PARAMS = dict(a=4, b=0, c=3, d=4, errorRange=1.1)
    PLAYER_LABELS = ['']
    STRATEGY_LABELS = (stratOptions)
    EQUILIBRIA_LABELS = ('Always punish', 'Never Punish', 'Coordinate on punishment')

    def __init__(self, a, b, c, d, errorRange, equilibrium_tolerance=0.2):
        payoff_matrix = [[0 for _ in range(m+2)] for _ in range(m+2)]

        values = (a, b, c, d, errorRange, n+2)  # For easier entry

        for i in range(m+2):  # My threshold is i
            for j in range(m+2):  # Your threshold is j
                payoff_matrix[i][j] = generatePayoffs(i, j, values)

        super(Discrete, self).__init__(payoff_matrix=payoff_matrix, n=2, equilibrium_tolerance=equilibrium_tolerance)

    @classmethod
    def classify(cls, params, state, tolerance):
        threshold = 1-tolerance

        if state[0][0] > threshold:
            return 0  # Always punish
        elif state[0][m+1] > threshold:
            return 1  # Never punish
        else:
            for value in range(1, m+1):
                if state[0][value] > threshold:
                    return 2  # Coordination on threshold
        return super(Discrete, cls).classify(params, state, tolerance)
