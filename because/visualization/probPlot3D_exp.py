"""
    Present a plot of the distributions for the given .py test file
    python3 Probabiity/probPlot.py <testfilepath>.py
    Data should previously have been generated using:
    python3 synth/synthDataGen.py <testfilepath>.py <numRecs>
"""
from sys import argv, path
if '.' not in path:
    path.append('.')
import time
from math import log, tanh, sqrt, sin, cos, e

import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from because.causality import rv
from because.synth import read_data, gen_data
from because.probability import independence
from because.probability.prob import ProbSpace
from because.probability.rkhs.rkhsMV import RKHS
from because.visualization import grid

def show(dataPath='', numRecs=0, targetSpec=[], condSpec=[], gtype='pdf', probspace=None, enhance=False):
    assert len(targetSpec) == 1 and len(condSpec) == 2, 'probPlot3D_exp.show:  Must provide exactly one target and two conditions.  Got: ' + str(targetSpec) + ', ' + str(condSpec)

    power = 3
    lim = 2  # Std's from the mean to test conditionals
    numPts = 30 # How many eval points for each conditional
    
    dims = 3

    if probspace is None:
        f = open(dataPath, 'r')
        exec(f.read(), globals())

        print('Testing: ', dataPath, '--', testDescript)
        gen = gen_data.Gen(dataPath)
        data = gen.getDataset(numRecs)
        prob1 = ProbSpace(data, power=power)
    else:
        prob1 = probspace
    
    numRecs = prob1.N
    if numRecs <= 1000:
        numPts = 15
    elif numRecs <= 10000:
        numPts = 20
    elif numRecs < 100000:
        numPts = 25
    else:
        numPts = 30 # How many eval points for each conditional

    target = targetSpec[0][0]
    cond = [condSpec[0][0], condSpec[1][0]]


    # Generate the test points
    g = grid.Grid(prob1, cond, lim, numPts)
    tps = g.makeGrid()
    incrs = g.getIncrs()
    isDisc = [prob1.isDiscrete(v) for v in cond]
    nTests = g.getTestCount()
    print('nTests = ', nTests)
    xt1 = []
    yt1 = []
    zt1 = []
    tnum = 0
    ssTot = 0 # Total sum of squares for R2 computation
    cmprs = []
    dp_est = []
    dp_start = time.time()
    for t in tps:
        condspec = []
        for c in range(dims-1):
            condIsDisc = isDisc[c]
            condVar = cond[c]
            val = t[c]
            if condIsDisc:
                spec = (condVar, val)
            else:
                spec = (condVar, val, val+incrs[c])
            condspec.append(spec)
        y_x = prob1.E(target, condspec)
        jp = prob1.P(condspec)
        if enhance and jp < .1/nTests:
            continue
        if y_x is None:
            continue
        xt1.append(t[0])
        yt1.append(t[1])
        zt1.append(y_x)
    dp_end = time.time()
    print('Test Time = ', round(dp_end-dp_start, 3))
    fig = plt.figure(constrained_layout=True)
    fig.suptitle('N=' + str(prob1.N))
    x = np.array(xt1)
    y = np.array(yt1)
    z = np.array(zt1)
    my_cmap = plt.get_cmap('plasma')
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_trisurf(x, y, z, cmap = my_cmap)
    ax.set_xlabel(cond[0], fontweight='bold')
    ax.set_ylabel(cond[1], fontweight='bold')
    ax.set_zlabel('E(' + target + ' | ' + cond[0] + ', ' + cond[1] + ')', fontweight='bold')
    ax.view_init(20, -165)

    plt.show()

if __name__ == '__main__':
    if '-h' in argv or len(argv) < 4:
        print('Usage: python because/visualization/probPlot3D_exp.py dataPath targets condition [numRecs]')
        print('  dataPath is the path to a .py (synthetic data) or .csv file')
        print('  targets is the variable(s) whose distribution to plot.')
        print('  conditions are the conditional variable names.')
        print('  numRecs is the number of records to generate')
    else:
        numRecs = 0 
        args = argv
        dataPath = args[1].strip()
        targets = args[2].strip()
        conditions = args[3].strip()
        tokens = targets.split(',')
        tSpec = []
        for token in tokens:
            varName = token.strip()
            if varName:
                tSpec.append((varName,))
        tokens = conditions.split(',')
        cSpec = []
        for token in tokens:
            varName = token.strip()
            if varName:
                cSpec.append((varName,))
        if len(args) > 4:
            try:
                numRecs = int(args[4].strip())
            except:
                pass
        gtype = 'pdf'
       
        #print('dims, datSize, numRecs = ', dims, datSize, numRecs)
        show(dataPath=dataPath, numRecs=numRecs, targetSpec=tSpec, condSpec=cSpec, gtype=gtype)
