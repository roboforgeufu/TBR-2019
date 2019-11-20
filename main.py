#!/usr/bin/env pybricks-micropython
# -*- coding: utf-8 -*-

"""Main module."""

# Imports
import os
import signal

from pybricks import ev3brick as brick
from pybricks.parameters import Button, Port
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


def get_first():
    """Função inicial. Coleta o primeiro bloco no centro do campo."""
    # TODO: implementar
    # FIXME: ALTA PRIORIDADE


# Main
def start_robot(corner):
    """Instacia a classe, começa o desafio."""
    print("Starting...")

    triton = Robot(Port.A, Port.C, Port.B, Port.D, Port.S1, Port.S2, Port.S3, Port.S4, corner)

    # Tests.
    test_catch(triton)
    test_walk(triton)
    test_turn(triton)

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
        # Botão do meio -> Começando do lado preto
        if Button.CENTER in buttons:
            try:
                start_robot(const.BLACK_CNR)
            except Exception as ecp:
                print("Fatal Error: %s" % ecp)
        # Botão de cima -> Começando do lado azul
        elif Button.UP in buttons:
            try:
                start_robot(const.BLUE_CNR)
            except Exception as ecp:
                print("Fatal Error: %s" % ecp)
        # Botão de baixo -> Sair
        elif Button.DOWN in buttons:
            break


if __name__ == "__main__":
    main()
