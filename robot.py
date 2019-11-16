from pybricks.ev3devices import Motor, ColorSensor
from pybricks.tools import wait, print, StopWatch
from pybricks.parameters import Stop
from pybricks.robotics import DriveBase

import constants as const

class Robot():

    def __init__(self, lmport, rmport, clport, csport):
        
        self.lmotor = Motor(lmport)
        self.rmotor = Motor(rmport)
        self.claw = Motor(clport)
        self.recog = ColorSensor(csport)
        self.stopwatch = StopWatch()
        self.base = DriveBase(self.lmotor, self.rmotor, 56, 190)

    def walk2(self, speed, steering):
        
        self.base.drive(speed, steering)

    def walk(self, aFuncao = 0, bFuncao = 0, cFuncao = 0, graus = 0, intervOscilacao = 15, insideReset = True):
        print('Walking...')
        if insideReset:
            self.lmotor.reset_angle(0)
            self.rmotor.reset_angle(0)
        velocDir = 0
        velocEsq = 0
        while True:
            #print(self.lmotor.angle(), self.rmotor.angle())
            #Funcao que descreve a velocidade em funcao da porcentagem do deslocamento ja realizado
            percDeslocado = (self.lmotor.angle()/graus)*100
            velocEsq = (aFuncao * (percDeslocado ** 2) + bFuncao * percDeslocado + cFuncao)*10
            velocDir = velocEsq
            
            #Teto
            if velocEsq > 900:
                velocEsq = 900
            if velocDir > 900:
                velocDir = 900

            diferenca_EsqDir = abs(self.lmotor.angle()) - abs(self.rmotor.angle())
            if abs(diferenca_EsqDir) > 3:
                if diferenca_EsqDir > 0:
                    #self.lmotor andou mais, joga mais velocidade no self.rmotor
                    velocEsq = velocEsq * (1 - (intervOscilacao/100))
                    velocDir = velocDir * (1 + (intervOscilacao/100))
                else:
                    #self.rmotor andou mais, joga mais velocidade no self.lmotor
                    velocEsq = velocEsq * (1 + (intervOscilacao/100))
                    velocDir = velocDir * (1 - (intervOscilacao/100))
            self.lmotor.run(velocEsq)
            self.rmotor.run(velocDir)
            if (abs(velocEsq) < 50 and abs(velocDir) < 50) or percDeslocado >= 99:
                break

    def turn(self, aFuncao, bFuncao, cFuncao, grausCurva, fix = True):
        print('Turning...')
        self.lmotor.reset_angle(0)
        self.rmotor.reset_angle(0)

        #P/ calibrar
        K = 180
        grausMotor = K * grausCurva / 90
        
        mediaPercorrida = 0
        while mediaPercorrida < 99:  
            #Calculo da velocidade de ambos os motores em funcao da media do deslocamento percorrido por cada um
            percPercorridoEsq = (abs(self.lmotor.angle())/grausMotor)*100
            percPercorridoDir = (abs(self.rmotor.angle())/grausMotor)*100
            mediaPercorrida = (percPercorridoDir + percPercorridoEsq)/2.0
            
            velocidade = (aFuncao * (mediaPercorrida ** 2) + bFuncao * mediaPercorrida + cFuncao)*10
            
            self.lmotor.run(velocidade)
            self.rmotor.run(-velocidade)
        self.lmotor.stop()
        self.rmotor.stop()

        if fix:
            while True:
                #Para o motor Esquerdo:
                difEsq = abs(self.lmotor.angle()) - grausMotor
                if abs(difEsq) > 3:
                    #A diferenca eh consideravel
                    if difEsq > 0:
                        #Andou mais do que devia
                        sinalEsq = -1 * (self.lmotor.angle()/abs(self.lmotor.angle())) #Deve se movimentar no sentido contrario ao mov anterior
                    else:
                        #Andou menos do que devia
                        sinalEsq = (self.lmotor.angle()/abs(self.lmotor.angle())) #Deve se movimentar no mesmo sentido do movimento anterior
                    velocEsq = sinalEsq * (2*abs(difEsq)+50)
                else:
                    #A diferenca eh irrelevante
                    velocEsq = 0

                #Para o motor Direito:
                difDir = abs(self.rmotor.angle()) - grausMotor
                if abs(difDir) > 3:
                    #A diferenca eh consideravel
                    if difDir > 0:
                        #Andou mais do que devia
                        sinalDir = -1 * (self.rmotor.angle()/abs(self.rmotor.angle())) #Deve se movimentar no sentido contrario ao mov anterior
                    else:
                        #Andou menos do que devia
                        sinalDir = (self.rmotor.angle()/abs(self.rmotor.angle())) #Deve se movimentar no mesmo sentido do movimento anterior
                    velocDir = sinalDir * (2*abs(difDir)+50)
                else:
                    #A diferenca eh irrelevante
                    velocDir = 0
                
                #Por fim, manda a velocidade calculada para os motores
                self.lmotor.run(velocEsq)
                self.rmotor.run(velocDir)

                if (difDir not in range(-3, 4)) or (difEsq not in range(-3, 4)): #Se qualquer dos motores estiver fora do intervalo seguro, entao ele ainda nao comeca a contar
                    self.stopwatch.reset() # Nao comecar a contar <=> resetar constantemente o self.stopwatch
                
                #print("Tempo:", self.stopwatch.time(), "\ Vel:", velocDir, velocEsq)
                #print(difDir, difEsq)
                if self.stopwatch.time() > 300: #Caso passem 400 ms sem resetar o self.stopwatch, ou seja, 300 ms com ambos os motores na zona segura
                    print("E:", self.lmotor.angle(), "D:", self.rmotor.angle())
                    print(grausMotor)
                    print()
                    break


    def catch(self, release = False):
        print('Catching...')
        self.claw.run((-1 if release else 1) * const.CLAW_SP)
        wait(const.CLAW_WT)
        self.claw.stop()


    def stop(self):

        print('Stoping...')
        self.base.stop(stop_type=Stop.BRAKE)
        self.lmotor.stop(Stop.BRAKE)
        self.rmotor.stop(Stop.BRAKE)
