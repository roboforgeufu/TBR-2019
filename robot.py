from pybricks.ev3devices import Motor, ColorSensor
from pybricks.tools import wait, print

import constants as const

class Robot():

    def __init__(self, lmport, rmport, clport, csport):
        
        self.lmotor = Motor(lmport)
        self.rmotor = Motor(rmport)
        self.claw = Motor(clport)
        self.recog = ColorSensor(csport)

    def foward(self):
        pass

    def catch(self, release = False):
        print('Catching...')
        self.claw.run((-1 if release else 1) * const.CLAW_SP)
        wait(const.CLAW_WT)


