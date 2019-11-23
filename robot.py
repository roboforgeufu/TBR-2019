# -*- coding: utf-8 -*-

"""Robot module."""

from pybricks.ev3devices import Motor, ColorSensor, GyroSensor
from pybricks.tools import wait, print, StopWatch
from pybricks.parameters import Stop
from pybricks.robotics import DriveBase

import constants as const


class Robot:
    """Classe do robo."""

    def __init__(self, lmport, rmport, clport, amport, csport, lcport, rcport, gyport, corner):
        """Inicializa variáveis do robo."""
        self.lmotor = Motor(lmport)
        self.rmotor = Motor(rmport)
        # self.claw = Motor(clport)
        # self.arm = Motor(amport)

        # self.recog = ColorSensor(csport)
        self.lcolor = ColorSensor(lcport)
        self.rcolor = ColorSensor(rcport)
        self.gyro = GyroSensor(gyport)

        self.map = [[const.UNK] * 4, [const.UNK] * 4]
        self.side = const.LEFT
        self.direction = const.NORTH
        self.corner = corner

        # TODO: Verificar a necessidade
        self.stopwatch = StopWatch()
        self.base = DriveBase(self.lmotor, self.rmotor, 56, 190)

    def walk(self, aFuncao=0, bFuncao=0, cFuncao=0, graus=0, intervOscilacao=15, insideReset=True):
        """Anda com o robo."""
        # TODO: Deixar velocidade constante.
        print("Walking...")
        if insideReset:
            self.lmotor.reset_angle(0)
            self.rmotor.reset_angle(0)
        velocDir = 0
        velocEsq = 0
        while True:
            # print(self.lmotor.angle(), self.rmotor.angle())
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
        K = 350
        grausMotor = K * grausCurva / 90

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
                if abs(difEsq) > 3:
                    # A diferenca eh consideravel
                    if difEsq > 0:
                        # Andou mais do que devia
                        sinalEsq = -1 * (
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

                # print("Tempo:", self.stopwatch.time(), "\ Vel:", velocDir, velocEsq)
                # print(difDir, difEsq)
                # Caso passem 400 ms sem resetar o self.stopwatch, ou seja, 300 ms com ambos os motores na zona segura
                if self.stopwatch.time() > 300:
                    print("E:", self.lmotor.angle(), "D:", self.rmotor.angle())
                    print(grausMotor)
                    print()
                    break

    def catch(self, release=False):
        """Pega/Solta o bloco."""
        print("Catching...")
        self.claw.run((-1 if release else 1) * const.CLAW_SP)
        wait(const.CLAW_WT)
        self.claw.stop()

    def stop(self):
        """Para os motores."""
        print("Stoping...")
        self.lmotor.stop(Stop.BRAKE)
        self.rmotor.stop(Stop.BRAKE)

    def check_block(self):
        """Verifica um bloco. Tamanho e cor."""
        # TODO: TESTAR COM O BRAÇO
        pass

    def align(self, color, velocidade):
        """Alinha com uma linha."""
        self.lmotor.run(velocidade)
        self.rmotor.run(velocidade)
        while(self.rcolor.color() != color or self.lcolor.color() != color):
            if self.lcolor.color() == color:
                self.lmotor.stop(Stop.HOLD)
            if self.rcolor.color() == color:
                self.rmotor.stop(Stop.HOLD)
