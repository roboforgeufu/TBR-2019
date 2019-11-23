#!/usr/bin/env pybricks-micropython
# -*- coding: utf-8 -*-

"""Main module."""

# Imports
import os
import time
import signal

from pybricks import ev3brick as brick
from pybricks.parameters import Button, Port, Color
from pybricks.tools import print, wait

import constants as const
from robot import Robot


# Utils
# TODO: ARTHUR FAZER CONVERSÃO GRAUS -> CM


# Tests TODO: ARQUIVO SEPARADO
def test_catch(robot):
    """Teste da garra."""
    robot.catch()
    wait(1000)
    robot.catch(release=True)


def test_walk(robot):
    """Teste de andar em linha reta."""
    print("Walking ahead")
    robot.walk(aFuncao=-0.04, bFuncao=4, cFuncao=5, graus=1000, intervOscilacao=5)
    robot.stop()
    wait(1000)

    print("Going back...")
    robot.walk(aFuncao=0.04, bFuncao=-4, cFuncao=-5, graus=-1000, intervOscilacao=5)
    robot.stop()
    wait(1000)


def test_turn(robot):
    """Teste de curva."""
    print("Turning 90 deg")
    robot.turn(aFuncao=-0.04, bFuncao=4, cFuncao=5, grausCurva=90)
    robot.stop()
    wait(1000)

    print("Turning 180 deg")
    robot.turn(aFuncao=-0.04, bFuncao=4, cFuncao=5, grausCurva=180)
    robot.stop()
    wait(1000)


def test_gyro_walk(robot):
    """Teste andar com o giroscópio."""
    robot.gyro_walk(300)

    time.sleep(1000)

    robot.stop()


def test_gyro_turn(robot):
    """Teste curva com gyro"""
    robot.gyro_turn(400, 90)

    time.sleep(1000)

    robot.gyro_turn(400, 180, lturn=True)


# Funções
def seek_block():
    """Segue em linha reta até perceber a presença de um bloco."""
    # TODO: implementar


def change_sides():
    """Atravessa o campo."""
    # TODO: implementar


def deliver():
    """Faz a entrega do bloco."""
    # TODO: implementar


def goto_base():
    """Retorna para a base."""
    # TODO: implementar
    # Deixar o mais geral possível, pode ser usado depois de deliver ou seek


def get_first(robot):
    """Função inicial. Coleta o primeiro bloco no centro do campo."""
    # TODO: implementar
    # FIXME: ALTA PRIORIDADE

    # Andar/Alinhar com a base
    robot.align(Color.BLACK, 100)

    # Andar fixo
    robot.walk(cFuncao=100, graus=420)
    robot.stop()

    # Curva
    robot.turn(aFuncao=0, bFuncao=0, cFuncao=30, grausCurva=90)
    robot.stop()

    # Andar/Alinhar com a linha do meio
    robot.align(Color.BLACK, 100)

    # Curva
    robot.turn(aFuncao=0, bFuncao=0, cFuncao=30, grausCurva=90)
    robot.stop()

    # Andar/Alinha com o quadrado vermelho
    robot.align(Color.BLACK, 100)


def deliver_first(robot):
    """Entrega o primeiro cubo."""
    pass

# Main
def start_robot(corner):
    """Instacia a classe, começa o desafio."""
    print("Starting...")

    triton = Robot(lmport = Port.A, rmport = Port.C, clport = Port.B, amport = Port.D, csport = Port.S1, lcport = Port.S2, rcport = Port.S3, gyport = Port.S4, corner = corner)

    # Tests.
    # test_catch(triton)
    # test_walk(triton)
    # test_turn(triton)
    # test_gyro_walk(triton)
    # test_gyro_turn(triton)

    get_first(triton)

    print("Goodbye...")
    wait(1000)


def main():
    """Função main."""
    # Mata processos
    procs = [
        item.split()[0]
        for item in os.popen("ps -e").read().splitlines()[4:]
        if "pybricks-micropython" in item.split()
    ]
    for proc in procs:
        if proc != os.getpid():
            os.kill(proc, signal.SIGTERM)

    while True:
        while not any(brick.buttons()):
            wait(10)

        buttons = brick.buttons()
        try:
            # Botão do meio -> Começando do lado preto
            if Button.CENTER in buttons:
                start_robot(const.BLACK_CNR)
            # Botão de cima -> Começando do lado azul
            elif Button.UP in buttons:
                start_robot(const.BLUE_CNR)
            # Botão de baixo -> Sair
            elif Button.DOWN in buttons:
                break
        except Exception as ecp:
            print("Fatal Error: %s" % ecp)


if __name__ == "__main__":
    main()
