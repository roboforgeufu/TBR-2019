#!/usr/bin/pybricks-micropython
# -*- coding: utf-8 -*-

"""Main module."""

# Imports
import os
import time
import signal

from pybricks import ev3brick as brick
from pybricks.parameters import Button, Port, Color, Stop
from pybricks.tools import print, wait, StopWatch

import constants as const
from robot import Robot


# Utils
# TODO: ARTHUR FAZER CONVERSÃO GRAUS -> CM


# Tests TODO: ARQUIVO SEPARADO
def main_testes(robot):
    """Main para testes"""
    for n in range(4):
        A = StopWatch()
        robot.turn(aFuncao=const.aT90_L, bFuncao=const.bT90_L, cFuncao=const.cT90_L, grausCurva=90)
        robot.stop()
        robot.walk(aFuncao=const.aRETA, bFuncao=const.bRETA, cFuncao=const.cRETA, graus=const.MEIO_PEQUENO, intervOscilacao=15)
        robot.stop()
        print(A.time())
    """
    robot.corner = const.BLACK_CNR
    leave_base(robot)
    get_deliver(robot)"""

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
    motor_angle = 0
    robot.resetMotors()
    identificado = False
    while not identificado:
        print(robot.infra.distance())
        robot.align(vInicial=300, intervOscilacao=8)
        motor_angle +=  robot.lmotor.angle()
        robot.resetMotors()
        while robot.lmotor.angle() < const.SEEK_DG:
            robot.equilib(velocidade=const.SEEK_SP)
            print(robot.infra.distance())
            if robot.infra.distance() < const.DST_BIGBLOCK:
                identificado = True
                robot.stop()
                break
    motor_angle += robot.lmotor.angle()
    robot.walk(cFuncao=-20, graus=const.BCK_SEEN, intervOscilacao=8)
    robot.stop()
    robot.turn(aFuncao=const.aT90_L, bFuncao=const.bT90_L, cFuncao=const.cT90_L, grausCurva=90)
    robot.stop()
    
    # print("MotorAngle =", motor_angle)
    if motor_angle < 400:
        #Parou no primeiro cubo
        return 1
    elif motor_angle < 800:
        #Parou no segundo cubo
        return 2
    else:
        #Parou no terceiro cubo
        return 3

def change_sides():
    """Atravessa o campo."""
    # TODO: implementar


def deliver(robot):
    """Faz a entrega do bloco."""
    # VERSAO DE TESTE
    robot.align(vInicial=200)
    robot.stop()
    robot.catch(release=True)
    robot.walk(cFuncao=-30, graus=-100)
    robot.stop()

def get_block(robot):
    """Se aproxima do bloco, le a cor, pega com a garra"""
    robot.resetMotors()
    while robot.central.rgb()[1] < const.GREEN_CLOSE:
        robot.equilib(velocidade=100, intervOscilacao=8)
    robot.stop()
    rgb = robot.central.rgb()
    if rgb[0] > 50:
        return const.RED
    robot.walk(cFuncao=-20, graus=const.REV_CATCH, intervOscilacao=8)
    robot.stop()
    robot.catch(release=True)
    robot.walk(cFuncao=40, graus=const.FWD_CATCH, intervOscilacao=8)
    robot.stop()
    robot.catch()
    if rgb[2] > 20:
        return const.BLUE
    else:
        return const.BLACK

def goto_base():
    """Retorna para a base."""
    # TODO: implementar
    # Deixar o mais geral possível, pode ser usado depois de deliver ou seek


