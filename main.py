#!/usr/bin/env pybricks-micropython
# -*- coding: utf-8 -*-

"""Main module."""

# Imports
import os
import time
import signal

from pybricks import ev3brick as brick
from pybricks.parameters import Button, Port, Color, Stop
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
def seek_block(robot):
    """Segue em linha reta até perceber a presença de um bloco grande."""
    print("Checking...")
    robot.resetMotors()
    identificado = False
    while not identificado:
        print(robot.infra.distance())
        robot.align(velocidade=500, intervOscilacao=8)
        robot.resetMotors()
        while robot.lmotor.angle() < 300:
            robot.equilib(velocidade=100)
            print(robot.infra.distance())
            if robot.infra.distance() < 10:
                identificado = True
                robot.stop()
                break
    robot.central.ambient()
    robot.walk(cFuncao=-20, graus=const.BCK_SEEN, intervOscilacao=8)
    robot.stop()
    robot.turn(aFuncao=0.04, bFuncao=-4, cFuncao=-20, grausCurva=92)
    robot.stop()
    robot.resetMotors()
    while robot.central.rgb()[1] < const.GREEN_CLOSE:
        robot.equilib(velocidade=150, intervOscilacao=8)
    robot.stop()
    rgb = robot.central.rgb()
    robot.walk(cFuncao=-20, graus=const.REV_CATCH, intervOscilacao=8)
    robot.stop()
    robot.catch(release=True)
    robot.walk(cFuncao=40, graus=const.FWD_CATCH, intervOscilacao=8)
    robot.stop()
    robot.catch()
    if rgb[0] > 50:
        return const.RED
    elif rgb[2] > 20:
        return const.BLUE
    else:
        return const.BLACK


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
    robot.align(velocidade=100)

    # Andar fixo
    robot.walk(cFuncao=40, graus=690, intervOscilacao=8)
    robot.stop()

    # Curva
    robot.turn(aFuncao=0, bFuncao=0, cFuncao=30, grausCurva=90)
    robot.stop()

    # Andar fixo
    robot.walk(cFuncao=40, graus=1300, intervOscilacao=8)
    robot.stop()

    # Andar/Alinhar com a linha do meio
    robot.align(velocidade=100)

    robot.walk(cFuncao=40, graus=60, intervOscilacao=8)
    robot.stop()

    # Curva
    robot.turn(aFuncao=0, bFuncao=0, cFuncao=-30, grausCurva=90)
    robot.stop()

    # Andar/Alinha com o quadrado vermelho
    robot.align(velocidade=200)
    robot.align(Color.RED, 100)

    # Manobra para ler a cor do bloco
    robot.walk(cFuncao=-40, graus=-100, intervOscilacao=8)
    robot.turn(aFuncao=0, bFuncao=0, cFuncao=30, grausCurva=90)
    
    wait(1000)
    
    # Manobra pra pegar o bloco
    robot.turn(aFuncao=0, bFuncao=0, cFuncao=-30, grausCurva=90)
    robot.walk(cFuncao=40, graus=100, intervOscilacao=8)
    robot.stop()

    #Programe a garra aqui

    ValorLido = Color.BLACK
    # Entrega
    if robot.corner == ValorLido:
        # Se move pra tras
        robot.walk(cFuncao=40, graus=100, intervOscilacao=8)
        robot.turn(aFuncao=0, bFuncao=0, cFuncao=-30, grausCurva=180)
        robot.align(velocidade=200)
        robot.walk(cFuncao=40, graus=1000)
        robot.align(velocidade=200)
        robot.stop()
    else:
        # Se move pra frente
        robot.align(velocidade=200)
        robot.walk(cFuncao=40, graus=1000)
        robot.align(velocidade=100)
        robot.stop()

def deliver_first(robot):
    """Entrega o primeiro cubo."""
    pass

def get_deliver(robot):
    """Pega um cubo do canto e entrega"""
    corLida = seek_block(robot)
    if corLida != const.RED:
        n_re = 1 #Valor multiplicador para o robo ir de re ate ficar na direcao do deposito
        robot.walk(aFuncao=0.04, bFuncao=-4, cFuncao=-5, graus=n_re*-450)
        if corLida == robot.corner:
            robot.turn(aFuncao=-0.04, bFuncao=4, cFuncao=5, grausCurva=90)
        else:
            robot.turn(aFuncao=0.04, bFuncao=-4, cFuncao=-5, grausCurva=90)
        robot.stop()
        robot.align(velocidade=-300)


# Main
def start_robot(corner):
    """Instacia a classe, começa o desafio."""
    print("Starting...")

    triton = Robot(lmport = Port.A, rmport = Port.C, clport = Port.B, amport = Port.D, csport = Port.S1, lcport = Port.S2, rcport = Port.S3, infraport = Port.S4, corner = corner)
    #Trava a garra no topo
    triton.catch()

    # Tests.
    # test_catch(triton)
    # test_walk(triton)
    # test_turn(triton)
    # test_gyro_walk(triton)
    # test_gyro_turn(triton)

    # get_first(triton)
    # deliver_first(triton)

    #get_deliver(triton)]

    triton.align(velocidade = 600, intervOscilacao=8)
    
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
