import numpy as np
import os

from jplephem.spk import SPK

class Planet(object):

    def __init__(self, kernel, planetID, relativeID, mass):
        if kernel is None:
            raise ValueError("Need a base kernel, like de430.bsp")
        
        self._planetID = planetID
        self._relativeID = relativeID
        self._kernel = kernel
        self.mass = mass
        self.position = np.zeros(3, dtype = np.longdouble)

        #Initialize Position History
        self.trajectory = [[], [], []]

    def logPosition(self):
        if self._planetID != self._relativeID:
            for i in xrange(3):
                self.trajectory[i].append(self.position[i])

    def updatePosition(self, time):
        if self._planetID != self._relativeID: self.position = (self._kernel[3, self._planetID].compute(time) - self._kernel[3, self._relativeID].compute(time))

#class CelestialBodies(object):
 #   def __init__(self, mass, position=None):
  #      if not os.path.isfile('de430.bsp'):
   #         raise ValueError('de430.bsp Was not found!')
    #    self.kernel = SPK.open('de430.bsp')

    #    self.mass = mass
    #    self.hist = [[],[],[]]
    #    if position is not None:
     #       self.pos = position
    #    else:
     #       self.pos = []

 #    def getPos(time):
 #       """Returns the position relative to the solar system barycentere"""
  #      return kernel[3, self.KERNAL_CONSTANT].compute(time)

#class Earth(CelestialBodies):
 #   KERNAL_CONSTANT = 399

 #   def __init__(self, mass):
  #      super(Earth, self).__init__(mass)

 #   def getRealPos(time):
  #      """Returns relative position of the Earth"""

  #      location = np.longdouble(0)
  #      self.pos = np.array([location, location, location])
  #      return self.pos

#class Moon(CelestialBodies):
 #   KERNAL_CONSTANT = 301

 #   def __init__(self, mass):
  #      super(Moon, self).__init__(mass)

 #   def getRealPos(time):
  #      """Returns relative position of the Moon"""

  #      self.pos = self.getPos(time) - kernel[3, 399].compute(time)
  #      return np.array([np.longdouble(self.pos[0]), np.longdouble(self.pos[1]), np.longdouble(self.pos[2])])      