def get_first(robot):
    """Função inicial. Coleta o primeiro bloco no centro do campo."""
    # TODO: Melhorar funcoes das linhas retas e das curvas

    # Andar/Alinhar com a base
    robot.align()

    robot.turn(aFuncao=const.aCURVA45, bFuncao=const.bCURVA45, cFuncao=const.cCURVA45, grausCurva=45)
    
    # Andar fixo
    robot.walk(aFuncao = const.aRETA, bFuncao = const.bRETA, cFuncao=const.cRETA, graus=600, intervOscilacao=const.intRETA)
    robot.stop()

    # Curva
    robot.turn(aFuncao=const.aCURVA45, bFuncao=const.bCURVA45, cFuncao=const.cCURVA45, grausCurva=45)
    robot.stop()

    # Andar fixo
    robot.walk(aFuncao=const.aRETA, bFuncao=const.bRETA, cFuncao=const.cRETA, graus=550, intervOscilacao=const.intRETA)
    robot.stop()

    # Andar/Alinhar com a linha do meio
    robot.align(vInicial=300)
    robot.stop()
    robot.walk(bFuncao=-0.1, cFuncao=30, graus=15, intervOscilacao=8)
    robot.stop()

    # Curva
    robot.turn(aFuncao=const.aT90_L, bFuncao=const.bT90_L, cFuncao=const.cT90_L, grausCurva=90, fix=True)
    robot.stop()

    # Andar/Alinha
    robot.align(vInicial=300)
    robot.stop(Stop.HOLD)

    #Pega o bloco
    corLida = get_block(robot)

    # Entrega
    if robot.corner == corLida:
        # Se move pra tras
        robot.walk(aFuncao = -0.01, bFuncao = 1, cFuncao=60, graus=100, intervOscilacao=8)
        robot.turn(aFuncao=0, bFuncao=0.5, cFuncao=-80, grausCurva=180, fix = True)
        robot.align(vInicial=300)
        robot.walk(aFuncao = -0.01, bFuncao = 1, cFuncao=40, graus=const.MEIO_PEQUENO)
    else:
        # Se move pra frente
        robot.align(vInicial=300)
        robot.walk(aFuncao = -0.01, bFuncao = 1, cFuncao=40, graus=const.MEIO_PEQUENO)
    robot.stop(Stop.HOLD)
    deliver(robot)
    robot.fast_catch()
    robot.deposit[corLida-1][1] = True

