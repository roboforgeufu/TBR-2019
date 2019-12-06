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

f = open("log.txt", "a")

# Utils
# TODO: ARTHUR FAZER CONVERSÃO GRAUS -> CM


# Tests TODO: ARQUIVO SEPARADO
def main_testes(robot):
    """Main para testes"""
    robot.corner = 1
    leave_base(robot)
    print(seek_block(robot))
    print(robot.seek_distance)

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
    f.write("Checking...\n")
    identificado = False
    blocoParada = 0

    if robot.seek_distance[robot.corner -1] > 100:
        robot.align()
        robot.walk(aFuncao=const.aRETA, bFuncao=const.bRETA, cFuncao=const.cRETA, graus=robot.seek_distance[robot.corner -1]-200, intervOscilacao=const.intRETA)
        robot.stop()
    while not identificado:
        print("Bloco Parada =", blocoParada)
        print("Infra >>", robot.infra.distance())
        f.write("STAGE%d\n" % blocoParada)
        robot.align(vInicial=300, intervOscilacao=8)
        robot.seek_distance[robot.corner -1] +=  robot.lmotor.angle()
        robot.resetMotors()
        while robot.lmotor.angle() < const.SEEK_DG:
            print("Infra >>", robot.infra.distance())
            robot.equilib(velocidade=const.SEEK_SP)
            # print(robot.infra.distance())
            f.write("InfraRed %d\n" % robot.infra.distance())
            if robot.infra.distance() < const.DST_BIGBLOCK:
                identificado = True
                robot.stop()
                break
        if robot.seek_distance[robot.corner -1] < const.SEEK_DST_1:
            #Primeiro cubo
            blocoParada = 1
        elif robot.seek_distance[robot.corner -1] < const.SEEK_DST_2:
            #Segundo cubo
            blocoParada = 2
        elif robot.seek_distance[robot.corner -1] < const.SEEK_DST_3:
            #Terceiro cubo
            blocoParada = 3
        else:
            #Quarto cubo
            blocoParada = 4
            print("Nada ainda...")

    robot.seek_distance[robot.corner -1] += robot.lmotor.angle()
    robot.walk(cFuncao=-20, graus=const.BCK_SEEN, intervOscilacao=8)
    robot.stop()
    robot.turn(aFuncao=const.aT90_L, bFuncao=const.bT90_L, cFuncao=const.cT90_L, grausCurva=90)
    robot.stop()
    
    f.write("SAIDA >> Bloco parada:%d\n" % blocoParada)
    return blocoParada

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
        f.write("RETURN BLUE\n")
        return const.BLUE
    else:
        f.write("RETURN BLUE\n")
        return const.BLACK

def goto_base():
    """Retorna para a base."""
    # TODO: implementar
    # Deixar o mais geral possível, pode ser usado depois de deliver ou seek


