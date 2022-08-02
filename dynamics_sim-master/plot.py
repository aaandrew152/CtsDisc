import matplotlib.pyplot as plt
import numpy
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import math
import copy
from plotHelperFunct import *

redBlueShades = [(229, 0, 15), (206, 3, 32), (183, 7, 50), (160, 11, 67), (137, 15, 85), (114, 19, 103), (91, 22, 120),
                 (68, 26, 138), (45, 30, 155), (22, 34, 173), (0, 0, 244)]

expandRBShades = []
for idx, shade in enumerate(redBlueShades):
    expandRBShades.append(shade)

    if idx != len(redBlueShades) - 1:
        blendShade = tuple([shade[tupIdx] + redBlueShades[idx + 1][tupIdx] for tupIdx in range(3)])
        blendShade = tuple([blendShade[tupIdx] / 2 for tupIdx in range(3)])
        expandRBShades.append(blendShade)

superExpandRBShades = []
for idx, shade in enumerate(redBlueShades):
    superExpandRBShades.append(shade)

    if idx != len(redBlueShades) - 1:
        blendShade = tuple([redBlueShades[idx + 1][tupIdx] - shade[tupIdx] for tupIdx in range(3)])
        stepShade = tuple([blendShade[tupIdx] / 11 for tupIdx in range(3)])
        newShade = shade

        for i in range(10):
            newShade = tuple([newShade[tupIdx] + stepShade[tupIdx] for tupIdx in range(3)])
            superExpandRBShades.append(newShade)

class GraphOptions:
    COLORS_KEY = 'colors'
    RED_TO_BLUE_COLORS_KEY = 'Red to Blue gradient'
    EXPAND_RB_COLORS_KEY = 'Red to Blue gradient expanded'
    SUPER_EXPAND_RB_COLORS_KEY = 'Red to Blue with 100 colors'
    EXTRA_COLORS = 'extra colors if more than 7 to be shown'
    Y_LABEL_KEY = 'y_label'
    LEGEND_LOCATION_KEY = 'legend_location'
    SHOW_GRID_KEY = 'grid'
    LEGEND_LABELS_KEY = 'legend_labels'
    TITLE_KEY = 'title'
    MARKERS_KEY = 'markers'
    NO_MARKERS_KEY = 'hide_markers'
    PLAYER_TYPES = 'Group certain graphs'

    default = {COLORS_KEY: ['Cyan', 'Blue', 'Green', 'Yellow', 'Red', 'Magenta', 'Black', 'BlueViolet', 'Crimson', 'Indigo'] * 5,  # If extra colors needed it repeats
               RED_TO_BLUE_COLORS_KEY: [(value[0]/255, value[1]/255, value[2]/255) for value in redBlueShades],
               EXPAND_RB_COLORS_KEY: [(value[0]/255, value[1]/255, value[2]/255) for value in expandRBShades],
               SUPER_EXPAND_RB_COLORS_KEY: [(value[0] / 255, value[1] / 255, value[2] / 255) for value in superExpandRBShades],
               MARKERS_KEY: "o.v8sh+xD|_ ",
               NO_MARKERS_KEY: False,
               Y_LABEL_KEY: "Proportion of Population",
               LEGEND_LOCATION_KEY: 'upper right',
               SHOW_GRID_KEY: True,
               TITLE_KEY: lambda player_i: "Population Dynamics for Player %d" % player_i,
               LEGEND_LABELS_KEY: lambda graph_i, cat_i: "X_%d,%d" % (graph_i, cat_i),
               PLAYER_TYPES: False}


def plot_data_for_players(data, x_range, x_label, num_strats, num_players=None, graph_options=None,
                          title="Proportion of Population", yBot=None, mslPos=None):
    # data is a list of n = (the number of player types) of 2D arrays
    # 1st dimension indices are the index into the x_range array
    # 2nd dimension indices are the index of the strategy number
    # num_players tells us the total number of players devoted to each player type, or None if already normalized

    # normalize data, if needed
    if num_players is not None:
        normalized_data = []
        for i, player in enumerate(data):
            num_gens, n_strats = player.shape
            d = numpy.zeros((num_gens, n_strats))
            for gen_i in range(num_gens):
                for strat_i in range(n_strats):
                    d[gen_i, strat_i] = player[gen_i, strat_i] / float(num_players[i])
            normalized_data.append(d)
        data = normalized_data
    old_options = GraphOptions.default.copy()
    if graph_options is not None:
        old_options.update(graph_options)
    graph_options = old_options

    plot_data(data, x_label, x_range, title, graph_options[GraphOptions.TITLE_KEY], num_strats,
              graph_options=graph_options, yBot=yBot, mslPos=mslPos)


