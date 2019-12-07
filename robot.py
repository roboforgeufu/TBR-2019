# -*- coding: utf-8 -*-

"""Robot module."""

from pybricks.ev3devices import Motor, ColorSensor, GyroSensor, InfraredSensor, UltrasonicSensor
from pybricks.tools import wait, print, StopWatch
from pybricks.parameters import Stop
from pybricks.robotics import DriveBase

import constants as const


class Robot:
    """Classe do robo."""

    def __init__(self, lmport, rmport, clport, amport, csport, lcport, rcport, infraport):
        """Inicializa variáveis do robo."""
        self.lmotor = Motor(lmport)
        self.rmotor = Motor(rmport)
        self.claw = Motor(clport)
        # self.arm = Motor(amport)

        self.central = ColorSensor(csport)
        self.lcolor = ColorSensor(lcport)
        self.rcolor = ColorSensor(rcport)
        self.infra = InfraredSensor(infraport)

        self.map = [[const.UNK] * 4, [const.UNK] * 4, [const.UNK]]
        self.deposit = [[False]*3, [False]*3]
        self.side = const.LEFT
        self.direction = const.NORTH
        self.corner = 0
        self.run = 1

        self.stopwatch = StopWatch()

        self.seek_distance = [0, 0]

    def walk(self, aFuncao=0, bFuncao=0, cFuncao=0, graus=0, intervOscilacao=0, insideReset=True):
        """Anda com o robo."""
        # TODO: Deixar velocidade constante.
        print("Walking...")
        if insideReset:
            self.lmotor.reset_angle(0)
            self.rmotor.reset_angle(0)
        velocDir = 0
        velocEsq = 0
        while True:
            print(self.lmotor.angle(), self.rmotor.angle())
            # Funcao que descreve a velocidade em funcao da porcentagem do deslocamento ja realizado
            percDeslocado = (self.lmotor.angle() / graus) * 100
            velocEsq = (aFuncao * (percDeslocado ** 2) + bFuncao * percDeslocado + cFuncao) * 10
            velocDir = velocEsq

            # Teto
            if velocEsq > 900:
                velocEsq = 900
            if velocDir > 900:
                velocDir = 900

            diferenca_EsqDir = abs(self.lmotor.angle()) - abs(self.rmotor.angle())
            if abs(diferenca_EsqDir) > 3:
                if diferenca_EsqDir > 0:
                    # self.lmotor andou mais, joga mais velocidade no self.rmotor
                    velocEsq = velocEsq * (1 - (intervOscilacao / 100))
                    velocDir = velocDir * (1 + (intervOscilacao / 100))
                else:
                    # self.rmotor andou mais, joga mais velocidade no self.lmotor
                    velocEsq = velocEsq * (1 + (intervOscilacao / 100))
                    velocDir = velocDir * (1 - (intervOscilacao / 100))
            self.lmotor.run(velocEsq)
            self.rmotor.run(velocDir)
            if (abs(velocEsq) < 50 and abs(velocDir) < 50) or percDeslocado >= 99:
                break

    def turn(self, aFuncao, bFuncao, cFuncao, grausCurva, fix=True):
        print("Turning...")
        self.lmotor.reset_angle(0)
        self.rmotor.reset_angle(0)

        # P/ calibrar
        K = const.K
        grausMotor = int(K * grausCurva / 90)

        mediaPercorrida = 0
        while mediaPercorrida < 99:
            # Calculo da velocidade de ambos os motores em funcao da media do deslocamento
            # percorrido por cada um
            percPercorridoEsq = (abs(self.lmotor.angle()) / grausMotor) * 100
            percPercorridoDir = (abs(self.rmotor.angle()) / grausMotor) * 100
            mediaPercorrida = (percPercorridoDir + percPercorridoEsq) / 2.0

            velocidade = (
                aFuncao * (mediaPercorrida ** 2) + bFuncao * mediaPercorrida + cFuncao
            ) * 10

            self.lmotor.run(velocidade)
            self.rmotor.run(-velocidade)
        self.lmotor.stop()
        self.rmotor.stop()

        if fix:
            while True:
                # Para o motor Esquerdo:
                difEsq = abs(self.lmotor.angle()) - grausMotor
                #print("DifEsq >>",difEsq, ">>", self.lmotor.angle(), grausMotor)
                if abs(difEsq) > 3:
                    # A diferenca eh consideravel
                    if difEsq > 0:
                        # Andou mais do que devia
                        sinalEsq = -1 *(
                            self.lmotor.angle() / abs(self.lmotor.angle())
                        )  # Deve se movimentar no sentido contrario ao mov anterior
                    else:
                        # Andou menos do que devia
                        sinalEsq = self.lmotor.angle() / abs(
                            self.lmotor.angle()
                        )  # Deve se movimentar no mesmo sentido do movimento anterior
                    velocEsq = sinalEsq * (2 * abs(difEsq) + 50)
                else:
                    # A diferenca eh irrelevante
                    velocEsq = 0

                # Para o motor Direito:
                difDir = abs(self.rmotor.angle()) - grausMotor
                #print("DifDir >>", difDir, ">>", self.rmotor.angle(), grausMotor)
                if abs(difDir) > 3:
                    # A diferenca eh consideravel
                    if difDir > 0:
                        # Andou mais do que devia
                        sinalDir = -1 * (
                            self.rmotor.angle() / abs(self.rmotor.angle())
                        )  # Deve se movimentar no sentido contrario ao mov anterior
                    else:
                        # Andou menos do que devia
                        sinalDir = self.rmotor.angle() / abs(
                            self.rmotor.angle()
                        )  # Deve se movimentar no mesmo sentido do movimento anterior
                    velocDir = sinalDir * (2 * abs(difDir) + 50)
                else:
                    # A diferenca eh irrelevante
                    velocDir = 0

                # Por fim, manda a velocidade calculada para os motores
                self.lmotor.run(velocEsq)
                self.rmotor.run(velocDir)

                # Se qualquer dos motores estiver fora do intervalo
                # seguro, entao ele ainda nao comeca a contar
                if (difDir not in range(-3, 4)) or (difEsq not in range(-3, 4)):
                    self.stopwatch.reset()  # Nao comecar a contar <=> resetar constantemente o self.stopwatch

                #print("Tempo:", self.stopwatch.time(), "\ Vel:", velocDir, velocEsq)
                #print(difDir, difEsq)
                # Caso passem 400 ms sem resetar o self.stopwatch, ou seja, 300 ms com ambos os motores na zona segura
                if self.stopwatch.time() > 80:
                    print("E:", self.lmotor.angle(), "D:", self.rmotor.angle())
                    print(velocEsq, velocDir)
                    print()
                    break

    def catch(self, release=False):
        """Pega/Solta o bloco."""
        if release:
            print("Going down...")
            self.claw.reset_angle(0)
            while self.claw.angle() > const.CLAWDG_DN:
                #print(self.claw.angle())
                if self.claw.angle() > const.CLAWDG_DN/8:
                    self.claw.run(const.CLAWSP_DN)
                else:
                    self.claw.run(const.CLAWSP_DN -900)
            self.claw.stop(Stop.HOLD)
        else:
            print("Going up...")
            self.claw.run_until_stalled(const.CLAWSP_UP, Stop.HOLD, const.CLAW_DTY_LIM)
            self.claw.set_dc_settings(100, 0)
    
    def fast_catch(self):
        self.claw.reset_angle(0)
        while self.claw.angle() < abs(const.CLAWDG_DN*0.95):
            self.claw.run(900)
        self.catch()

    def stop(self, stop_type = Stop.BRAKE):
        """Para os motores."""
        print("Stoping...")
        self.lmotor.run(0)
        self.rmotor.run(0)
        self.lmotor.stop(stop_type)
        self.rmotor.stop(stop_type)
        self.lmotor.run(0)
        self.rmotor.run(0)

    def align(self, color = 0, vInicial = 100, vPosterior = 100, intervOscilacao = 0, sameSide = False):
        """Alinha com uma linha."""
        print("Aligning...")
        self.lmotor.reset_angle(0)
        self.rmotor.reset_angle(0)
        self.lmotor.set_dc_settings(100, 0)
        self.rmotor.set_dc_settings(100, 0)
        if color == 0:
            # Alinha na linha preta
            lstate = 0
            rstate = 0
            boolDir = True
            boolEsq = True
            while not(lstate == 2 and rstate == 2 and self.lmotor.speed() == 0 and self.rmotor.speed() == 0):
                # print("E:", self.lcolor.reflection(), "D:", self.rcolor.reflection())
                # print(lstate, rstate)
                # print()
                
                """Estado 0 - Sensor ainda nao identificou a linha"""
                if rstate == 0 and lstate == 0:
                    # Nesse ponto do codigo, nenhum dos sensores identificou uma linha preta
                    # O robo continua andando, equilibrando os dois motores para manter a linha reta
                    # e sempre verificando os dois sensores
                    velocDir = velocEsq = vInicial
                    # Teto
                    if velocEsq > 900:
                        velocEsq = 900
                    if velocDir > 900:
                        velocDir = 900
                    diferenca_EsqDir = abs(self.lmotor.angle()) - abs(self.rmotor.angle())
                    # print("Diferenca", diferenca_EsqDir)
                    if abs(diferenca_EsqDir) > 3:
                        if diferenca_EsqDir > 0:
                            # self.lmotor andou mais, joga mais velocidade no self.rmotor
                            velocEsq = velocEsq * (1 - (intervOscilacao / 100))
                            velocDir = velocDir * (1 + (intervOscilacao / 100))
                        else:
                            # self.rmotor andou mais, joga mais velocidade no self.lmotor
                            velocEsq = velocEsq * (1 + (intervOscilacao / 100))
                            velocDir = velocDir * (1 - (intervOscilacao / 100))
                    if self.rcolor.reflection() < const.BLK_PCT and self.lcolor.reflection() < const.BLK_PCT:
                        rstate = lstate = 1 
                    if self.rcolor.reflection() < const.BLK_PCT:
                        rstate = 1
                    if self.lcolor.reflection() < const.BLK_PCT:
                        lstate = 1
                    self.lmotor.run(velocEsq)
                    self.rmotor.run(velocDir)
                elif rstate == 0:
                    # Apenas o sensor esquerdo ainda nao viu a linha preta
                    self.rmotor.run(vInicial)
                    if self.rcolor.reflection() < const.BLK_PCT:
                        rstate = 1
                elif lstate == 0:
                    # Apenas o sensor direito ainda nao viu a linha preta
                    self.lmotor.run(vInicial)
                    if self.lcolor.reflection() < const.BLK_PCT:
                        lstate = 1
                
                """Estado 1 - Sensor ja identificou a linha,
                Se sameSide == False pula pro proximo
                Se sameSide == True re com o robo para alinhar do outro lado"""
                if (lstate == 1 or rstate == 1) and sameSide:
                    self.lmotor.reset_angle(0)
                    while abs(self.lmotor.angle()) < 100:
                        self.lmotor.run(-vInicial/2)
                        self.rmotor.run(-vInicial/2)
                    self.lmotor.stop(Stop.HOLD)
                    self.rmotor.stop(Stop.HOLD)
                    lstate = 2
                    rstate = 2
                elif(lstate == 1):
                    self.lmotor.stop(Stop.BRAKE)
                    velocEsq = vPosterior
                    lstate = 2
                elif(rstate == 1):
                    self.rmotor.stop(Stop.BRAKE)
                    velocDir = vPosterior
                    rstate = 2

                """Estado 2 - Termina o alinhamento"""
                if sameSide:
                    multiplicador = 1
                else:
                    multiplicador = -1
                if lstate == 2:
                    if self.lcolor.reflection() > const.BLK_PCT + 10:
                        # Se o sensor ja passou pelo preto, mas atualmente ve branco
                        if boolEsq:
                            boolEsq = False
                            velocEsq = velocEsq*0.75
                        self.lmotor.run(multiplicador*velocEsq)
                    elif self.lcolor.reflection() < const.BLK_PCT - 10:
                        # Se o sensor ja passou pelo preto, mas atualmente ve muito preto
                        boolEsq = True
                        self.lmotor.run(-1*multiplicador*velocEsq)
                    else:
                        #Perfeitamente na borda
                        boolEsq = True
                        self.lmotor.stop(Stop.HOLD)
                if rstate == 2:
                    if self.rcolor.reflection() > const.BLK_PCT + 10:
                        # Se o sensor ja passou pelo preto, mas atualmente ve branco
                        if boolDir:
                            boolDir = False
                            velocDir = velocDir*0.75
                        self.rmotor.run(multiplicador*velocDir)
                    elif self.rcolor.reflection() < const.BLK_PCT - 10:
                        # Se o sensor ja passou pelo preto, mas atualmente ve muito preto
                        boolDir = True
                        self.rmotor.run(-1*multiplicador*velocDir)
                    else:
                        #Perfeitamente na borda
                        boolDir = True
                        self.rmotor.stop(Stop.HOLD)
            self.stop(Stop.HOLD)

        else:
            # Alinha na linha da cor dada
            while(self.rcolor.color() != color or self.lcolor.color() != color):
                if self.lcolor.color() == color:
                    self.lmotor.stop(Stop.HOLD)
                if self.rcolor.color() == color:
                    self.rmotor.stop(Stop.HOLD)
    
    def equilib(self, velocidade = 500, intervOscilacao = 8):
        # print("Equilibrando...")
        velocDir = velocEsq = velocidade
        # Teto
        if velocEsq > 900:
            velocEsq = 900
        if velocDir > 900:
            velocDir = 900
        diferenca_EsqDir = abs(self.lmotor.angle()) - abs(self.rmotor.angle())
        # print("Diferenca", diferenca_EsqDir)
        if abs(diferenca_EsqDir) > 3:
            if diferenca_EsqDir > 0:
                # self.lmotor andou mais, joga mais velocidade no self.rmotor
                velocEsq = velocEsq * (1 - (intervOscilacao / 100))
                velocDir = velocDir * (1 + (intervOscilacao / 100))
            else:
                # self.rmotor andou mais, joga mais velocidade no self.lmotor
                velocEsq = velocEsq * (1 + (intervOscilacao / 100))
                velocDir = velocDir * (1 - (intervOscilacao / 100))
        self.lmotor.run(velocEsq)
        self.rmotor.run(velocDir)
    
    def resetMotors(self):
        self.lmotor.reset_angle(0)
        self.rmotor.reset_angle(0)