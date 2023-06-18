import numpy as np
def converter(string):
    x=[i for i in string]
    return x
def tabuleiro_inicio():
    #inicializando a matriz
    matriz = np.zeros((23,12), dtype=str)
    matriz[::4, ::2] = "#"
    matriz[::4, 1::2] = " "
    matriz[2::4, ::2]=" "
    matriz[2::4, 1::2]="#"
    for i in range(23):
        for j in range(12):
            if (i==0 or i==22) and 0<j<=10:
                matriz[i][j]=chr(65+(j-1))
            if 0<i<7 and ((i%4!=0 and j%2==0) or (i%4==0 and j%2==1)) and 0<j<11:
                matriz[i][j]="o"
            if 15<=i<22 and ((i%4!=0 and j%2==0) or (i%4==0 and j%2==1)) and 0<j<11:
                matriz[i][j]="@"
            if i%2==1 and (j!=0 or j!=11):
                matriz[i][j]="-"
            if (j==0 or j==11) and i%2==0 and (i!=0 and i!=22):
                matriz[i][j]=str((i/2)-1)
            elif (j==0 or j==11):
                matriz[i][j]=" "
    return matriz
def print_tabuleiro(x):
    #printando a matriz
    print("A configuraçao é:")
    matriz=x
    for i in range(23):
        for j in range(12): 
            if i%2==1 and (i!=0 and i!=22) and (j!=11):
                print(matriz[i][j], end="+")
            elif (i==0 or i ==22) or j==11:
                print(matriz[i][j], end=" ")
            else:
                print(matriz[i][j], end="|")
        print()
def eh_dama(x):
    #transforma uma peça em dama
    matriz=x
    for i in range(2,21,18):
        for j in range(12):
            if (matriz[i][j]=="@" and i==2):
                matriz[i][j]="&"
            if (matriz[i][j]=="o" and i==20):
                matriz[i][j]="O"
    return x
def pode_ser_comida(x):
    matriz=x
    posso_comer=False
    #VERIFICANDO SE HÁ ALGUMA PEÇA QUE POSSA SER COMIDA, SE SIM, EMITINDO UMA BOOLEANA VERDADEIRA
    for i in range(23):
        for j in range(12):
            if matriz[i][j]=="o":
                if (matriz[i-2][j-1]=="@" and matriz[i+2][j+1]==" "):
                    posso_comer=True
                if matriz[i+2][j+1]=="@" and matriz[i-2][j-1]==" ":
                    posso_comer=True
                if matriz[i-2][j+1]=="@" and matriz[i+2][j-1]==" ":
                    posso_comer=True
                if matriz[i+2][j-1]=="@" and matriz[i-2][j+1]==" ":
                    posso_comer=True
            if matriz[i][j]=="@":
                if (matriz[i-2][j-1]=="o" and matriz[i+2][j+1]==" "):
                    posso_comer=True
                if matriz[i+2][j+1]=="o" and matriz[i-2][j-1]==" ":
                    posso_comer=True
                if matriz[i-2][j+1]=="o" and matriz[i+2][j-1]==" ":
                    posso_comer=True
                if matriz[i+2][j-1]=="o" and matriz[i-2][j+1]==" ":
                    posso_comer=True
    return posso_comer
