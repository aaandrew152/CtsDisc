from plot import plot_data_for_players, GraphOptions

def setupGraph(graph, game, dyn, burn, num_gens, results, payoffs):  # TODO allow ordering of various lines
    if graph is True:
        graph = dict()
    graph_options = graph
    if 'options' in graph_options:
        order = 1
        for key in graph_options['options']:
            graph_options[key] = True


    yPos = 0

    if game.STRATEGY_LABELS is not None:
        graph_options[GraphOptions.LEGEND_LABELS_KEY] = lambda p, s: game.STRATEGY_LABELS[p][s]

    if game.PLAYER_LABELS is not None:
        graph_options[GraphOptions.TITLE_KEY] = lambda p: game.PLAYER_LABELS[p]

    if any(k in graph_options for k in ['payoffLine', 'modeStratLine', 'meanStratLine']):
        yPos = 0
        graph_options['colorLineArray'] = [[] for player in results]
        graph_options['textList'] = []

    if 'payoffLine' in graph_options:
        yPos -= 0.05
        for playerIdx, player in enumerate(payoffs):
            colorLineArray = []
            for gen in range(burn, num_gens - 1):
                maxPayoff = 0
                maxPayoffIdx = -1
                for payoffIdx, payoff in enumerate(player[gen]):
                    if payoff > maxPayoff:
                        maxPayoff = payoff
                        maxPayoffIdx = payoffIdx

                currentGen = gen - burn
                nextGen = gen - burn + 1

                line = [currentGen, nextGen, yPos, yPos]
                colorLineArray.append([line, maxPayoffIdx])
            # colorLineArray[0][1] = colorLineArray[1][1]  # To fill in first gen
            graph_options['colorLineArray'][playerIdx].extend(colorLineArray)
            graph_options['textList'].append(([-num_gens / 10, yPos], 'Greatest payoff'))  # TODO fix x positioning

    if 'modeStratLine' in graph_options:
        yPos -= 0.05
        for playerIdx, player in enumerate(results):
            colorLineArray = []
            for gen in range(burn, num_gens):
                maxStratProp = 0
                maxStratIdx = -1
                for stratIdx, stratProp in enumerate(player[gen]):
                    if stratProp > maxStratProp:
                        maxStratProp = stratProp
                        maxStratIdx = stratIdx

                currentGen = gen - burn
                nextGen = gen - burn + 1
                line = [currentGen, nextGen, yPos, yPos]
                colorLineArray.append([line, maxStratIdx])
            graph_options['colorLineArray'][playerIdx].extend(colorLineArray)
            graph_options['textList'].append(([-num_gens / 10, yPos], 'Modal strategy'))

    if 'meanStratLine' in graph_options:
        yPos -= 0.05
        graph_options['textList'].append(([-num_gens / 10, yPos], 'Average strategy'))

    yPos -= 0.025

    graph_options[GraphOptions.NO_MARKERS_KEY] = True

    plot_data_for_players(results, range(burn, num_gens), "Generation #", dyn.pm.num_strats,
                          num_players=dyn.num_players,
                          graph_options=graph_options, yBot=yPos)

    if 'graph_payoffs' in graph_options:
        if burn == 0:
            burn = 1
        plot_data_for_players(payoffs, range(burn, num_gens), "Generation #", dyn.pm.num_strats,
                              num_players=dyn.num_players,
                              graph_options=dict(), title="Normalized Payoffs")