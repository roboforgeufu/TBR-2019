import time

def leBloco(cor = -1, tamanho = '-'):
    if cor == -1:
        while True:
            tempCor = int(input(">>Qual a cor do bloco?(1, 2, 5)")) 
            if tempCor not in [1, 2, 5]:
                print("Entrada invalida.")
                continue
            else:
                break
    else:
        tempCor = cor    
    if tamanho == '-':
        while True:
            tempTamanho = input(">>Qual o tamanho do bloco?(P, G)")
            if tempTamanho not in ['P', 'G']:
                print("Entrada invalida.")
                continue
            else:
                break
    else:
        tempTamanho = tamanho
    return [tempCor, tempTamanho]

def deducao(blocosAzuis, blocosPretos, blocoVermelho, blocosGrandes, blocosPequenos):
    #Possivel deducao de alguma caracteristica do bloco dado as quantidades ainda nao lidas de cada tipo
    tempCor = -1
    tempTamanho = '-'

    if blocosGrandes == 0 and blocosPequenos > 0:
        print("O robo ja sabe que e um bloco pequeno.")
        tempTamanho = 'P'
    elif blocosPequenos == 0 and blocosGrandes > 0:
        print("O robo ja sabe que e um bloco grande.")
        tempTamanho = 'G'

    if blocosAzuis + blocosPretos == 0 and blocoVermelho > 0:
        print("O robo ja sabe que e um bloco vermelho.")
        tempCor = 5
    elif blocosAzuis + blocoVermelho == 0 and blocosPretos > 0:
        print("O robo ja sabe que e um bloco preto.")
        tempCor = 1
    elif blocosPretos + blocoVermelho == 0 and blocosAzuis > 0:
        print("O robo ja sabe que e um bloco azul.")
        tempCor = 2
    
    return [tempCor, tempTamanho]


#Dados que o robo armazenara
blocosConhecidos = []
for x in range(9):
    blocosConhecidos.append([-1, '-'])
print(blocosConhecidos)

depositoAzul = [False, False, False]
depositoPreto = [False, False, False]

base = {
    1 : "Azul",
    2 : "Preta"
    }

#Quantos blocos de cada tipo, pra que o robo consiga fazer deducao durante o processo
blocosAzuis = 4
blocosPretos = 4
blocoVermelho = 1
blocosGrandes = 7
blocosPequenos = 2



print("<<<Simulacao dos processos feitos pelo robo no Desafio Pratico TBR 2019>>>\n")
#time.sleep(1)
print("Start!")
#time.sleep(1)

while True:
    baseInicial = int(input(">>O robo comeca em qual base?(1.Azul/2.Preta) :-"))
    if baseInicial not in range(1, 3):
        print("Entrada invalida.")
        time.sleep(0.5)
        continue
    else:
        break
#time.sleep(1)

print("O robo se move da base %s ate o bloco no centro." % base[baseInicial])
#time.sleep(1)
print("O robo le a cor do bloco do centro.")
#time.sleep(1)

print("O robo ja sabe que o bloco do meio e grande.")
blocosGrandes -= 1
blocosConhecidos[8] = leBloco(tamanho = 'G')

print("\nValores guardados para o bloco:", blocosConhecidos[8])

if blocosConhecidos[8][0] == 1:
    print("Como o bloco e preto:\n\tO robo se move em linha reta para o sul")
    blocosPretos -= 1
else:
    print("Como o bloco e azul\n\tO robo se move em linha reta para o norte")
    blocosAzuis -= 1

print("O robo se aproxima do deposito do meio.")
print("O robo deixa o bloco no deposito do meio.")
print("Agora o robo sabe que o deposito do meio daquela cor esta ocupado.")

if blocosConhecidos[8][0] == 1:
    depositoPreto[1] = True
else:
    depositoAzul[1] = True

print("\nValores salvos:")
print("depositoPreto =", depositoPreto)
print("depositoAzul =", depositoAzul)
print()