def get_first(robot):
    """Função inicial. Coleta o primeiro bloco no centro do campo."""
    # Andar/Alinhar com a base
    robot.align()

    robot.turn(aFuncao=const.aCURVA45, bFuncao=const.bCURVA45, cFuncao=const.cCURVA45, grausCurva=45)
    
    # Andar fixo
    robot.walk(aFuncao = const.aRETA, bFuncao = const.bRETA, cFuncao=const.cRETA, graus=650, intervOscilacao=const.intRETA)
    robot.stop()

    # Curva
    robot.turn(aFuncao=const.aCURVA45, bFuncao=const.bCURVA45, cFuncao=const.cCURVA45, grausCurva=40)
    robot.stop()

    # Andar fixo
    robot.walk(aFuncao=const.aRETA, bFuncao=const.bRETA, cFuncao=const.cRETA, graus=500, intervOscilacao=const.intRETA)
    robot.stop()

    # Andar/Alinhar com a linha do meio
    robot.align(vInicial=300)
    robot.stop()
    robot.walk(bFuncao=-0.1, cFuncao=30, graus=35, intervOscilacao=8)
    robot.stop()

    # Curva
    robot.turn(aFuncao=const.aT90_L, bFuncao=const.bT90_L, cFuncao=const.cT90_L, grausCurva=90, fix=True)
    robot.stop()

    # Andar/Alinha
    robot.align(vInicial=300)
    robot.stop(Stop.HOLD)

    #Pega o bloco
    corLida = get_block(robot)
    robot.map[2][0] = corLida

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
    robot.map[robot.corner -1][blocoParada -1] = corLida
    if corLida == const.RED:
        """Ignora o vermelho"""
        while robot.lmotor.angle() > -10:
            robot.equilib(velocidade=-200, intervOscilacao=6)
        robot.stop()
        robot.turn(aFuncao=const.aT90_R, bFuncao=const.bT90_R, cFuncao= const.cT90_R, grausCurva=90)
        get_deliver(robot)
    else:
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
                f.write("CASO 1\n")
                robot.turn(aFuncao=const.aT90_L, bFuncao=const.bT90_L, cFuncao=const.cT90_L, grausCurva=90)
                robot.align(vInicial=-300, vPosterior=-100)
                robot.walk(aFuncao=const.aRETA, bFuncao=const.bRETA, cFuncao=const.cRETA, graus= const.MEIO_PEQUENO, intervOscilacao=const.intRETA, insideReset=True)
                robot.stop(stop_type=Stop.HOLD)
            else:
                print("CASO 2")
                f.write("CASO 2\n")
                robot.turn(aFuncao=const.aT90_R, bFuncao=const.bT90_R, cFuncao=const.cT90_R, grausCurva=90)
                robot.align(vInicial=-300, vPosterior=-100)
                robot.walk(aFuncao=const.aRETA, bFuncao=const.bRETA, cFuncao=const.cRETA, graus= const.MEIO_GRANDE, intervOscilacao=const.intRETA, insideReset=True)
                robot.stop(stop_type=Stop.HOLD) 
        elif blocoParada == 2:
            if robot.corner == corLida:
                print("CASO 3")
                f.write("CASO 3\n")
                robot.turn(aFuncao=const.aT90_L, bFuncao=const.bT90_L, cFuncao=const.cT90_L, grausCurva=90)
                robot.align(vInicial=-300, vPosterior=-100)
                robot.walk(aFuncao=const.aRETA, bFuncao=const.bRETA, cFuncao=const.cRETA, graus= const.MEIO_GRANDE, intervOscilacao=const.intRETA, insideReset=True)
                robot.stop(stop_type=Stop.HOLD)
            else:
                print("CASO 4")
                f.write("CASO 4\n")
                robot.turn(aFuncao=const.aT90_R, bFuncao=const.bT90_R, cFuncao=const.cT90_R, grausCurva=90)
                robot.align(vInicial=-300, vPosterior=-100)
                robot.walk(aFuncao=const.aRETA, bFuncao=const.bRETA,cFuncao=const.cRETA, graus= const.MEIO_PEQUENO, intervOscilacao=const.intRETA, insideReset=True)
                robot.stop(stop_type=Stop.HOLD)
        else:
            if robot.corner == corLida:
                print("CASO 5")
                f.write("CASO 5\n")
                robot.turn(aFuncao=const.aT90_L, bFuncao=const.bT90_L, cFuncao=const.cT90_L, grausCurva=90)
                robot.align(vInicial=300, vPosterior=100)
                robot.walk(aFuncao=const.aRETA, bFuncao=const.bRETA, cFuncao=const.cRETA, graus= const.MEIO_GRANDE, intervOscilacao=const.intRETA, insideReset=True)
                robot.stop(stop_type=Stop.HOLD)
            else:
                print("CASO 6")
                f.write("CASO 6\n")
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
    while robot.lmotor.angle() < 540:
        robot.equilib()
    robot.rmotor.reset_angle(0)
    while robot.rmotor.angle() < 530:
        robot.rmotor.run(800)
        robot.lmotor.run(200)
    robot.stop()
    robot.resetMotors()

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
    f.write("DEPOSITOS\n")
    for depositos in robot.deposit:
        f.write(">>\n")
    #    f.writelines(["%s " % item  for item in depositos])


    print(robot.map)
    f.write("MAP\n")
    for minimap in robot.map:
        f.write(">>\n")
    #    f.writelines(["%d " % item  for item in minimap])


    print(robot.seek_distance)
    f.write("SEEK_DISTANCE\n")
    #f.writelines(["%d " % item  for item in robot.seek_distance])
    
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
                f.write(">>%d\n" % triton.run)
                triton.corner = const.BLACK_CNR
                start_robot(triton)
            # Botão de cima -> Começando do lado azul
            elif Button.UP in buttons:
                print(">>", triton.run)
                f.write(">>%d\n" % triton.run)
                triton.corner = const.BLUE_CNR
                start_robot(triton)
            # Botao da esquerda -> Main de testes
            elif Button.LEFT in buttons:
                print(">> TESTE")
                f.write(">>%d\n" % triton.run)
                main_testes(triton)
            # Botão de baixo -> Sair
            elif Button.DOWN in buttons:
                break

        except Exception as ecp:
            print("Fatal Error: %s" % ecp)
            f.write("Fatal Error: %s\n" % ecp)


if __name__ == "__main__":
    main()

f.close()