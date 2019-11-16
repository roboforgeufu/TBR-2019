#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.parameters import Button, Port
from pybricks.tools import print, wait

from robot import Robot

def test_catch(robot):
    triton.catch()
    wait(1000)
    triton.catch(release = True)

def start_robot():
    print('Starting...')
    triton = Robot(Port.A, Port.C, Port.B, Port.S1)
    
    # Code goes here
    test_catch(triton)

    print('Goodbye...')
    wait(10000)

def sing():
    print('Singing in the rain...')
    wait(1000)

def main ():

    while True:
        while not any(brick.buttons()):
            wait(10)
        
        buttons = brick.buttons()
        if Button.CENTER in buttons:
            try:
                start_robot()    
            except Exception as ecp:
                print('Fatal Error: %s' %ecp)
        elif Button.UP in buttons:
            sing()
        elif Button.DOWN in buttons:
            break


if __name__ == "__main__":
    main()