print("Independente de qual lado esta, o robo se vira para a sua esquerda.")
print("E entao segue em frente.")
print("Ao encontrar um bloco, faz a leitura de cor e tamanho.")

if blocosConhecidos[8][0] == 1:
    idxBlocoAtual = 7
else:
    idxBlocoAtual = 3

while blocosGrandes > 0:
    if idxBlocoAtual == -1:
        idxBlocoAtual = 7
    skip = input("<>")
    try:
        if int(skip) == 1:
            print("Valores salvos pelo robo:\n\t", blocosConhecidos)
            print("\tdepositoAzul =", depositoAzul)
            print("\tdepositoPreto =", depositoPreto)
    except:
        print()
    print("\n\nPosicao -> Bloco", (idxBlocoAtual+1))
    if blocosConhecidos[idxBlocoAtual][0] == -1:
        print("Bloco ainda nao conhecido. Le o bloco.")

        deduCor, deduTamanho = deducao(blocosAzuis, blocosPretos, blocoVermelho, blocosGrandes, blocosPequenos)

        blocosConhecidos[idxBlocoAtual] = leBloco(deduCor, deduTamanho)
        print("\nValores salvos:")
        print("Bloco %d:" %(idxBlocoAtual+1), blocosConhecidos[idxBlocoAtual])
        if blocosConhecidos[idxBlocoAtual][1] == 'P':
            print("Ignora o cubo pois ele eh pequeno.")
            blocosPequenos -= 1
            idxBlocoAtual -= 1
        else:
            blocosGrandes -= 1
            if blocosConhecidos[idxBlocoAtual][0] == 5:
                blocoVermelho -= 1
                print("Cubo vermelho!")
                print("Coloca o cubo no centro.")
                print("Volta para ler o proximo bloco do mesmo lado que o anterior.")
                idxBlocoAtual -= 1
            else:
                if idxBlocoAtual >= 4:
                    inicioDeposito = 2
                    incremDeposito = -1
                else:
                    inicioDeposito = 0
                    incremDeposito = 1
                iPercorreDep = inicioDeposito
                if blocosConhecidos[idxBlocoAtual][0] == 1:
                    blocosPretos -= 1
                    print("Cubo preto!")
                    print("Se move ate o deposito preto.")
                    while iPercorreDep in range(0, 3):
                        print("Chega na posicao %d..."%iPercorreDep)
                        if not depositoPreto[iPercorreDep]:
                            print("Coloca o bloco na posicao %d." %iPercorreDep)
                            depositoPreto[iPercorreDep] = True
                            break
                        else:
                            print("Ja tem um bloco na posicao %d." %iPercorreDep)
                            print("Continua pra proxima posicao...")
                        iPercorreDep += incremDeposito
                    print("Volta para ler o proximo bloco do lado Preto.")
                    idxBlocoAtual = 7
                else:
                    blocosAzuis -= 1
                    print("Cubo azul!")
                    print("Se move ate o deposito azul.")
                    while iPercorreDep in range(0, 3):
                        print("Chega na posicao %d..."%iPercorreDep)
                        if not depositoAzul[iPercorreDep]:
                            print("Coloca o bloco na posicao %d." %iPercorreDep)
                            depositoAzul[iPercorreDep] = True
                            break
                        else:
                            print("Ja tem um bloco na posicao %d." %iPercorreDep)
                            print("Continua pra proxima posicao...")
                        iPercorreDep += incremDeposito
                    print("Volta para ler o proximo bloco do lado Azul.")
                    idxBlocoAtual = 3
    else:
        print("Bloco ja conhecido.")
        if blocosConhecidos[idxBlocoAtual][1] == 'P':
            print("Segue em frente pois e bloco pequeno.")
        else:
            print("O robo ja entregou esse bloco.")
            print("Se move ate o proximo.")
        idxBlocoAtual -= 1

print("O robo entregou todos os blocos grandes.")