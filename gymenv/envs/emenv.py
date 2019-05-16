import gym
from gym import error, spaces, utils
from gym.utils import seeding
from sympy import *
import numpy as np

def angle_normalize(x):
        return (((x+np.pi) % (2*np.pi)) - np.pi)


class emenv(gym.Env):  
    metadata = {'render.modes': ['human']}   
    def __init__(self):
        self.dt=.05
        self.viewer = None
        self.state = np.zeros(3)
 
    def step(self, u):
        x1, x2, x3 = self.state
        J = 1.625e-3
        ro = 0.02
        l = 0.3
        R = 5.0
        L = 25e-3
        m0 = 0.45
        m1 = 0.5
        G = 9.81
        B0 = 16.25e-3
        Kt = 0.9
        Kb = 0.9
        
        dt = self.dt
        M = (J + m1*(l**2)/3 + m0*(l**2) + 2*m0*(ro**2)/5)/Kt
        N = (m1*l*G/(2*Kt)) + (m0*l*G/Kt)
        c0 = 1/L
        c1 = -Kb/L
        c2 = -R/L
        B = B0/Kt
        v1 = 1/M
        v2 = -N/M
        
        newx1 = x1 + x2 * dt
        newx2 = x2 + (v1*x3 + v2*np.sin(x1) + B*v1*x2) * dt
        newx3 = x3 + (c0*u + c1*x2 + c2*x3) * dt
        
        y = newx1
        
        self.state = [newx1, newx2, newx3]
        return self.state#angle_normalize(y) #self._get_obs()
 

    def _get_obs(self):
        x1, x2, x3 = self.state
        return x1 
    
    def reset(self):
        self.state = np.array([0, 0, 0])
 
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
        self.pole_transform.set_rotation(self.state[0] - np.pi/2) 
        #if self.last_u:
        #    self.imgtrans.scale = (-self.last_u/2, np.abs(self.last_u)/2)

        return self.viewer.render(return_rgb_array = mode=='rgb_array')
    
    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None
    