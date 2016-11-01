import math
import numpy as np

def profile(func): return func

class Craft(object):

    def __init__(self,delta_t,x=0.0,y=0.0,z=0.0,v_x=0.0,v_y=0.0,v_z=0.0,mass=0):

        #Position in km
        self.position=np.array([np.longdouble(x),np.longdouble(y),np.longdouble(z)])

        #Velocity in km/s
        self.velocity=np.array([np.longdouble(v_x),np.longdouble(v_y),np.longdouble(v_z)])

        #Mass in kg
        self.mass=mass

        #delta_t in days
        self.delta_t=np.longdouble(delta_t)*86400

        #Initialize Trajectory history of positions
        self.trajectory=[[np.longdouble(x)],[np.longdouble(y)],[np.longdouble(z)]]

        #Initialize Force Array
        self.force=np.zeros(3,dtype=np.longdouble)

        #Class Constants related to Self.Mass
        gConstant = np.longdouble(0.00000000006674)
        self.forceFactor = gConstant*self.mass / 1000000
        self.velocityFactor = self.delta_t / self.mass / 1000

    @profile
    def forceG(self, body):
        """Updates force of the body on the Craft"""

        dist = self.position - body.position
        gComponent = (self.forceFactor * body.mass/((dist[0]**2 + dist[1]**2 + dist[2]**2)**1.5))

        self.force -= np.dot(dist, gComponent)

    def update(self):
        """Updates simulation based on calculations for force"""

        #Velocity and Position
        self.velocity+=np.dot(self.force,self.velocityFactor)
        self.position+=np.dot(self.velocity,self.delta_t)

        #Reset Force profile
        self.force=np.zeros(3,dtype=np.longdouble)

    def log(self):
        for i in range(3):
            self.trajectory[i].append(self.position[i])
