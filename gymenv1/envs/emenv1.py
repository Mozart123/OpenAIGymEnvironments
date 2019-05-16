import gym
from gym import error, spaces, utils
from gym.utils import seeding
from sympy import *
import numpy as np

def angle_normalize(x):
        return (((x+np.pi) % (2*np.pi)) - np.pi)

class emenv1(gym.Env):  
    metadata = {'render.modes': ['human']}   
    def __init__(self):
        #self.dt=.05
        self.viewer = None
        self.theta1 = None
 
    def step(self, u):
        x1, x2 = self.state
        dt = self.dt
        print('dsfsdgf')
        #k1, k2 are constants based on the link length,
        #mass of the link, gravitational acceleration
        
        #theta1 is the unknown non-linear damping coeff.
        k1 = 10
        k2 = 0.5
        self.theta1 = 2.4 #becomes 4 in paper after 6th second.
        
        newx1 = x1 + x2 * dt
        newx2 = x2 + (-k1 * np.cos(x1) + k2*u - self.theta1 * x2**3) * dt
        x_new = np.zeros((2,1))
        x_new[0] = newx1
        x_new[1] = newx2
        self.state = x_new
        return angle_normalize(x_new) #self._get_obs()
 

    def _get_obs(self):
        x1, x2 = self.state
        return x1 
    
    def reset(self):
        self.state = np.array([-np.pi/2, 0])
 
    def render(self, mode='human'):
        if self.viewer is None:
            from gym.envs.classic_control import rendering
            self.viewer = rendering.Viewer(500,500)
            self.viewer.set_bounds(-2.2,2.2,-2.2,2.2)
            rod = rendering.make_capsule(1, .1)
            rod.set_color(.8, .3, .3)
            self.pole_transform = rendering.Transform()
            rod.add_attr(self.pole_transform)
            self.viewer.add_geom(rod)
            axle = rendering.make_circle(.05)
            axle.set_color(0,0,0)
            self.viewer.add_geom(axle)
            #fname = path.join(path.dirname(__file__), "assets/clockwise.png")
            #self.img = rendering.Image(fname, 1., 1.)
            #self.imgtrans = rendering.Transform()
            #self.img.add_attr(self.imgtrans)

        #self.viewer.add_onetime(self.img)
        self.pole_transform.set_rotation(self.state[0])
        #if self.last_u:
        #    self.imgtrans.scale = (-self.last_u/2, np.abs(self.last_u)/2)

        return self.viewer.render(return_rgb_array = mode=='rgb_array')
    
    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None
    