def plot_single_data_set(data, x_label, x_values, y_label, title, num_categories, graph_options=None):
    legend_labels = graph_options[GraphOptions.LEGEND_LABELS_KEY]
    graph_options[GraphOptions.LEGEND_LABELS_KEY] = lambda i, j: legend_labels(j)
    plot_data([data], x_label, x_values, y_label, lambda i: title, [num_categories], graph_options=graph_options)


def _append_options(options):
    old_options = GraphOptions.default.copy()
    if options is not None:
        old_options.update(options)
    return old_options

#TODO rewrite so that mslPos doesn't need to be carried around separately
def plot_data(data, x_label, x_values, y_label, title_i, num_categories, graph_options=None, yBot=None, mslPos=None):
    """
    support for multiple 2d arrays, each as an entry in the data array
    All data should be normalized before being passed in
    """

    n_x = len(x_values)
    for state_i, n_cats in zip(data, num_categories):
        n, s = state_i.shape
        assert n == n_x
        assert s == n_cats

    graph_options = _append_options(graph_options)

    #Determine coloration
    if 'shading' in graph_options:
        shading = graph_options['shading'].lower()
        if ',' in shading:
            color, different = graph_options['shading'].split(',')
            different = int(different)
        else:
            color = shading
            different = 10

        shading = [value / different for value in range(different)]
        lightShading = [value / (different * 3) for value in range(different)]

        if color == 'blue':
            colors = [(lightShading[idx], lightShading[idx], value) for idx, value in enumerate(shading)]
        elif color == 'green':
            colors = [(lightShading[idx], value, lightShading[idx]) for idx, value in enumerate(shading)]
        elif color == 'red':
            colors = [(value, lightShading[idx], lightShading[idx]) for idx, value in enumerate(shading)]
        elif color == 'redblue':
            colors = graph_options[GraphOptions.RED_TO_BLUE_COLORS_KEY]
        elif color == 'expandrb':
            colors = graph_options[GraphOptions.EXPAND_RB_COLORS_KEY]
        elif color == 'superexpandrb':
            colors = graph_options[GraphOptions.SUPER_EXPAND_RB_COLORS_KEY]
        else:
            print('Please enter a valid color!')
            colors = graph_options[GraphOptions.COLORS_KEY]
    else:
        colors = graph_options[GraphOptions.COLORS_KEY]

    category_labels = graph_options[GraphOptions.LEGEND_LABELS_KEY]
    markers = graph_options[GraphOptions.MARKERS_KEY]

    if graph_options[GraphOptions.PLAYER_TYPES]:
        print("not implemented")
    else:
        # graph the results
        for i, data_i in enumerate(data):
            rawData = copy.deepcopy(data_i)
            plt.figure(i)
            plt.title(title_i(i))
            
            if 'area' in graph_options:
                stackProportions(data_i)   
                
            if 'normalize' in graph_options:
                x_values = normalize(x_values, graph_options['normalize'])
    
            # iterate over all the generations
            num_xs, n_cats = data_i.shape

            if yBot is None:
                plt.ylim([-0.01, 1.01])
            else:
                plt.ylim([yBot, 1.01])

            plt.xlim([x_values[0], x_values[-1]])
            if not 'no_axis' in graph_options:
                plt.ylabel(y_label)
                plt.xlabel(x_label)
            #plt.grid()graph_options[GraphOptions.SHOW_GRID_KEY])

            if 'no_axis' in graph_options:
                plt.gca().axes.xaxis.set_ticklabels([])
                plt.gca().axes.yaxis.set_ticklabels([])

            # iterate over all the categories
            for cat_i in range(n_cats):
                if graph_options[GraphOptions.NO_MARKERS_KEY]:
                    marker = ' '
                else:
                    marker = markers[cat_i // n_cats]                  

                if 'area' in graph_options:
                    if cat_i == 0:
                        plt.fill_between(x_values, data_i[:, cat_i], 0, color=colors[cat_i % n_cats])
                    else:
                        plt.fill_between(x_values, data_i[:, cat_i], data_i[:, cat_i-1], color=colors[cat_i % n_cats])

                plt.plot(x_values, data_i[:, cat_i], c=colors[cat_i % n_cats], lw=2, marker=marker)
                
            labels = [category_labels(i, j) for j in range(n_cats)]
            if not 'no_legend' in graph_options:
                plt.legend(labels, loc=graph_options[GraphOptions.LEGEND_LOCATION_KEY])

            if 'lineArray' in graph_options:
                graphLines(graph_options['lineArray'], plt)
            if 'meanStratLine' in graph_options:
                for genNumber, gen in enumerate(rawData):
                    avgColor = colorAvg(colors, gen)
                    line = [genNumber, genNumber + 1, mslPos, mslPos]
                    graph_options['colorLineArray'][i].append([line, avgColor])
            if 'colorLineArray' in graph_options:
                graphColoredLines(graph_options['colorLineArray'][i], plt, colors)
            if 'textList' in graph_options:
                plotText(graph_options['textList'], plt)

    plt.show()
    
def plot_contour_data_set(data, y_label, y_values, x_label, x_values, z_label, title, num_categories, graph_options=None):
    # Note it seems as though the x and y values are switched for contour plots
    
    graph_options = _append_options(graph_options)
    category_labels = graph_options[GraphOptions.LEGEND_LABELS_KEY]
    plt.close('all')
    
    colors = ['DarkSlateGray', 'DarkGreen', 'Green', 'ForestGreen',
              'LimeGreen', 'Lime', 'LawnGreen', 'Chartreuse', 'GreenYellow',
              'Yellow', 'Khaki', 'PaleGoldenrod', 'LightGoldenrodYellow',
              'LightYellow', 'White'] 
    
    # iterate over all the generations
    num_xs, num_ys, n_cats = data.shape
    assert num_categories == n_cats
    
    # Iterate over all categories
    x_values = numpy.array(x_values)
    y_values = numpy.array(y_values)
    
    levels = [x/len(colors) for x in range(len(colors)+1)]
    
    root = math.ceil(math.sqrt(n_cats))
    if root * (root - 1) >= n_cats:
        rootX = root - 1
    else:
        rootX = root
    
    fig, axs = plt.subplots(rootX, root)
    ax = axs.ravel()
    for cat_i in range(n_cats):
        cs = ax[cat_i].contourf(x_values, y_values, data[:, :, cat_i], levels, colors=colors)
        fig.colorbar(cs, ax=ax[cat_i])
        ax[cat_i].set_title(category_labels(cat_i))
        ax[cat_i].set_xlabel(x_label)
        ax[cat_i].set_ylabel(y_label)

        if 'lineArray' in graph_options:
            graphLines(graph_options['lineArray'], ax[cat_i])

    plt.show()


def plot_3d_data_set(data, x_label, x_values, y_label, y_values, z_label, title, num_categories, graph_options=None):

    graph_options = _append_options(graph_options)
    colors = graph_options[GraphOptions.COLORS_KEY]
    category_labels = graph_options[GraphOptions.LEGEND_LABELS_KEY]
    plt.close('all')
    fig = plt.figure()

    # iterate over all the generations
    num_xs, num_ys, n_cats = data.shape
    assert num_categories == n_cats

    # iterate over all the categories
    x_values = numpy.array(x_values)
    y_values = numpy.array(y_values)
    nx = len(x_values)
    ny = len(y_values)
    assert nx == num_xs
    assert ny == num_ys
    xs = numpy.repeat(x_values, ny)
    xs.resize((nx, ny))
    ys = numpy.tile(y_values, nx)
    ys.resize((nx, ny))

    dim = int(numpy.ceil(numpy.sqrt(n_cats)))
    for cat_i in range(n_cats):
        ax = fig.add_subplot(dim, dim, cat_i + 1, projection='3d')
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        zs = data[:, :, cat_i]
        ax.set_title(category_labels(cat_i))
        ax.plot_wireframe(xs, ys, zs, color=colors[cat_i % n_cats])#3d Visualization

    fig2 = plt.figure()
    ax = fig2.add_subplot(1, 1, 1, projection='3d')
    # plot_wireframe
    # TODO: plot surface seems to look better, except it doesn't play nicely with multiple surfaces on the same graph
    for cat_i in range(n_cats):
        zs = data[:, :, cat_i]
        ax.plot_wireframe(xs, ys, zs, color=colors[cat_i % n_cats])
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)    
    
    labels = [category_labels(j) for j in range(n_cats)]
    plt.legend(labels, loc=graph_options[GraphOptions.LEGEND_LOCATION_KEY])
    plt.show()