def get_deliver(robot):
    """Pega um cubo do canto e entrega"""
    blocoParada = seek_block(robot)
    corLida = get_block(robot)
    if corLida == const.RED:
        """Ignora o vermelho"""
        while robot.lmotor.angle() > -10:
            robot.equilib(velocidade=-200, intervOscilacao=15)
        robot.stop()
        robot.turn(aFuncao=const.aT90_R, bFuncao=const.bT90_R, cFuncao= const.cT90_R, grausCurva=90)
        get_deliver(robot)
    else:
        # TODO: Calcular o tamanho da re baseado nos depositos ocupados

        cor_idx = corLida -1
        if robot.corner == const.BLACK:
            direcao = 1
        else:
            direcao = -1
        n_re = 1 #Valor multiplicador para o robo ir de re ate ficar na direcao do deposito
        for idx in range(len(robot.deposit[cor_idx]))[::direcao]:
            if not robot.deposit[cor_idx][idx]:
                break
            n_re += 1
        robot.deposit[cor_idx][idx] = True
        
        robot.walk(aFuncao=-const.aRETA, bFuncao=-const.bRETA, cFuncao=-const.cRETA, graus=(n_re*const.BACK_DEPOSIT)+300)
        
        if blocoParada == 1:
            if robot.corner == corLida:
                print("CASO 1")
                robot.turn(aFuncao=const.aT90_L, bFuncao=const.bT90_L, cFuncao=const.cT90_L, grausCurva=90)
                robot.align(vInicial=-300, vPosterior=-100)
                robot.walk(aFuncao=const.aRETA, bFuncao=const.bRETA, cFuncao=const.cRETA, graus= const.MEIO_PEQUENO, intervOscilacao=const.intRETA, insideReset=True)
                robot.stop(stop_type=Stop.HOLD)
            else:
                print("CASO 2")
                robot.turn(aFuncao=const.aT90_R, bFuncao=const.bT90_R, cFuncao=const.cT90_R, grausCurva=90)
                robot.align(vInicial=-300, vPosterior=-100)
                robot.walk(aFuncao=const.aRETA, bFuncao=const.bRETA, cFuncao=const.cRETA, graus= const.MEIO_GRANDE, intervOscilacao=const.intRETA, insideReset=True)
                robot.stop(stop_type=Stop.HOLD) 
        elif blocoParada == 2:
            if robot.corner == corLida:
                print("CASO 3")
                robot.turn(aFuncao=const.aT90_L, bFuncao=const.bT90_L, cFuncao=const.cT90_L, grausCurva=90)
                robot.align(vInicial=-300, vPosterior=-100)
                robot.walk(aFuncao=const.aRETA, bFuncao=const.bRETA, cFuncao=const.cRETA, graus= const.MEIO_GRANDE, intervOscilacao=const.intRETA, insideReset=True)
                robot.stop(stop_type=Stop.HOLD)
            else:
                print("CASO 4")
                robot.turn(aFuncao=const.aT90_R, bFuncao=const.bT90_R, cFuncao=const.cT90_R, grausCurva=90)
                robot.align(vInicial=-300, vPosterior=-100)
                robot.walk(aFuncao=const.aRETA, bFuncao=const.bRETA,cFuncao=const.cRETA, graus= const.MEIO_PEQUENO, intervOscilacao=const.intRETA, insideReset=True)
                robot.stop(stop_type=Stop.HOLD)
        else:
            if robot.corner == corLida:
                print("CASO 5")
                robot.turn(aFuncao=const.aT90_L, bFuncao=const.bT90_L, cFuncao=const.cT90_L, grausCurva=90)
                robot.align(vInicial=300, vPosterior=100)
                robot.walk(aFuncao=const.aRETA, bFuncao=const.bRETA, cFuncao=const.cRETA, graus= const.MEIO_GRANDE, intervOscilacao=const.intRETA, insideReset=True)
                robot.stop(stop_type=Stop.HOLD)
            else:
                print("CASO 6")
                robot.turn(aFuncao=const.aT90_R, bFuncao=const.bT90_R, cFuncao=const.cT90_R, grausCurva=90)
        
        robot.stop(Stop.HOLD)
        deliver(robot)
        robot.fast_catch()


def leave_base(robot):
    robot.align()
    robot.lmotor.reset_angle(0)
    while robot.lmotor.angle() < 500:
        robot.lmotor.run(800)
        robot.rmotor.run(200)
    while robot.lmotor.angle() < 600:
        robot.equilib()
    robot.rmotor.reset_angle(0)
    while robot.rmotor.angle() < 500:
        robot.rmotor.run(800)
        robot.lmotor.run(200)
    robot.stop()

# Main
def start_robot(robot):
    """Começa o desafio a partir da base."""
    print("Starting...")

    #Trava a garra no topo
    robot.catch()
    
    if robot.run == 0:
        get_first(robot)
    else:
        leave_base(robot)
        get_deliver(robot)

    robot.run += 1
    print(robot.deposit)
    print("Goodbye...")


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

    """Instancia o robo, comeca o desafio"""
    triton = Robot(lmport = Port.A, rmport = Port.C, clport = Port.B, amport = Port.D, csport = Port.S1, lcport = Port.S2, rcport = Port.S3, infraport = Port.S4)
    
    
    while True:
        while not any(brick.buttons()):
            wait(10)

        buttons = brick.buttons()
        try:
            # Botão do meio -> Começando do lado preto
            if Button.CENTER in buttons:
                print(">>", triton.run)
                triton.corner = const.BLACK_CNR
                start_robot(triton)
            # Botão de cima -> Começando do lado azul
            elif Button.UP in buttons:
                print(">>", triton.run)
                triton.corner = const.BLUE_CNR
                start_robot(triton)
            # Botao da esquerda -> Main de testes
            elif Button.LEFT in buttons:
                print(">> TESTE")
                main_testes(triton)
            # Botão de baixo -> Sair
            elif Button.DOWN in buttons:
                break

        except Exception as ecp:
            print("Fatal Error: %s" % ecp)


if __name__ == "__main__":
    main()
