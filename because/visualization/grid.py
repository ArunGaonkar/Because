import numpy as np

class Grid:
    def __init__(self, ps, vars, lim=1, numPts=20):
        dims = len(vars)
        assert dims > 0 and dims <= 3, 'makeGrid:  Only dimensionality 1 through 3 is supported.  Got: ' +  str(dims)
        distrs = [ps.distr(c) for c in vars]
        minvs = [distr.percentile(lim) for distr in distrs]
        maxvs = [distr.percentile(100-lim) for distr in distrs]
        incrs = [(maxvs[i] - minvs[i]) / (numPts-1) for i in range(dims)]
        vSpaces = []
        incrs = []
        nTests = 1
        for i in range(dims):
            var = vars[i]
            if ps.isDiscrete(var):
                vSpace = ps.getMidpoints(var)
                incrs.append(1)
            else:
                vSpace = list(np.linspace(minvs[i], maxvs[i], numPts))
                incrs.append(vSpace[1] - vSpace[0])
            nTests *= len(vSpace)
            vSpaces.append(vSpace)
        self.dims = dims
        self.vSpaces = vSpaces
        self.incrs = incrs
        self.nTests = nTests

    def getTestCount(self, varNum=None):
        if varNum is not None:
            return len(self.vSpaces[varNum])
        return self.nTests

    def getIncrs(self):
        return self.incrs

    def makeGrid(self):
        vSpaces = self.vSpaces
        dims = self.dims
        for val1 in vSpaces[0]:
            if dims > 1:
                for val2 in vSpaces[1]:
                    if dims > 2:
                        for val3 in vSpaces[2]:
                            yield ((val1, val2, val3))
                    else:
                        yield ((val1, val2))
            else:
                yield((val1,))
    
    
                
        