def jogada_player1(x):
    #fazer a jogada do player 1
    matriz=x
    entrada= input("Turno do Jogador de Cima, coloque a entrada na forma <COLUNA_INICIAL><LINHA_INICIAL>--<COLUNA_FINAL><LINHA_FINAL>\n").split("--")
    cordenadas_inicio=converter(entrada[0])
    coluna_inicio=(ord(cordenadas_inicio[0])-64)
    linha_inicio=(int(cordenadas_inicio[1])*2+2)
    cordenadas_final=converter(entrada[1])
    coluna_final=(ord(cordenadas_final[0])-64)
    linha_final=(int(cordenadas_final[1])*2+2)
    valido=False
    captura=False
    y=pode_ser_comida(matriz)
    #VERIFICANDO SE O MOVIMENTO É VÁLIDO
    if matriz[linha_inicio][coluna_inicio]=="o" and (((linha_final==linha_inicio+2) and (coluna_final==coluna_inicio+1 or coluna_final==coluna_inicio-1))) and matriz[linha_final][coluna_final]==" ":
        valido=True #AO PULAR LINHAS, LEMBRAR-SE QUE NA MATRIZ EXISTE AS LINHAS DE +- NO MEIO, OU SEJA, O PULO TEM QUE SER DUPLO AO INVÉS DE UNITÁRIO.
    if matriz[linha_inicio][coluna_inicio]=="o" and (linha_final==linha_inicio+4 and coluna_final==coluna_inicio+2 and matriz[linha_final-2][coluna_final-1]=="@" or linha_final==linha_inicio-4 and coluna_final==coluna_inicio-2 and matriz[linha_final+2][coluna_final+1]=="@") and matriz[linha_final][coluna_final]==" ":
        valido=True
        captura=True
    elif matriz[linha_inicio][coluna_inicio]=="o" and (linha_final==linha_inicio+4 and coluna_final==coluna_inicio-2 and matriz[linha_final-2][coluna_final+1]=="@" or linha_final==linha_inicio-4 and coluna_final==coluna_inicio+2 and matriz[linha_final+2][coluna_final-1]=="@") and matriz[linha_final][coluna_final]==" ":
        valido=True
        captura=True
    #VERIFICANDO SE NÃO HÁ NENHUMA PEÇA QUE POSSA SER COMIDA, SE HOUVER, O JOGADOR É OBRIGADO A EXECUTAR O MOVIMENTO DE COMÊ-LA
    if y==True and matriz[linha_inicio][coluna_inicio]=="o" and (((linha_final==linha_inicio+2) and (coluna_final==coluna_inicio+1 or coluna_final==coluna_inicio-1))) and matriz[linha_final][coluna_final]==" ":
        valido=False
    while valido==False:
    #SE O MOVIMENTO NÃO FOR VÁLIDO, O CÓDIGO SE REPETE
        print("Input inválido, por favor, tente novamente")
        matriz=x
        entrada= input("Turno do Jogador de Cima, coloque a entrada na forma <COLUNA_INICIAL><LINHA_INICIAL>--<COLUNA_FINAL><LINHA_FINAL>\n").split("--")
        cordenadas_inicio=converter(entrada[0])
        coluna_inicio=(ord(cordenadas_inicio[0])-64)
        linha_inicio=(int(cordenadas_inicio[1])*2+2)
        cordenadas_final=converter(entrada[1])
        coluna_final=(ord(cordenadas_final[0])-64)
        linha_final=(int(cordenadas_final[1])*2+2)
        valido=False
        captura=False
        y=pode_ser_comida(matriz)
        if matriz[linha_inicio][coluna_inicio]=="o" and (((linha_final==linha_inicio+2) and (coluna_final==coluna_inicio+1 or coluna_final==coluna_inicio-1))) and matriz[linha_final][coluna_final]==" ":
            valido=True #AO PULAR LINHAS, LEMBRAR-SE QUE NA MATRIZ EXISTE AS LINHAS DE +- NO MEIO, OU SEJA, O PULO TEM QUE SER DUPLO AO INVÉS DE UNITÁRIO.
        if matriz[linha_inicio][coluna_inicio]=="o" and (linha_final==linha_inicio+4 and coluna_final==coluna_inicio+2 and matriz[linha_final-2][coluna_final-1]=="@" or linha_final==linha_inicio-4 and coluna_final==coluna_inicio-2 and matriz[linha_final+2][coluna_final+1]=="@") and matriz[linha_final][coluna_final]==" ":
            valido=True
            captura=True  
        elif matriz[linha_inicio][coluna_inicio]=="@" and (linha_final==linha_inicio+4 and coluna_final==coluna_inicio-2 and matriz[linha_final-2][coluna_final+1]=="@" or linha_final==linha_inicio-4 and coluna_final==coluna_inicio+2 and matriz[linha_final+2][coluna_final-1]=="@") and matriz[linha_final][coluna_final]==" ":
            valido=True
            captura=True
        if y==True and matriz[linha_inicio][coluna_inicio]=="o" and (((linha_final==linha_inicio+2) and (coluna_final==coluna_inicio+1 or coluna_final==coluna_inicio-1))) and matriz[linha_final][coluna_final]==" ":
            valido=False
    #EXECUTANDO O MOVIMENTO, TROCA-SE DE LUGAR O ELEMENTOS DAS CORDENADAS INICIAIS COM O ELEMENTO DAS CORDENADAS FINAIS
    aux=matriz[linha_inicio][coluna_inicio]
    matriz[linha_inicio][coluna_inicio]=matriz[linha_final][coluna_final]
    matriz[linha_final][coluna_final]=aux
    if captura==True:
        #SE O MOVIMENTO FOR DE CAPTURA, ALÉM DE MOVER A PEÇA, APAGA-SE A PEÇA QUE FOI COMIDA.
        if coluna_final==coluna_inicio+2:
            coluna_captura=coluna_final-1
        elif coluna_final==coluna_inicio-2:
            coluna_captura=coluna_final+1
        if linha_final==linha_inicio+4:
            linha_captura=linha_final-2
        elif linha_final==linha_inicio-4:
            linha_captura=linha_final+2
        matriz[linha_captura][coluna_captura]=" "
        print("Você comeu uma peça!, jogue novamente")
        print_tabuleiro(matriz)
        jogada_player1(matriz)
    return matriz
