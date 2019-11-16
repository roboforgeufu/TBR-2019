#!/usr/bin/env pybricks-micropython

import os
import signal
import threading

from pybricks import ev3brick as brick
from pybricks.parameters import Button, Port, SoundFile
from pybricks.tools import print, wait

from robot import Robot


# TODO: ARTHUR FAZER CONVERSÃO GRAUS -> CM



def test_catch(robot):
    robot.catch()
    wait(1000)
    robot.catch(release = True)

def test_walk_base(robot):
    print('Walking ahead')
    robot.walk2(200, 0)
    wait(1000)
    robot.stop()

    print('Going back...')
    robot.walk2(-200, 0)
    wait(1000)
    robot.stop()

def test_walk(robot):
    print('Walking ahead')
    robot.walk(aFuncao = -0.04, bFuncao = 4, cFuncao = 5, graus = 1000, intervOscilacao=5)
    robot.stop()
    wait(1000)

    print('Going back...')
    robot.walk(aFuncao = 0.04, bFuncao = -4, cFuncao = -5, graus = -1000, intervOscilacao=5)
    robot.stop()
    wait(1000)

def test_turn(robot):
    print('Turning 90 deg')
    robot.turn(aFuncao = -0.04, bFuncao = 4, cFuncao = 5, grausCurva = 90)
    robot.stop()
    wait(1000)

    print('Turning 180 deg')
    robot.turn(aFuncao = -0.04, bFuncao = 4, cFuncao = 5, grausCurva = 180)
    robot.stop()
    wait(1000)

def start_robot():
    print('Starting...')
    triton = Robot(Port.A, Port.C, Port.B, Port.S1)
    
    # Code goes here
    test_catch(triton)
    test_walk(triton)
    test_turn(triton)

    print('Goodbye...')
    wait(1000)

def sing():
    print('Singing in the rain...')
    wait(1000)

def shouting():
    while True:
        brick.sound.file(SoundFile.SHOUTING)
        wait(500)

def main ():

    procs = [item.split()[0] for item in os.popen('ps -e').read().splitlines()[4:] if 'pybricks-micropython' in item.split()]
    for proc in procs:
        if proc != os.getpid():
            os.kill(proc, signal.SIGTERM)

    brick.sound.beep()
    shout = threading.Thread(target = shouting)
    shout.start()

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