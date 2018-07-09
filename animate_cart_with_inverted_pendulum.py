'''
Created on Jul 8, 2018

@author: Austin Owens
'''
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import animation


class AnimateCartWithInvertedPendulum():
    def __init__(self, cartPositionArray, pendulumAngularPositionArray, bobRadius, cartWidth, cartHeight, rodHeight, rodWidth=2.5, block=True):
        '''
        Given position of the cart and angular position of the pendulum (in radians), the show() function will plot the motion of the
        inverted pendulum on the cart.
        '''
        #Create axis object
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        
        #Make axes equal and apply grid
        plt.axis('equal')
        plt.grid()
        
        #Set axis limits
        self.ax.set_xlim(-2, 2)
        self.ax.set_ylim(-2, 2)
        
        #Create patches
        self.circ = patches.Circle((0, 0), bobRadius)
        self.rect = patches.Rectangle((0, 0), cartWidth, cartHeight, fc='g')
        self.line = plt.Line2D((0, 0), (0, 0), lw=rodWidth)
        
        #User params
        self.rodHeight = rodHeight
        self.cartPositionArray = cartPositionArray
        self.pendulumAngularPositionArray = pendulumAngularPositionArray
        self.block = block
        
        #Amount of samples given from cartPositionArray or pendulumAngularPositionArray
        self.samples = min(len(self.cartPositionArray), len(self.pendulumAngularPositionArray))
        
    def init_animate(self):
        
        self.ax.add_patch(self.circ)
        self.ax.add_patch(self.rect)
        self.ax.add_line(self.line)
        
        return self.circ, self.rect, self.line
    
    def animate(self, i):
        
        xRect = self.cartPositionArray[i]-(self.rect.get_width()/2.0)
        yRect = 0-self.rect.get_height()
        self.rect.set_xy([xRect, yRect])
        
        xCirc = (xRect+(self.rect.get_width()/2.0))-math.sin(self.pendulumAngularPositionArray[i])*self.rodHeight
        yCirc = math.cos(self.pendulumAngularPositionArray[i])*self.rodHeight
        self.circ.center = xCirc, yCirc
        #print "Pendulum angle:", self.pendulumAngularPositionArray[i]*(180.0/np.pi)
        
        self.line.set_data((xRect+(self.rect.get_width()/2.0), xCirc), (yRect+self.rect.get_height(), yCirc))
            
        return self.circ, self.rect, self.line
    
    def show(self):
        anim = animation.FuncAnimation(self.fig, self.animate,
                                       init_func=self.init_animate,
                                       frames=self.samples,
                                       interval=1,
                                       blit=True)
        plt.show(block=self.block)
        
        
if __name__ == "__main__":
    bobRadius = 0.025
    cartWidth = 0.3
    cartHeight = 0.1
    rodHeight = 0.3
    
    with open("data.txt", 'r') as f:
        lines = f.readlines()
    
    cartPositionArray = map(float, lines[0].split(", "))
    pendulumAngularPositionArray = map(float, lines[1].split(", "))
    
    AnimateCartWithInvertedPendulum(cartPositionArray, pendulumAngularPositionArray, bobRadius, cartWidth, cartHeight, rodHeight).show()
    
    
