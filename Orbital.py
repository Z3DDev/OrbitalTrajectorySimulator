import time as t
import math
import sys

from jplephem.spk import SPK
import os

from astropy.time import Time
import numpy as np

sys.path.append('./Objects/')

from Objects import Craft
from planets import Planet

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def profile(func): return func

#Plotting 3D Output
def drawSphere(xCenter, yCenter, zCenter, r):
    #Program Drwas the Sphere
    u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
    x = np.cos(u) * np.sin(v)
    y = np.sin(u) * np.sin(v)
    z = np.cos(v)

    # Shift and Scale 
    x = r * x + xCenter
    y = r * y + yCenter
    z = r * z + zCenter
    return (x, y, z)

def plot(ship, planets):

    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
    ax.set_xlabel('X km')
    ax.set_ylabel('Y km')
    ax.set_zlabel('Z km')
    ax.set_xlim3d(-500000, 500000)
    ax.set_ylim3d(-500000, 500000)
    ax.set_zlim3d(-500000, 500000)

    ax.plot(xs = ship.trajectory[0][0::10], ys = ship.trajectory[1][0::10], zs = ship.trajectory[2][0::10], zdir = 'z', label = 'ys=0, zdir=z')

    #Planet Trajectory
    for planet in planets:
        ax.plot(xs = planet.trajectory[0], ys = planet.trajectory[1], zs = planet.trajectory[2], zdir = 'z', label = 'ys=0, zdir=z'))

    (xs, ys, zs) = drawSphere(0, 0, 0, 6367.4447)
    ax.plot_wireframe(xs, ys, zs, color = "r")

    plt.show()

@profile
def runSimulation(startTime, endTime, step, ship, planets):
    
    #Calculate Moon and Planet rate of update
    planetStepRate = int(math.ceil(((endTime - startTime) / step) / 100))

    #Initialize Planets Positions
    for planet in planets:
        planet.updatePosition(startTime)
        planet.logPosition()

    start  = t.time()
    totalTime = endTime - startTime

    #Total Tics
    totalSteps = int((endTime - startTime) / step)

    print("Days in Simulation: {:6.2f}, number of steps: {}".format(totalTime, totalSteps))

    for i, time in enumerate(np.arrange(startTime, endTime, step)):

        #Planet stepRate estimation update
        if (i % planetStepRate == 0):
            for planet in planets[1:]:
                planet.updatePosition(time)
                planet.logPosition()

        #Ship Velocity and Force Vectors (relating to planets)
        for planet in planets:
            ship.forceG(planet)

        #Ship Position (update) according to affecting forces
        ship.update()

        #Ship Position Log
        if(i % 1000) == 0:
            ship.log()

        #Print Position Updates
        if(i % 100000) == 0:
            if t.time() - start > 1:
                timeSinceStart = time - startTime

                #Calculate Time Left
                remainingDays = endTime - time
                remainingPercentage = (1 = timeSinceStart / totalTime)

                #Tics Per Second
                stepsPerSecond = int(math.ceil( i / (t.time() - start)))
                #Remaining Seconds
                remainingSeconds = (totalSteps - i) / stepsPerSecond

                #Convert Reamining Time From Seconds
                minutes, seconds = divmod(remainingSeconds, 60)
                hours, minutes = divmod(minutes, 60)
                print(" Simulation remaining: {:6.2f} days, {:5.2f}%.  Script statistics - steps/s: {:6}, est. time left: {:0>2}:{:0>2}:{:0>2}".format(remainingDays, remainingPercentage, stepsPerSecond, hours, minutes, seconds))

    end = t.time()
    timeElapsed = end - start 
    print("Final Steps/Second: {0:.2f}".format((totalTime / step) / timeElapsed))

    minutes, seconds = divmod(timeElapsed, 60)
    hours, minutes = divmod(minutes, 60)
    print("Total running time: {:0>2.0f}:{:0>2.0f}:{:0>2.0f}".format(hours, minutes, seconds))

def main():
    #DeltaT (in Days) for simulations
    detla_t = np.longdouble(1.0) / (24.0 * 60.0 * 60.0)

    ship = #INSERT SHIP DATA

    #Initialize Simulation
    simulationStart = Time('')
    simulationEnd = Time('')

    if not os.path.isfile('de430.bsp'):
        raise ValueError('de430.bsp Was not found!')
    kernel = SPK.open('de430.bsp')

    planets = #[INSERT PLANET DATA]

    runSimulation(simulationStart.jd, simulationEnd.jd, delta_t, ship, planets)
    plot(ship, [planets[1]])

if __name__ == "__main__":
    main()