def jogada_player2(x):
    #FUNÇÃO IGUAL A PRIMEIRA, PORÉM PARA O SEGUNDO JOGADOR, O CÓDIGO FOI FEITO ASSIM PARA MELHOR ORGANIZAÇÃO
    matriz=x
    entrada= input("Turno do Jogador de Baixo, coloque a entrada na forma <COLUNA_INICIAL><LINHA_INICIAL>--<COLUNA_FINAL><LINHA_FINAL>\n").split("--")
    cordenadas_inicio=converter(entrada[0])
    coluna_inicio=(ord(cordenadas_inicio[0])-64)
    linha_inicio=(int(cordenadas_inicio[1])*2+2)
    cordenadas_final=converter(entrada[1])
    coluna_final=(ord(cordenadas_final[0])-64)
    linha_final=(int(cordenadas_final[1])*2+2)
    valido=False
    captura=False
    y=pode_ser_comida(matriz)
    if matriz[linha_inicio][coluna_inicio]=="@" and (((linha_final==linha_inicio-2) and (coluna_final==coluna_inicio+1 or coluna_final==coluna_inicio-1)))  and matriz[linha_final][coluna_final]==" ":
        valido=True
    if matriz[linha_inicio][coluna_inicio]=="@" and (linha_final==linha_inicio+4 and coluna_final==coluna_inicio+2 and matriz[linha_final-2][coluna_final-1]=="o" or linha_final==linha_inicio-4 and coluna_final==coluna_inicio-2 and matriz[linha_final+2][coluna_final+1]=="o") and matriz[linha_final][coluna_final]==" ":
        valido=True
        captura=True  
    elif matriz[linha_inicio][coluna_inicio]=="@" and (linha_final==linha_inicio+4 and coluna_final==coluna_inicio-2 and matriz[linha_final-2][coluna_final+1]=="o" or linha_final==linha_inicio-4 and coluna_final==coluna_inicio+2 and matriz[linha_final+2][coluna_final-1]=="o") and matriz[linha_final][coluna_final]==" ":
        valido=True
        captura=True
    if y==True and matriz[linha_inicio][coluna_inicio]=="@" and (((linha_final==linha_inicio-2) and (coluna_final==coluna_inicio+1 or coluna_final==coluna_inicio-1))) and matriz[linha_final][coluna_final]==" ":
            valido=False
    while valido==False:
        print("Input inválido, por favor, tente novamente")
        matriz=x
        entrada= input("Turno do Jogador de Baixo, coloque a entrada na forma <COLUNA_INICIAL><LINHA_INICIAL>--<COLUNA_FINAL><LINHA_FINAL>\n").split("--")
        cordenadas_inicio=converter(entrada[0])
        coluna_inicio=(ord(cordenadas_inicio[0])-64)
        linha_inicio=(int(cordenadas_inicio[1])*2+2)
        cordenadas_final=converter(entrada[1])
        coluna_final=(ord(cordenadas_final[0])-64)
        linha_final=(int(cordenadas_final[1])*2+2)
        valido=False
        captura=False
        y=pode_ser_comida(matriz)
        if matriz[linha_inicio][coluna_inicio]=="@" and (((linha_final==linha_inicio-2) and (coluna_final==coluna_inicio+1 or coluna_final==coluna_inicio-1)))  and matriz[linha_final][coluna_final]==" ":
            valido= True
        if matriz[linha_inicio][coluna_inicio]=="@" and (linha_final==linha_inicio+4 and coluna_final==coluna_inicio+2 and matriz[linha_final-2][coluna_final-1]=="o" or linha_final==linha_inicio-4 and coluna_final==coluna_inicio-2 and matriz[linha_final+2][coluna_final+1]=="o") and matriz[linha_final][coluna_final]==" ":
            valido=True
            captura=True
        elif matriz[linha_inicio][coluna_inicio]=="@" and (linha_final==linha_inicio+4 and coluna_final==coluna_inicio-2 and matriz[linha_final-2][coluna_final+1]=="o" or linha_final==linha_inicio-4 and coluna_final==coluna_inicio+2 and matriz[linha_final+2][coluna_final-1]=="o") and matriz[linha_final][coluna_final]==" ":
            valido=True
            captura=True
        if y==True and matriz[linha_inicio][coluna_inicio]=="@" and (((linha_final==linha_inicio+2) and (coluna_final==coluna_inicio+1 or coluna_final==coluna_inicio-1))) and matriz[linha_final][coluna_final]==" ":
            valido=False
    aux=matriz[linha_inicio][coluna_inicio]
    matriz[linha_inicio][coluna_inicio]=matriz[linha_final][coluna_final]
    matriz[linha_final][coluna_final]=aux
    if captura==True:
        if coluna_final==coluna_inicio+2:
            coluna_capturada=coluna_final-1
        elif coluna_final==coluna_inicio-2:
            coluna_capturada=coluna_final+1
        if linha_final==linha_inicio+4:
            linha_capturada=linha_final-2
        elif linha_final==linha_inicio-4:
            linha_capturada=linha_final+2
        matriz[linha_capturada][coluna_capturada]=" "
        print("Você comeu uma peça!, jogue novamente")
        print_tabuleiro(matriz)
        jogada_player2(matriz)
    return matriz

#print("Vamos jogar damas!")
#print_tabuleiro(tabuleiro_inicio())
#acabou=False
#pecas1=pecas2=15
turno=0
#while acabou==False:
print_tabuleiro(tabuleiro_inicio())
matriz=(tabuleiro_inicio())
while True:
    #EM TURNOS PARES, QUEM JOGA É O JOGADOR DE CIMA, EM TURNOS ÍMPARES, O JOGADOR DE BAIXO, ISSO SERÁ MUDADO NA VERSÃO FINAL
    if turno%2==0:
        matriz=jogada_player1(matriz)
        print_tabuleiro(matriz)
    if turno%2==1:
        matriz=jogada_player2(matriz)
        print_tabuleiro(matriz)
    turno+=1
