import numpy as np

class Planet(object):

    def __init__(self, kernel, planetID, relativeID, mass):
        if kernel is None:
            raise ValueError("Need a base kernel, like de430.bsp")
        
        self._planetID = planetID
        self._relativeID = relativeID
        self._kernel = kernel
        self._mass = mass
        self.position = np.zeroes(3, dtype = np.longdouble)

        #Initialize Position History
        self.trajectory = [[], [], []]

    def logPosition(self):
        if self._planetID != self._relativeID:
            for i in xrange(3):
                self.trajectory[i].append(self.position[i])

    def updatePosition(self, time):
        if self._planetID != self._relativeID: self.position = (self._kernel[3, self._planetID].compute(time) - self._kernel[3, self._relativeID].compute(time))
        