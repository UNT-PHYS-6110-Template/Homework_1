#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Assignment 3
The following is a program to simulate the motion of non-interacting particles inside a box
Time is discretized into small intervals (timesteps), during which the motion of the particles follow some simple physical laws
Trajectories of particles are simulated as a sequence of a large number of timesteps
 
Authors: O. Andreussi and STUDENT
"""
# 
# Parameters and variables
# 
#    ntot: number of particles in the simulation
#    dt: lenght of the timestep (in arbitrary units)
#    xbox: size of box along the x axis (in arbitrary units)
#    ybox: size of box along the y axis (in arbitrary units)
#    xpos: x component of particles positions (in arbitrary units)
#    ypos: y component of particles positions (in arbitrary units)
#    xvel: x component of particles velocities (in arbitrary units)
#    yvel: y component of particles velocities (in arbitrary units)
#
# Start by importing useful modules
#
import numpy as np
import matplotlib.animation as ani
import matplotlib.pyplot as plt
#
# Setup simulation parameters
#
ntot=8 # total number of particles
nl0=8 # initial number of particles on the left side of the box
dt=0.005 # this value should be reasonable, but you are free to test larger or smaller values
xbox=1. # when using arbitrary units is a good idea to keep them close to unity
ybox=1. # we start by considering a square box, but you are free to change this parameter as you like
#
# Setup starting configuration of the system
# 
xpos=np.random.uniform(0.,xbox/2,nl0) # this is numpy array with nl0 elements, corresponding to the x-coordinates of the particles on the left side of the box
np.append(xpos,np.random.uniform(xbox/2,xbox,ntot-nl0)) # here we add the x-coordinates of the particles in the right side of the box
ypos=np.random.uniform(0.,ybox,ntot) # this is a numpy array with ntot elements, corresponding to the y-coordinates of the particles. 
# NOTE: initial positions should be inside the [0,ybox] interval. 
xvel=np.random.uniform(-1.,1.,ntot) # this is a numpy array with ntot elements, corresponding to the x-component of the particles's velocities. 
# NOTE: initial velocities are considered to be uniformly distributed inside the [-1.,1.] interval.
yvel=np.random.uniform(-1.,1.,ntot) # this is a numpy array with ntot elements, corresponding to the x-component of the particles's velocities. 
# NOTE: initial velocities are considered to be uniformly distributed inside the [-1.,1.] interval.
#
# The following is the function responsible to describe the motion of a single particle during a short timestep
#
def move(dt,xpos,ypos,xvel,yvel,xbox,ybox):
    """
    This function describes the motion of a single particle subject to no interactions but elastic reflections from the box walls.
    The particle's coordinates will change according to a constant velocity motion. 
    If the position of the particle falls outside of the box walls, the particle's velocity changes sign (reflection).
    Input arguments:
        dt: timestep; xpos/ypos: particle's coordinate along xy; xvel/yvel: x/y-component of particle's velocity; xbox/ybox: lenghts of box.
    Output results:
        updated x and y components of particle's position and velocity
    """
    xpos += dt*xvel
    ypos += dt*yvel
    xvel *= 1-2*((xpos > xbox)+(xpos < 0.0))
    yvel *= 1-2*((ypos > ybox)+(ypos < 0.0))
    return xpos, ypos, xvel, yvel
#
#
#
def checkside(xpos,ypos,xbox,ybox):
    leftx=[]
    lefty=[]
    rightx=[]
    righty=[]
    for i,x in enumerate(xpos):
        if x<xbox/2 :
            leftx.append(xpos[i])
            lefty.append(ypos[i])
        else:
            rightx.append(xpos[i])
            righty.append(ypos[i])
    return leftx,lefty,rightx,righty
#
# The following command setup the visualization of plot, where the particle is represented by a green filled circle
#
leftx,lefty,rightx,righty=checkside(xpos,ypos,xbox,ybox)
fig, axes = plt.subplots(1)
axes.set_xlim(0, xbox) # This statement set the limits for the x-axis of the plot
axes.set_ylim(0, ybox) # This statement set the limits for the y-axis of the plot.
a,=axes.plot(leftx,lefty,'go') # We generate a plot with the starting configuration
b,=axes.plot(rightx,righty,'ro') # We generate a plot with the starting configuration
#
# Define the function that performs a single step of the animation
#
def animate(i):
    global xpos
    global ypos
    global xvel
    global yvel
    xpos,ypos,xvel,yvel=move(dt,xpos,ypos,xvel,yvel,xbox,ybox)
    leftx,lefty,rightx,righty=checkside(xpos,ypos,xbox,ybox)
    a.set_data(leftx,lefty) # update the plot
    b.set_data(rightx,righty) # update the plot
    return a,b
#
# We perform the animation using the FuncAnimation function from the animation module of matplotlib. 
# This function requires as an argument the user-defined animate() function above
#
anim = ani.FuncAnimation(fig, animate, frames=1000, interval=50, blit=True)
#
# If you keep the following lines commented out, the code will only show the animation
# If you uncomment the following lines, the animation will be saved as an mp4 video
#
Writer = ani.writers['ffmpeg']
writer = Writer(fps=20, bitrate=1800)
anim.save('homework1.mp4', writer=writer)