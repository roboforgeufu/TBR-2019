# -*- coding: utf-8 -*-
from pybricks.parameters import Color

"""Constants file."""

# Claw
CLAWSP_UP = 1000
CLAWSP_DN = -200
CLAWDG_DN = -950
CLAW_DTY_LIM = 30

# Map
SML = -1
BIG_BLK = 1
BIG_BLU = 2
RED = 5
UNK = 0

LEFT = 0
RIGHT = 1

NORTH = 0
SOUTH = 1

BLACK_CNR = Color.BLACK
BLUE_CNR = Color.BLUE

# Motors
MOTOR_SP = 500

# COLORS
WHITE_PCT = 70
BLK_PCT = 35
BLACK = 1
BLUE = 2
RED = 5

SEEK_SP = 200
SEEK_DG = 150

#TURN
K = 250

BCK_SEEN = -30
REV_CATCH = -210
FWD_CATCH = 80

GREEN_CLOSE = 10

# DISTANCIAS DE ENTREGA
MEIO_GRANDE = 1200
MEIO_PEQUENO = 600

BACK_DEPOSIT = -650

#INFRA
DST_BIGBLOCK = 15

# FUNCOES VELOCIDADE CURVA

# Tempo = 650--
aT90_R = -0.016
bT90_R = 1.17
cT90_R = 50

aT90_L = 0.01
bT90_L = -0.7
cT90_L = -50

# Tempo = 620--
aCURVA45 = -0.008
bCURVA45 = 0.62
cCURVA45 = 25

# FUNCOES VELOCIDADE LINHA RETA

# Tempo(MeioGrande) = 1700--
# (MeioPequeno) = 970--
aRETA = -0.01
bRETA = 10
cRETA = 30
intRETA = 10


# SEEK DISTANCES
SEEK_DST_1 = 500
SEEK_DST_2 = 960
SEEK_DST_3 = 1300
