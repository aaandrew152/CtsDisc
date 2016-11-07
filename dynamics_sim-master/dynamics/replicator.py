from dynamics.dynamics import StochasticDynamicsSimulator
import numpy as np

class Replicator(StochasticDynamicsSimulator):
    """
    A stochastic dynamics simulator which performs replicator dynamics on all player types in the population.
    """
    def __init__(self, generation_skip=1, *args, **kwargs):#Recommended to use a higher population number if utilizing generationSkip
        """
        The constructor for the Replicator dynamics process, that the number of births/deaths to precess per time step.
        
        @param num_iterations_per_time_step: the number of iterations of the Moran process we do per time step
        @type num_iterations_per_time_step: int
        """
        super(Replicator, self).__init__(*args, **kwargs)
        self.generation_skip = generation_skip
        
    def next_generation(self, previousState):
        nextState = []
        
        fitness = self.calculate_fitnesses(previousState)

        for pIndex, (fitnesses, stratDistribution, numPlayers) in enumerate(zip(fitness, previousState, self.num_players)):
            meanFitness = np.mean(fitnesses)
            
            newPlayerState = np.zeros(len(fitnesses))
            for stratIndex, (stratFitness, stratProportion) in enumerate(zip(fitnesses, stratDistribution)):
                dStrat = stratProportion * (stratFitness - meanFitness) / self.generation_skip
                newPlayerState[stratIndex] = stratProportion + dStrat
                
            for i, strat in enumerate(newPlayerState):
                if strat < 0:
                    newPlayerState[i] = 0
            if newPlayerState.sum() <= 0:
                for i in range(len(newPlayerState)):
                    newPlayerState[i] = 1#Normalization in edge cases (to prevent negative distributions or all 0 distributions
                    
            newPlayerState *= float(numPlayers / newPlayerState.sum())
            newPlayerState = np.array(self.round_individuals(newPlayerState))
            nextState.append(newPlayerState)

        return nextState, fitness
        
    