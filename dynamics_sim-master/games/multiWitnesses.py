from games.game import SymmetricNPlayerGame
from games.payoff_matrices.multiWitnesses import generatePayoffs

n = 18  # Number of distinct values
m = n + 1

step = 1 / n
stepRange = [step * value for value in range(m)]

stratOptions = ['Punish iff S > ' + str(round(stepRange[idx], 2)) for idx in range(m)]


class multiWitnesses(SymmetricNPlayerGame):
    DEFAULT_PARAMS = dict(a=4, b=0, c=2, d=4, errorRange=0.1)
    PLAYER_LABELS = ['']
    STRATEGY_LABELS = stratOptions
    EQUILIBRIA_LABELS = ('Always punish', 'Never Punish', 'Coordinate on punishment')

    def __init__(self, a, b, c, d, A, errorRange, equilibrium_tolerance=0.30):
        payoff_matrix = [[0 for _ in range(m)] for _ in range(m)]  # Add two to both if AP & NP

        values = (a, b, c, d, A, errorRange)  # For easier entry, A is the probability of an atom

        for i in range(m):  # General strategies coordinating punishment
            for j in range(m):
                payoff_matrix[j][i] = generatePayoffs(stepRange[i], stepRange[j], values)  # Offset by one if including always punish and never punish

        super(multiWitnesses, self).__init__(payoff_matrix=payoff_matrix, n=2, equilibrium_tolerance=equilibrium_tolerance)

    @classmethod
    def classify(cls, params, state, tolerance):
        threshold = 1-tolerance

        if state[0][0] > threshold:
            return 0  # Always punish
        elif state[0][m-1]+state[0][m-2] > threshold:  # +1 if AP & NP
            return 1  # Never punish
        else:
            for value in range(m):
                if state[0][value] > threshold:
                    return 2  # Coordination on threshold
        return super(multiWitnesses, cls).classify(params, state, tolerance)
