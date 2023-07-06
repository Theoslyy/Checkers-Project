'''
TRABALHO DE FuP

PARTICIPANTES:
PEDRO MILITÃO BONA LOPES-552261
PEDRO WAGNER RABELO EVARISTO-552271
THEO ARAUJO MAGALHÃES-555910
'''
import sys
import os
import numpy as np
clear = lambda: os.system('clear') #CRIAMOS UMA VARIÁVEL CLEAR PARA LIMPAR O TERMINAL A CADA JOGADA
quantidade_de_movimentos = 0
quantidade_de_peças1 = 15
quantidade_de_peças2 = 15
jogo = True
vencedor = None
modoOffline = False
jogadasLista = []
jogaCima=bool
novamente = True
novamente_bool = True
def converter(string):
    '''FUNÇÃO PARA CONVERTER STRINGS EM LISTAS'''
    x = [i for i in string]
    return x

def tabuleiro_inicio():

    '''Função para incializar a matriz, a qual tem 23 linhas e 12 colunas'''
    #TAMBÉM FORAM COLOCADAS AS #, ALTERNANDO DE 4 EM 4, DEIXANDO LINHAS VAZIAS, POIS NELAS SERÃO COLOCADOS OS DIVISORES DE LINHAS (+-+-+-+)
    matriz = np.zeros((23,12), dtype=str)

    matriz[::4, ::2] = "#"

    matriz[::4, 1::2] = " "

    matriz[2::4, ::2]=" "

    matriz[2::4, 1::2]="#"

    for i in range(23):
        for j in range(12):

            #COLOCANDO, NA PRIMEIRA E NA ÚLTIMA LINHA, OS ÍNDICES DAS COLUNAS, QUE VÃO DE A ATÉ J
            if (i==0 or i==22) and 0<j<=10:
                matriz[i][j]=chr(65+(j-1))
            
            #COLOCANDO AS PEÇAS "o"
            if 0<i<7 and ((i%4!=0 and j%2==0) or (i%4==0 and j%2==1)) and 0<j<11:
                matriz[i][j]="o"

            #COLOCANDO AS PEÇAS "@"
            if 15<=i<22 and ((i%4!=0 and j%2==0) or (i%4==0 and j%2==1)) and 0<j<11:
                matriz[i][j]="@"

            #COLOCANDO, NAS LINHAS VAZIAS, OS ELEMENTOS "-"
            if i%2==1 and (j!=0 or j!=11):
                matriz[i][j]="-"

            #COLOCANDO, NA PRIMEIRA E ULTIMA COLUNA, OS ÍNDICES DAS LINHAS, QUE VÃO DE 0 A 9
            if (j==0 or j==11) and i%2==0 and (i!=0 and i!=22):
                matriz[i][j]=str((i/2)-1)

            #FAZENDO COM QUE, NA PRIMEIRA E NA ULTIMA COLUNA, ONDE NÃO TIVER ÍNDICE, SEJJA VAZIO
            elif (j==0 or j==11):
                matriz[i][j]=" "
    return matriz
def print_tabuleiro(x):
    '''Função que printa a matriz que foi dada a ela como parâmetro'''
    matriz=x
    for i in range(23):
        for j in range(12): 

            #PRINTANDO, NAS LINHAS DE DIVISÃO, O ELEMENTO "-", SEPARADOS POR "+", FORMANDO, ASSIM, A SEQUÊNCIA "+-+-+..."
            if i%2==1 and (i!=0 and i!=22) and (j!=11):
                print(matriz[i][j], end="+")

            #PRINTANDO OS ELEMENTOS DA PRIMEIRA E DA ÚLTIMA LINHA, ASSIM COMO DA ÚLTIMA COLUNA, SEPARADOS POR VAZIO
            elif (i==0 or i ==22) or j==11:
                print(matriz[i][j], end=" ")

            #O RESTO DOS ELEMENTOS SÃO PRINTADOS SEPARADOS POR |
            else:
                print(matriz[i][j], end="|")
        print()

def eh_dama(x):
    '''Função que verifica, na primeira e na última linha, se a peça é uma dama. Se for, ela é convertida'''
    matriz=x
    for i in range(2,21,18):
        for j in range(12):
            if (matriz[i][j]=="@" and i==2):
                matriz[i][j]="&"
            if (matriz[i][j]=="o" and i==20):
                matriz[i][j]="O"
    return x


def pode_ser_comida1(x):
    '''É verificado se a peça do tipo "o" pode ser capturada, verifica-se se existe uma peça oposta de um lado e um espaço vazio no outro'''
    matriz=x
    posso_comer=False
    for i in range(2,21):
        for j in range(12):

            if matriz[i][j]=="o" or matriz[i][j]=="O":

                if matriz[i-2][j-1]=="@" and matriz[i+2][j+1]==" " and j+1<11:
                    posso_comer=True
                            
                if matriz[i+2][j+1]=="@" and matriz[i-2][j-1]==" " and j-1>0:
                    posso_comer=True
                            
                if matriz[i-2][j+1]=="@" and matriz[i+2][j-1]==" " and j-1>0:
                    posso_comer=True
                            
                if matriz[i+2][j-1]=="@" and matriz[i-2][j+1]==" " and j+1<11:
                    posso_comer=True
    return posso_comer

def pode_ser_comida2(x):
    '''É verificado se a peça do tipo "@" pode ser capturada, verifica-se se existe uma peça oposta de um lado e um espaço vazio no outro'''
    matriz=x
    posso_comer=False
    for i in range(2,21):
        for j in range(12):
            #O MESMO CÓDIGO É REPETIDO, PORÉM AGORA VERIFICANDO SE EXITE ALGUMA PEÇA "@" OU "&" QUE PODE SER COMIDA
            if matriz[i][j]=="@" or matriz[i][j]=="&":

                if matriz[i-2][j-1]=="o" and matriz[i+2][j+1]==" " and j+1<11:
                    posso_comer=True
                
                if matriz[i+2][j+1]=="o" and matriz[i-2][j-1]==" " and j-1>0:
                    posso_comer=True
                
                if matriz[i-2][j+1]=="o" and matriz[i+2][j-1]==" " and j-1>0:
                    posso_comer=True
                
                if matriz[i+2][j-1]=="o" and matriz[i-2][j+1]==" " and j+1<11:
                    posso_comer=True

    return posso_comer

def dama_ta_livre(m,a,b,c,d):
    '''Função que verifica se, no caminho da dama, não existe nenhuma peça a obstruindo'''

    ta_livre=True

    #COMEÇANDO DAS CORDENADAS INICIAIS, VAI SE VERIFICANDO AS CASAS EM DIAGONAL, SE ALLGUMA DELAS NÃO ESTIVER VAZIA, A FUNÇÃO RETORNARÁ UMA BOOLEANA FALSA
    if a>c and b>d:
        a-=2
        b-=1
        while a>c and b>d:
            if m[a][b]!=" ":
                ta_livre=False
                break
            a-=2
            b-=1
    
    elif a<c and b<d:
        a+=2
        b+=1
        while a<c and b<d:
            if m[a][b]!=" ":
                ta_livre=False
                break
            a+=2
            b+=1
    
    elif a>c and b<d:
        a-=2
        b+=1
        while a>c and b<d:
            if m[a][b]!=" ":
                ta_livre=False
                break
            a-=2
            b+=1

    elif a<c and b>d:
        a+=2
        b-=1
        while a<c and b>d:
            if m[a][b]!=" ":
                ta_livre=False
                break
            a+=2
            b-=1

    return ta_livre

def esvaziar_caminho(m,a,b,c,d):
    #Função que esvazia o caminho numa captura

    if a>c and b>d:
        a-=2
        b-=1
        while a>c and b>d:
            m[a][b]=" "

            a-=2
            b-=1

    elif a<c and b<d:
        a+=2
        b+=1
        while a<c and b<d:
            m[a][b]=" "

            a+=2
            b+=1

    elif a>c and b<d:
        a-=2
        b+=1
        while a>c and b<d:
            m[a][b]=" "

            a-=2
            b+=1

    elif a<c and b>d:
        a+=2
        b-=1
        while a<c and b>d:
            m[a][b]=" "

            a+=2
            b-=1

    return m

def ta_livre_pra_comer1(m,a,b,c,d):
    #ARIAÇÃO DA FUNÇÃO "TÁ LIVRE" QUE VERIFICA SE, EM UM MOVIMENTO DE CAPTURA, EXISTEM MAIS COISAS ALÉM DA PEÇA QUE SERÁ CAPTURADA

    ta_livre=True
    contador=0

    if a>c and b>d:
        a-=2
        b-=1
        while a>c and b>d:
            if m[a][b]=="@" or m[a][b]=="&":
                contador+=1
            if m[a][b]!=" " and m[a][b]!="@" and m[a][b]!="&":
                ta_livre=False
                break
            a-=2
            b-=1
    
    elif a<c and b<d:
        a+=2
        b+=1
        while a<c and b<d:
            if m[a][b]=="@" or m[a][b]=="&":
                contador+=1
            if m[a][b]!=" " and m[a][b]!="@" and m[a][b]!="&":
                ta_livre=False
                break
            a+=2
            b+=1
    
    elif a>c and b<d:
        a-=2
        b+=1
        while a>c and b<d:
            if m[a][b]=="@" or m[a][b]=="&":
                contador+=1
            if m[a][b]!=" " and m[a][b]!="@" and m[a][b]!="&":
                ta_livre=False
                break
            a-=2
            b+=1

    elif a<c and b>d:
        a+=2
        b-=1
        while a<c and b>d:
            if m[a][b]=="@" or m[a][b]=="&":
                contador+=1
            if m[a][b]!=" " and m[a][b]!="@" and m[a][b]!="&":
                ta_livre=False
                break
            a+=2
            b-=1
    if contador!=1:
        ta_livre=False
    
    return ta_livre

def ta_livre_pra_comer2(m,a,b,c,d):
    ta_livre=True
    contador=0

    if a>c and b>d:
        a-=2
        b-=1
        while a>c and b>d:
            if m[a][b]=="o" or m[a][b]=="O":
                contador+=1
            if m[a][b]!=" " and m[a][b]!="o" and m[a][b]!="O":
                ta_livre=False
                break
            a-=2
            b-=1

    elif a<c and b<d:
        a+=2
        b+=1
        while a<c and b<d:
            if m[a][b]=="o" or m[a][b]=="O":
                contador+=1
            if m[a][b]!=" " and m[a][b]!="o" and m[a][b]!="O":
                ta_livre=False
                break
            a+=2
            b+=1

    elif a>c and b<d:
        a-=2
        b+=1
        while a>c and b<d:
            if m[a][b]=="o" or m[a][b]=="O":
                contador+=1
            if m[a][b]!=" " and m[a][b]!="o" and m[a][b]!="O":
                ta_livre=False
                break
            a-=2
            b+=1

    elif a<c and b>d:
        a+=2
        b-=1
        while a<c and b>d:
            if m[a][b]=="o" or m[a][b]=="O":
                contador+=1
            if m[a][b]!=" " and m[a][b]!="o" and m[a][b]!="O":
                ta_livre=False
                break
            a+=2
            b-=1

    if contador!=1:
        ta_livre=False

    return ta_livre
def tem_comida_no_caminho1(matriz,a,b):
    '''Função para verificar obrigatoriedade de comer das damas'''
    tem_comida=False

    c=a
    d=b

    c-=2
    d-=1
    
    while tem_comida==False and c>=2 and d>=1:
        if (matriz[c][d]=="@" or matriz[c][d]=="&") and matriz[c-2][d-1]==" " and d-1>0:
            tem_comida=True
            break
        c-=2
        d-=1

    if tem_comida==False:

        c=a
        d=b

        c+=2
        d+=1
    
        while tem_comida==False and c<=21 and d<=10:
            if (matriz[c][d]=="@" or matriz[c][d]=="&") and matriz[c+2][d+1]==" " and d+1<11:
                tem_comida=True
                break
            c+=2
            d+=1

    if tem_comida==False:

        c=a
        d=b

        c-=2
        d+=1
    
        while tem_comida==False and c>=2 and d<=10:
            if (matriz[c][d]=="@" or matriz[c][d]=="&") and matriz[c-2][d+1]==" " and d+1<11:
                tem_comida=True
                break
            c-=2
            d+=1
    
    if tem_comida==False:

        c=a
        d=b

        c+=2
        d-=1
    
        while tem_comida==False and c<=21 and d>=1:
            if (matriz[c][d]=="@" or matriz[c][d]=="&") and matriz[c+2][d-1]==" " and d-1>0:
                tem_comida=True
                break
            c+=2
            d-=1

    return tem_comida
def tem_comida_no_caminho2(matriz,a,b):
    '''Função para verificar obrigatoriedade de comer das damas'''
    tem_comida=False

    c=a
    d=b

    c-=2
    d-=1
    
    while tem_comida==False and c>=2 and d>=1:
        if (matriz[c][d]=="o" or matriz[c][d]=="O") and matriz[c-2][d-1]==" " and d-1>0:
            tem_comida=True
            break
        c-=2
        d-=1

    if tem_comida==False:

        c=a
        d=b

        c+=2
        d+=1
    
        while tem_comida==False and c<=21 and d<=10:
            if (matriz[c][d]=="o" or matriz[c][d]=="O") and matriz[c+2][d+1]==" " and d+1<11:
                tem_comida=True
                break
            c+=2
            d+=1

    if tem_comida==False:

        c=a
        d=b

        c-=2
        d+=1
    
        while tem_comida==False and c>=2 and d<=10:
            if (matriz[c][d]=="o" or matriz[c][d]=="O") and matriz[c-2][d+1]==" " and d+1<11:
                tem_comida=True
                break
            c-=2
            d+=1
    
    if tem_comida==False:

        c=a
        d=b

        c+=2
        d-=1
    
        while tem_comida==False and c<=21 and d>=1:
            if (matriz[c][d]=="o" or matriz[c][d]=="O") and matriz[c+2][d-1]==" " and d-1>0:
                tem_comida=True
                break
            c+=2
            d-=1

    return tem_comida

def dama_pode_comer1(matriz):
    '''Função para verificar possibilidade de comer das damas'''
    pode_comer=False
    controle=False
    for i in range(1,21):
        for j in range(1,11):
            if matriz[i][j]=="O" and tem_comida_no_caminho1(matriz,i,j)==True:
                pode_comer=True
                controle=True
                break
        if controle==True:
            break
    
    return pode_comer

def dama_pode_comer2(matriz):
    '''Função para verificar possibilidade de comer das damas'''
    pode_comer=False
    controle=False
    for i in range(1,21):
        for j in range(1,11):
            if matriz[i][j]=="&" and tem_comida_no_caminho2(matriz,i,j)==True:
                pode_comer=True
                controle=True
                break
        if controle==True:
            break
    
    return pode_comer

def jogada_player1(matriz):
    '''Função que faz a jogada do player das peças "o"'''
    global quantidade_de_peças2
    if quantidade_de_peças1 != 0 and quantidade_de_peças2 != 0:
        print("Você já comeu: ",15 - quantidade_de_peças2, "peças do jogador adversário.")
        #PEGANDO O INPUT E O DIVIDINDO EM DUAS PARTES, AS CORDENADAS DE INICIO E AS CORDENADAS FINAIS
        while True:
            try:
                entrada= input("Turno do Jogador de Cima, coloque a entrada na forma <COLUNA_INICIAL><LINHA_INICIAL>--<COLUNA_FINAL><LINHA_FINAL>\n").split("--")

                #AS CORDENADAS INICIAIS SÃO A PRIMEIRA PARTE DO INPUT, ELAS SÃO DIVIDIAS NOVAMENTE, OBTENDO DOIS ELEMENTOS
                cordenadas_inicio=converter(entrada[0])

                #O PRIMEIRO ELEMENTO É A COLUNA, QUE PASSA POR UM AJUSTE PARA QUE POSSAMOS TRABALHAR COM ELA
                #PEGAMOS O CÓDIGO ASCII DA LETRA E SUBTRAÍMOS 64, OBTENDO O NÚMERO CORRESPONDENTE AO ÍNDICE
                coluna_inicio=(ord(cordenadas_inicio[0])-64)

                #O SEGUNDO ELEMENTO É A LINHA, QUE TAMBÉM PASSA POR UM AJUSTE PARA QUE POSSAMOS TRABALHAR COM ELA
                #MULTIPLICAMOS O ÍNDICE POR 2 E SOMAMOS O RESULTADO COM 2, OBTENDO UM NÚMERO CORRESPONDENTE AO ÍNDICE
                linha_inicio=(int(cordenadas_inicio[1])*2+2)

                #O MESMO PROCESSO É FEITO PARA AS CORDENADAS FINAIS, QUE SÃO A SEGUNDA PARTE DO INPUT ORIGINAL
                cordenadas_final=converter(entrada[1])

                coluna_final=(ord(cordenadas_final[0])-64)

                linha_final=(int(cordenadas_final[1])*2+2)
                break
            except (IndexError, ValueError):
                print("Insira uma entrada válida!")
        #ESSA VARIÁVEL FICA ATIVA SE UM MOVIMENTO É VÁLIDO
        valido=False

        #ESSA VARIÁVEL FICA ATIVA SE FOR UM MOVIMENTO DE CAPTURA
        captura=False

        #AS DUAS PRÓXIMAS VARIÁVEIS RECEBEM FUNÇÕES JÁ EXPLICADAS
        captura_dama=False
        x=dama_pode_comer1(matriz)
        y=pode_ser_comida2(matriz)
        z=dama_ta_livre(matriz,linha_inicio,coluna_inicio,linha_final,coluna_final)
        #VERIFICANDO SE O MOVIMENTO É VÁLIDO
        #SEGUEM UMA SEQUENCIA DE IF E ELIFS QUE VÃO CHECANDO AS CONDIÇÕES PARA TODOS OS TIPOS DE MOVIMENTO, SE TODAS ELAS FOREM ACEITAS, A VARIÁVEL "VALIDO", SERA VERDADEIRA

        #O PRIMEIRO IF VERIFICA SE É UM MOVIMENTO NORMAL DE UMA PEÇA NORMAL, OLHANDO AS CONDIÇÕES PARA QUE ELE ACONTEÇA
        if matriz[linha_inicio][coluna_inicio]=="o" and (((linha_final==linha_inicio+2) and (coluna_final==coluna_inicio+1 or coluna_final==coluna_inicio-1))) and matriz[linha_final][coluna_final]==" ":
            valido=True

        #OS DOIS ELIFS VERIFICAM SE É UM MOVIMENTO NORMAL DE UMA DAMA, OLHANDO AS CONDIÇÕES PARA QUE ELE ACONTEÇA 
        elif matriz[linha_inicio][coluna_inicio]=="O" and matriz[linha_final][coluna_final]==" "and ((linha_final+(coluna_inicio-coluna_final)-coluna_final)==(linha_inicio-coluna_inicio)) and z==True:
            valido=True
        elif matriz[linha_inicio][coluna_inicio]=="O" and matriz[linha_final][coluna_final]==" "and ((linha_final-(coluna_inicio-coluna_final)+coluna_final)==(linha_inicio+coluna_inicio)) and z==True:
            valido=True

        #O IF E O ELIF VERIFICAM SE É UM MOVIMENTO DE CAPTURA FEITO POR UMA PEÇA NORMAL
        if matriz[linha_inicio][coluna_inicio]=="o" and (linha_final==linha_inicio+4 and coluna_final==coluna_inicio+2 and (matriz[linha_final-2][coluna_final-1]=="@" or matriz[linha_final-2][coluna_final-1]=="&") or linha_final==linha_inicio-4 and coluna_final==coluna_inicio-2 and (matriz[linha_final+2][coluna_final+1]=="@" or matriz[linha_final+2][coluna_final+1]=="&")) and matriz[linha_final][coluna_final]==" ":
            valido=True
            captura=True
        elif matriz[linha_inicio][coluna_inicio]=="o" and (linha_final==linha_inicio+4 and coluna_final==coluna_inicio-2 and (matriz[linha_final-2][coluna_final+1]=="@" or matriz[linha_final-2][coluna_final+1]=="&") or linha_final==linha_inicio-4 and coluna_final==coluna_inicio+2 and (matriz[linha_final+2][coluna_final-1]=="@" or matriz[linha_final+2][coluna_final-1]=="&")) and matriz[linha_final][coluna_final]==" ":
            valido=True
            captura=True

        #OS PROXIMOS QUATRO ELIFS VERIFICAM SE É UM MOVIMENTO DE CAPTURA FEITO POR UMA DAMA
        elif matriz[linha_inicio][coluna_inicio]=="O" and matriz[linha_final][coluna_final]==" " and ((linha_final+(coluna_inicio-coluna_final)-coluna_final)==(linha_inicio-coluna_inicio)) and tem_comida_no_caminho1(matriz,linha_inicio,coluna_inicio)==True and linha_inicio-linha_final>2 and coluna_inicio-coluna_final>1 and ta_livre_pra_comer1(matriz,linha_inicio,coluna_inicio,linha_final,coluna_final)==True:
            valido=True
            captura_dama=True
        elif matriz[linha_inicio][coluna_inicio]=="O" and matriz[linha_final][coluna_final]==" " and ((linha_final+(coluna_inicio-coluna_final)-coluna_final)==(linha_inicio-coluna_inicio)) and tem_comida_no_caminho1(matriz,linha_inicio,coluna_inicio)==True and linha_final-linha_inicio>2 and coluna_final-coluna_inicio>1 and ta_livre_pra_comer1(matriz,linha_inicio,coluna_inicio,linha_final,coluna_final)==True:
            valido=True
            captura_dama=True
        elif matriz[linha_inicio][coluna_inicio]=="O" and matriz[linha_final][coluna_final]==" " and ((linha_final-(coluna_inicio-coluna_final)+coluna_final)==(linha_inicio+coluna_inicio)) and tem_comida_no_caminho1(matriz,linha_inicio,coluna_inicio)==True and linha_final-linha_inicio>2 and coluna_inicio-coluna_final>1 and ta_livre_pra_comer1(matriz,linha_inicio,coluna_inicio,linha_final,coluna_final)==True:
            valido=True
            captura_dama=True
        elif matriz[linha_inicio][coluna_inicio]=="O" and matriz[linha_final][coluna_final]==" " and ((linha_final-(coluna_inicio-coluna_final)+coluna_final)==(linha_inicio+coluna_inicio)) and tem_comida_no_caminho1(matriz,linha_inicio,coluna_inicio)==True and linha_inicio-linha_final>2 and coluna_final-coluna_inicio>1 and ta_livre_pra_comer1(matriz,linha_inicio,coluna_inicio,linha_final,coluna_final)==True:                                                                                        
            valido=True
            captura_dama=True


            #VERIFICANDO SE NÃO HÁ NENHUMA PEÇA QUE POSSA SER COMIDA, SE HOUVER, O JOGADOR É OBRIGADO A EXECUTAR O MOVIMENTO DE COMÊ-LA
        if (y==True or x==True) and captura==False and captura_dama==False:
            valido=False

        while valido==False:
            while True:
                try:
                    print("Jogada inválida, por favor, tente novamente")
                    #SE O MOVIMENTO NÃO FOR VÁLIDO, O CÓDIGO SE REPETE


                    entrada= input("Turno do Jogador de Cima, coloque a entrada na forma <COLUNA_INICIAL><LINHA_INICIAL>--<COLUNA_FINAL><LINHA_FINAL>\n").split("--")

                    cordenadas_inicio=converter(entrada[0])

                    coluna_inicio=(ord(cordenadas_inicio[0])-64)

                    linha_inicio=(int(cordenadas_inicio[1])*2+2)

                    cordenadas_final=converter(entrada[1])

                    coluna_final=(ord(cordenadas_final[0])-64)

                    linha_final=(int(cordenadas_final[1])*2+2)
                    break
                except (ValueError,IndexError):
                    print("insira uma entrada válida!")

            #ESSA VARIÁVEL FICA ATIVA SE UM MOVIMENTO É VÁLIDO
            valido=False

            #ESSA VARIÁVEL FICA ATIVA SE FOR UM MOVIMENTO DE CAPTURA
            captura=False

            #AS DUAS PRÓXIMAS VARIÁVEIS RECEBEM FUNÇÕES JÁ EXPLICADAS
            captura_dama=False
            x=dama_pode_comer1(matriz)
            y=pode_ser_comida2(matriz)
            z=dama_ta_livre(matriz,linha_inicio,coluna_inicio,linha_final,coluna_final)
            #VERIFICANDO SE O MOVIMENTO É VÁLIDO
            #SEGUEM UMA SEQUENCIA DE IF E ELIFS QUE VÃO CHECANDO AS CONDIÇÕES PARA TODOS OS TIPOS DE MOVIMENTO, SE TODAS ELAS FOREM ACEITAS, A VARIÁVEL "VALIDO", SERA VERDADEIRA

            #O PRIMEIRO IF VERIFICA SE É UM MOVIMENTO NORMAL DE UMA PEÇA NORMAL, OLHANDO AS CONDIÇÕES PARA QUE ELE ACONTEÇA
            if matriz[linha_inicio][coluna_inicio]=="o" and (((linha_final==linha_inicio+2) and (coluna_final==coluna_inicio+1 or coluna_final==coluna_inicio-1))) and matriz[linha_final][coluna_final]==" ":
                valido=True

            #OS DOIS ELIFS VERIFICAM SE É UM MOVIMENTO NORMAL DE UMA DAMA, OLHANDO AS CONDIÇÕES PARA QUE ELE ACONTEÇA 
            elif matriz[linha_inicio][coluna_inicio]=="O" and matriz[linha_final][coluna_final]==" "and ((linha_final+(coluna_inicio-coluna_final)-coluna_final)==(linha_inicio-coluna_inicio)) and z==True:
                valido=True
            elif matriz[linha_inicio][coluna_inicio]=="O" and matriz[linha_final][coluna_final]==" "and ((linha_final-(coluna_inicio-coluna_final)+coluna_final)==(linha_inicio+coluna_inicio)) and z==True:
                valido=True

            #O IF E O ELIF VERIFICAM SE É UM MOVIMENTO DE CAPTURA FEITO POR UMA PEÇA NORMAL
            if matriz[linha_inicio][coluna_inicio]=="o" and (linha_final==linha_inicio+4 and coluna_final==coluna_inicio+2 and (matriz[linha_final-2][coluna_final-1]=="@" or matriz[linha_final-2][coluna_final-1]=="&") or linha_final==linha_inicio-4 and coluna_final==coluna_inicio-2 and (matriz[linha_final+2][coluna_final+1]=="@" or matriz[linha_final+2][coluna_final+1]=="&")) and matriz[linha_final][coluna_final]==" ":
                valido=True
                captura=True
            elif matriz[linha_inicio][coluna_inicio]=="o" and (linha_final==linha_inicio+4 and coluna_final==coluna_inicio-2 and (matriz[linha_final-2][coluna_final+1]=="@" or matriz[linha_final-2][coluna_final+1]=="&") or linha_final==linha_inicio-4 and coluna_final==coluna_inicio+2 and (matriz[linha_final+2][coluna_final-1]=="@" or matriz[linha_final+2][coluna_final-1]=="&")) and matriz[linha_final][coluna_final]==" ":
                valido=True
                captura=True

            #OS PROXIMOS QUATRO ELIFS VERIFICAM SE É UM MOVIMENTO DE CAPTURA FEITO POR UMA DAMA
            elif matriz[linha_inicio][coluna_inicio]=="O" and matriz[linha_final][coluna_final]==" " and ((linha_final+(coluna_inicio-coluna_final)-coluna_final)==(linha_inicio-coluna_inicio)) and tem_comida_no_caminho1(matriz,linha_inicio,coluna_inicio)==True and linha_inicio-linha_final>2 and coluna_inicio-coluna_final>1 and ta_livre_pra_comer1(matriz,linha_inicio,coluna_inicio,linha_final,coluna_final)==True:
                valido=True
                captura_dama=True
            elif matriz[linha_inicio][coluna_inicio]=="O" and matriz[linha_final][coluna_final]==" " and ((linha_final+(coluna_inicio-coluna_final)-coluna_final)==(linha_inicio-coluna_inicio)) and tem_comida_no_caminho1(matriz,linha_inicio,coluna_inicio)==True and linha_final-linha_inicio>2 and coluna_final-coluna_inicio>1 and ta_livre_pra_comer1(matriz,linha_inicio,coluna_inicio,linha_final,coluna_final)==True:
                valido=True
                captura_dama=True
            elif matriz[linha_inicio][coluna_inicio]=="O" and matriz[linha_final][coluna_final]==" " and ((linha_final-(coluna_inicio-coluna_final)+coluna_final)==(linha_inicio+coluna_inicio)) and tem_comida_no_caminho1(matriz,linha_inicio,coluna_inicio)==True and linha_final-linha_inicio>2 and coluna_inicio-coluna_final>1 and ta_livre_pra_comer1(matriz,linha_inicio,coluna_inicio,linha_final,coluna_final)==True:
                valido=True
                captura_dama=True
            elif matriz[linha_inicio][coluna_inicio]=="O" and matriz[linha_final][coluna_final]==" " and ((linha_final-(coluna_inicio-coluna_final)+coluna_final)==(linha_inicio+coluna_inicio)) and tem_comida_no_caminho1(matriz,linha_inicio,coluna_inicio)==True and linha_inicio-linha_final>2 and coluna_final-coluna_inicio>1 and ta_livre_pra_comer1(matriz,linha_inicio,coluna_inicio,linha_final,coluna_final)==True:                                                                                        
                valido=True
                captura_dama=True


            #VERIFICANDO SE NÃO HÁ NENHUMA PEÇA QUE POSSA SER COMIDA, SE HOUVER, O JOGADOR É OBRIGADO A EXECUTAR O MOVIMENTO DE COMÊ-LA
            if (y==True or x==True) and captura==False and captura_dama==False:
                valido=False

        #PARA EXECUTAR O MOVIMENTO O MOVIMENTO, TROCA-SE DE LUGAR O ELEMENTOS DAS CORDENADAS INICIAIS COM O ELEMENTO DAS CORDENADAS FINAIS
        aux=matriz[linha_inicio][coluna_inicio]
        matriz[linha_inicio][coluna_inicio]=matriz[linha_final][coluna_final]
        matriz[linha_final][coluna_final]=aux
        global quantidade_de_movimentos 
        quantidade_de_movimentos= quantidade_de_movimentos + 1
        if captura==True:
            #SE O MOVIMENTO FOR DE CAPTURA, ALÉM DE MOVER A PEÇA, APAGA-SE A PEÇA QUE FOI COMIDA.
            #EM CADA SITUAÇÃO, AS CORDENADAS DE CAPTURA GUARDAM A LOCALIZAÇÃO DA PEÇA CAPTURADA
            if coluna_final>coluna_inicio and linha_final>linha_inicio:
                coluna_captura=coluna_final-1
                linha_captura=linha_final-2

            elif coluna_final<coluna_inicio and linha_final<linha_inicio:
                coluna_captura=coluna_final+1
                linha_captura=linha_final+2

            elif coluna_final>coluna_inicio and linha_final<linha_inicio:
                coluna_captura=coluna_final-1
                linha_captura=linha_final+2

            elif coluna_final<coluna_inicio and linha_final>linha_inicio:
                coluna_captura=coluna_final+1
                linha_captura=linha_final-2

            #POR FIM, APAGA-SE O ELEMENTO QUE ESTAVA NAS CORDENADAS DE CAPTURA
            
            matriz[linha_captura][coluna_captura]=" "
            quantidade_de_peças2 = quantidade_de_peças2 - 1
            
            #VERIFICANDO SE UMA DAMA FOI FEITA NA CAPTURA
            matriz=eh_dama(matriz)

            #A FUNÇÃO É EXECUTADA NOVAMENTE
            print_tabuleiro(matriz)
            print("Você comeu uma peça! Jogue novamente.")
            jogada_player1(matriz)

        elif captura_dama==True:
            #SE UMA DAMA CAPTURAR, A DIAGONAL SE TORNA VAZIA
            esvaziar_caminho(matriz,linha_inicio,coluna_inicio,linha_final,coluna_final)
            quantidade_de_peças2 = quantidade_de_peças2 - 1
            matriz=eh_dama(matriz)
            print_tabuleiro(matriz)
            print("Você comeu uma peça! Jogue novamente.")
            jogada_player1(matriz)

        return matriz

def jogada_player2(matriz):
    global quantidade_de_peças1
    if quantidade_de_peças1 != 0 and quantidade_de_peças2 != 0: 
        print("Você já comeu: ",15 - quantidade_de_peças1, "peças do jogador adversário.")
        '''Função que faz a jogada do player das peças "@"'''
        global modoOffline
        while True:
            try:
                entrada= input("Turno do Jogador de Baixo, coloque a entrada na forma <COLUNA_INICIAL><LINHA_INICIAL>--<COLUNA_FINAL><LINHA_FINAL>\n").split("--")
                cordenadas_inicio=converter(entrada[0])

                coluna_inicio=(ord(cordenadas_inicio[0])-64)

                linha_inicio=(int(cordenadas_inicio[1])*2+2)

                cordenadas_final=converter(entrada[1])

                coluna_final=(ord(cordenadas_final[0])-64)

                linha_final=(int(cordenadas_final[1])*2+2)
                break
            except (ValueError,IndexError):
                print("Insira uma entrada válida!")
        valido=False
        captura=False
        captura_dama=False

        x=dama_pode_comer2(matriz)
        y=pode_ser_comida1(matriz)
        print(x,y)
        z=dama_ta_livre(matriz,linha_inicio,coluna_inicio,linha_final,coluna_final)
        #MOVIMENTO NORMAL DE PEÇA NORMAL
        if matriz[linha_inicio][coluna_inicio]=="@" and (((linha_final==linha_inicio-2) and (coluna_final==coluna_inicio+1 or coluna_final==coluna_inicio-1))) and matriz[linha_final][coluna_final]==" ":
            valido=True

        #OS DOIS ELIFS VERIFICAM SE É UM MOVIMENTO NORMAL DE UMA DAMA, OLHANDO AS CONDIÇÕES PARA QUE ELE ACONTEÇA 
        elif matriz[linha_inicio][coluna_inicio]=="&" and matriz[linha_final][coluna_final]==" "and ((linha_final+(coluna_inicio-coluna_final)-coluna_final)==(linha_inicio-coluna_inicio)) and z==True:
            valido=True
        elif matriz[linha_inicio][coluna_inicio]=="&" and matriz[linha_final][coluna_final]==" "and ((linha_final-(coluna_inicio-coluna_final)+coluna_final)==(linha_inicio+coluna_inicio)) and z==True:
            valido=True

        #O IF E O ELIF VERIFICAM SE É UM MOVIMENTO DE CAPTURA FEITO POR UMA PEÇA NORMAL
        if matriz[linha_inicio][coluna_inicio]=="@" and (linha_final==linha_inicio+4 and coluna_final==coluna_inicio+2 and (matriz[linha_final-2][coluna_final-1]=="o" or matriz[linha_final-2][coluna_final-1]=="O") or linha_final==linha_inicio-4 and coluna_final==coluna_inicio-2 and (matriz[linha_final+2][coluna_final+1]=="o" or matriz[linha_final+2][coluna_final+1]=="O")) and matriz[linha_final][coluna_final]==" ":
            valido=True
            captura=True
        elif matriz[linha_inicio][coluna_inicio]=="@" and (linha_final==linha_inicio+4 and coluna_final==coluna_inicio-2 and (matriz[linha_final-2][coluna_final+1]=="o" or matriz[linha_final-2][coluna_final+1]=="O") or linha_final==linha_inicio-4 and coluna_final==coluna_inicio+2 and (matriz[linha_final+2][coluna_final-1]=="o" or matriz[linha_final+2][coluna_final-1]=="O")) and matriz[linha_final][coluna_final]==" ":
            valido=True
            captura=True

        #OS PROXIMOS QUATRO ELIFS VERIFICAM SE É UM MOVIMENTO DE CAPTURA FEITO POR UMA DAMA
        elif matriz[linha_inicio][coluna_inicio]=="&" and matriz[linha_final][coluna_final]==" " and ((linha_final+(coluna_inicio-coluna_final)-coluna_final)==(linha_inicio-coluna_inicio)) and tem_comida_no_caminho2(matriz,linha_inicio,coluna_inicio)==True and linha_inicio-linha_final>2 and coluna_inicio-coluna_final>1 and ta_livre_pra_comer2(matriz,linha_inicio,coluna_inicio,linha_final,coluna_final)==True:
            valido=True
            captura_dama=True
        elif matriz[linha_inicio][coluna_inicio]=="&" and matriz[linha_final][coluna_final]==" " and ((linha_final+(coluna_inicio-coluna_final)-coluna_final)==(linha_inicio-coluna_inicio)) and tem_comida_no_caminho2(matriz,linha_inicio,coluna_inicio)==True and linha_final-linha_inicio>2 and coluna_final-coluna_inicio>1 and ta_livre_pra_comer2(matriz,linha_inicio,coluna_inicio,linha_final,coluna_final)==True:
            valido=True
            captura_dama=True
        elif matriz[linha_inicio][coluna_inicio]=="&" and matriz[linha_final][coluna_final]==" " and ((linha_final-(coluna_inicio-coluna_final)+coluna_final)==(linha_inicio+coluna_inicio)) and tem_comida_no_caminho2(matriz,linha_inicio,coluna_inicio)==True and linha_final-linha_inicio>2 and coluna_inicio-coluna_final>1 and ta_livre_pra_comer2(matriz,linha_inicio,coluna_inicio,linha_final,coluna_final)==True:
            valido=True
            captura_dama=True
        elif matriz[linha_inicio][coluna_inicio]=="&" and matriz[linha_final][coluna_final]==" " and ((linha_final-(coluna_inicio-coluna_final)+coluna_final)==(linha_inicio+coluna_inicio)) and tem_comida_no_caminho2(matriz,linha_inicio,coluna_inicio)==True and linha_inicio-linha_final>2 and coluna_final-coluna_inicio>1 and ta_livre_pra_comer2(matriz,linha_inicio,coluna_inicio,linha_final,coluna_final)==True:                                                                                        
            valido=True
            captura_dama=True
        print(captura_dama)


        #SE HOUVER UMA PEÇA QUE POSSA SER CAPTURADA, O JOGADOR É OBRIGADO A FAZER ISSO
        if (x==True or y==True) and captura==False and captura_dama==False:
            valido=False

        while valido==False:
            while True:
                try:
                    print("Jogada inválida, por favor, tente novamente")
                    #SE O MOVIMENTO NÃO FOR VÁLIDO, O CÓDIGO SE REPETE


                    entrada= input("Turno do Jogador de Baixo, coloque a entrada na forma <COLUNA_INICIAL><LINHA_INICIAL>--<COLUNA_FINAL><LINHA_FINAL>\n").split("--")

                    cordenadas_inicio=converter(entrada[0])

                    coluna_inicio=(ord(cordenadas_inicio[0])-64)

                    linha_inicio=(int(cordenadas_inicio[1])*2+2)

                    cordenadas_final=converter(entrada[1])

                    coluna_final=(ord(cordenadas_final[0])-64)

                    linha_final=(int(cordenadas_final[1])*2+2)
                    break
                except (ValueError,IndexError):
                    print("insira uma entrada válida!")

            valido=False
            captura=False
            captura_dama=False

            x=dama_pode_comer2(matriz)
            y=pode_ser_comida1(matriz)
            print(x,y)
            z=dama_ta_livre(matriz,linha_inicio,coluna_inicio,linha_final,coluna_final)

            #MOVIMENTO NORMAL DE PEÇA NORMAL
            if matriz[linha_inicio][coluna_inicio]=="@" and (((linha_final==linha_inicio-2) and (coluna_final==coluna_inicio+1 or coluna_final==coluna_inicio-1))) and matriz[linha_final][coluna_final]==" ":
                valido=True

            #OS DOIS ELIFS VERIFICAM SE É UM MOVIMENTO NORMAL DE UMA DAMA, OLHANDO AS CONDIÇÕES PARA QUE ELE ACONTEÇA 
            elif matriz[linha_inicio][coluna_inicio]=="&" and matriz[linha_final][coluna_final]==" "and ((linha_final+(coluna_inicio-coluna_final)-coluna_final)==(linha_inicio-coluna_inicio)) and z==True:
                valido=True
            elif matriz[linha_inicio][coluna_inicio]=="&" and matriz[linha_final][coluna_final]==" "and ((linha_final-(coluna_inicio-coluna_final)+coluna_final)==(linha_inicio+coluna_inicio)) and z==True:
                valido=True

            #O IF E O ELIF VERIFICAM SE É UM MOVIMENTO DE CAPTURA FEITO POR UMA PEÇA NORMAL
            if matriz[linha_inicio][coluna_inicio]=="@" and (linha_final==linha_inicio+4 and coluna_final==coluna_inicio+2 and (matriz[linha_final-2][coluna_final-1]=="o" or matriz[linha_final-2][coluna_final-1]=="O") or linha_final==linha_inicio-4 and coluna_final==coluna_inicio-2 and (matriz[linha_final+2][coluna_final+1]=="o" or matriz[linha_final+2][coluna_final+1]=="O")) and matriz[linha_final][coluna_final]==" ":
                valido=True
                captura=True
            elif matriz[linha_inicio][coluna_inicio]=="@" and (linha_final==linha_inicio+4 and coluna_final==coluna_inicio-2 and (matriz[linha_final-2][coluna_final+1]=="o" or matriz[linha_final-2][coluna_final+1]=="O") or linha_final==linha_inicio-4 and coluna_final==coluna_inicio+2 and (matriz[linha_final+2][coluna_final-1]=="o" or matriz[linha_final+2][coluna_final-1]=="O")) and matriz[linha_final][coluna_final]==" ":
                valido=True
                captura=True

            #OS PROXIMOS QUATRO ELIFS VERIFICAM SE É UM MOVIMENTO DE CAPTURA FEITO POR UMA DAMA
            elif matriz[linha_inicio][coluna_inicio]=="&" and matriz[linha_final][coluna_final]==" " and ((linha_final+(coluna_inicio-coluna_final)-coluna_final)==(linha_inicio-coluna_inicio)) and tem_comida_no_caminho2(matriz,linha_inicio,coluna_inicio)==True and linha_inicio-linha_final>2 and coluna_inicio-coluna_final>1 and ta_livre_pra_comer2(matriz,linha_inicio,coluna_inicio,linha_final,coluna_final)==True:
                valido=True
                captura_dama=True
            elif matriz[linha_inicio][coluna_inicio]=="&" and matriz[linha_final][coluna_final]==" " and ((linha_final+(coluna_inicio-coluna_final)-coluna_final)==(linha_inicio-coluna_inicio)) and tem_comida_no_caminho2(matriz,linha_inicio,coluna_inicio)==True and linha_final-linha_inicio>2 and coluna_final-coluna_inicio>1 and ta_livre_pra_comer2(matriz,linha_inicio,coluna_inicio,linha_final,coluna_final)==True:
                valido=True
                captura_dama=True
            elif matriz[linha_inicio][coluna_inicio]=="&" and matriz[linha_final][coluna_final]==" " and ((linha_final-(coluna_inicio-coluna_final)+coluna_final)==(linha_inicio+coluna_inicio)) and tem_comida_no_caminho2(matriz,linha_inicio,coluna_inicio)==True and linha_final-linha_inicio>2 and coluna_inicio-coluna_final>1 and ta_livre_pra_comer2(matriz,linha_inicio,coluna_inicio,linha_final,coluna_final)==True:
                valido=True
                captura_dama=True
            elif matriz[linha_inicio][coluna_inicio]=="&" and matriz[linha_final][coluna_final]==" " and ((linha_final-(coluna_inicio-coluna_final)+coluna_final)==(linha_inicio+coluna_inicio)) and tem_comida_no_caminho2(matriz,linha_inicio,coluna_inicio)==True and linha_inicio-linha_final>2 and coluna_final-coluna_inicio>1 and ta_livre_pra_comer2(matriz,linha_inicio,coluna_inicio,linha_final,coluna_final)==True:                                                                                        
                valido=True
                captura_dama=True
            #SE HOUVER UMA PEÇA QUE POSSA SER CAPTURADA, O JOGADOR É OBRIGADO A FAZER ISSO
            if (x==True or y==True) and captura==False and captura_dama==False:
                valido=False
        
        aux=matriz[linha_inicio][coluna_inicio]
        matriz[linha_inicio][coluna_inicio]=matriz[linha_final][coluna_final]
        matriz[linha_final][coluna_final]=aux
        global quantidade_de_movimentos 
        quantidade_de_movimentos= quantidade_de_movimentos + 1
        if captura==True:

            if coluna_final>coluna_inicio and linha_final>linha_inicio:
                coluna_captura=coluna_final-1
                linha_captura=linha_final-2

            elif coluna_final<coluna_inicio and linha_final<linha_inicio:
                coluna_captura=coluna_final+1
                linha_captura=linha_final+2

            elif coluna_final>coluna_inicio and linha_final<linha_inicio:
                coluna_captura=coluna_final-1
                linha_captura=linha_final+2

            elif coluna_final<coluna_inicio and linha_final>linha_inicio:
                coluna_captura=coluna_final+1
                linha_captura=linha_final-2
            
            matriz[linha_captura][coluna_captura]=" "
            quantidade_de_peças1= quantidade_de_peças1 - 1

            matriz=eh_dama(matriz)
            
            print_tabuleiro(matriz)
            print("Você comeu uma peça! Jogue novamente.")
            jogada_player2(matriz)
        elif captura_dama==True:
            #SE UMA DAMA CAPTURAR, A DIAGONAL SE TORNA VAZIA
            esvaziar_caminho(matriz,linha_inicio,coluna_inicio,linha_final,coluna_final)

            quantidade_de_peças1= quantidade_de_peças1 - 1
            matriz=eh_dama(matriz)
            print_tabuleiro(matriz)
            print("Você comeu uma peça! Jogue novamente.")
            jogada_player2(matriz)
        
        return matriz

def jogadaoffline_player1(matriz,jogadas):
    '''Função que faz a jogada do player das peças "o"'''
    global quantidade_de_peças2
    
    #PEGANDO O INPUT E O DIVIDINDO EM DUAS PARTES, AS CORDENADAS DE INICIO E AS CORDENADAS FINAIS
    global jogaCima
    if quantidade_de_peças1 != 0 and quantidade_de_peças2 != 0: 
        entrada=jogadas.split("--")

        cordenadas_inicio=converter(entrada[0])

        coluna_inicio=(ord(cordenadas_inicio[0])-64)

        linha_inicio=(int(cordenadas_inicio[1])*2+2)

        cordenadas_final=converter(entrada[1])

        coluna_final=(ord(cordenadas_final[0])-64)

        linha_final=(int(cordenadas_final[1])*2+2)

        #ESSA VARIÁVEL FICA ATIVA SE UM MOVIMENTO É VÁLIDO
        valido=False

        #ESSA VARIÁVEL FICA ATIVA SE FOR UM MOVIMENTO DE CAPTURA
        captura=False

        #AS DUAS PRÓXIMAS VARIÁVEIS RECEBEM FUNÇÕES JÁ EXPLICADAS
        captura_dama=False
        x=dama_pode_comer1(matriz)
        y=pode_ser_comida1(matriz)
        z=dama_ta_livre(matriz,linha_inicio,coluna_inicio,linha_final,coluna_final)
        #VERIFICANDO SE O MOVIMENTO É VÁLIDO
        #SEGUEM UMA SEQUENCIA DE IF E ELIFS QUE VÃO CHECANDO AS CONDIÇÕES PARA TODOS OS TIPOS DE MOVIMENTO, SE TODAS ELAS FOREM ACEITAS, A VARIÁVEL "VALIDO", SERA VERDADEIRA

        #O PRIMEIRO IF VERIFICA SE É UM MOVIMENTO NORMAL DE UMA PEÇA NORMAL, OLHANDO AS CONDIÇÕES PARA QUE ELE ACONTEÇA
        if matriz[linha_inicio][coluna_inicio]=="o" and (((linha_final==linha_inicio+2) and (coluna_final==coluna_inicio+1 or coluna_final==coluna_inicio-1))) and matriz[linha_final][coluna_final]==" ":
            valido=True

        #OS DOIS ELIFS VERIFICAM SE É UM MOVIMENTO NORMAL DE UMA DAMA, OLHANDO AS CONDIÇÕES PARA QUE ELE ACONTEÇA 
        elif matriz[linha_inicio][coluna_inicio]=="O" and matriz[linha_final][coluna_final]==" "and ((linha_final+(coluna_inicio-coluna_final)-coluna_final)==(linha_inicio-coluna_inicio)) and z==True:
            valido=True
        elif matriz[linha_inicio][coluna_inicio]=="O" and matriz[linha_final][coluna_final]==" "and ((linha_final-(coluna_inicio-coluna_final)+coluna_final)==(linha_inicio+coluna_inicio)) and z==True:
            valido=True

        #O IF E O ELIF VERIFICAM SE É UM MOVIMENTO DE CAPTURA FEITO POR UMA PEÇA NORMAL
        if matriz[linha_inicio][coluna_inicio]=="o" and (linha_final==linha_inicio+4 and coluna_final==coluna_inicio+2 and (matriz[linha_final-2][coluna_final-1]=="@" or matriz[linha_final-2][coluna_final-1]=="&") or linha_final==linha_inicio-4 and coluna_final==coluna_inicio-2 and (matriz[linha_final+2][coluna_final+1]=="@" or matriz[linha_final+2][coluna_final+1]=="&")) and matriz[linha_final][coluna_final]==" ":
            valido=True
            captura=True
        elif matriz[linha_inicio][coluna_inicio]=="o" and (linha_final==linha_inicio+4 and coluna_final==coluna_inicio-2 and (matriz[linha_final-2][coluna_final+1]=="@" or matriz[linha_final-2][coluna_final+1]=="&") or linha_final==linha_inicio-4 and coluna_final==coluna_inicio+2 and (matriz[linha_final+2][coluna_final-1]=="@" or matriz[linha_final+2][coluna_final-1]=="&")) and matriz[linha_final][coluna_final]==" ":
            valido=True
            captura=True

        #OS PROXIMOS QUATRO ELIFS VERIFICAM SE É UM MOVIMENTO DE CAPTURA FEITO POR UMA DAMA
        elif matriz[linha_inicio][coluna_inicio]=="O" and matriz[linha_final][coluna_final]==" " and ((linha_final+(coluna_inicio-coluna_final)-coluna_final)==(linha_inicio-coluna_inicio)) and tem_comida_no_caminho1(matriz,linha_inicio,coluna_inicio)==True and linha_inicio-linha_final>2 and coluna_inicio-coluna_final>1 and ta_livre_pra_comer1(matriz,linha_inicio,coluna_inicio,linha_final,coluna_final)==True:
            valido=True
            captura_dama=True
        elif matriz[linha_inicio][coluna_inicio]=="O" and matriz[linha_final][coluna_final]==" " and ((linha_final+(coluna_inicio-coluna_final)-coluna_final)==(linha_inicio-coluna_inicio)) and tem_comida_no_caminho1(matriz,linha_inicio,coluna_inicio)==True and linha_final-linha_inicio>2 and coluna_final-coluna_inicio>1 and ta_livre_pra_comer1(matriz,linha_inicio,coluna_inicio,linha_final,coluna_final)==True:
            valido=True
            captura_dama=True
        elif matriz[linha_inicio][coluna_inicio]=="O" and matriz[linha_final][coluna_final]==" " and ((linha_final-(coluna_inicio-coluna_final)+coluna_final)==(linha_inicio+coluna_inicio)) and tem_comida_no_caminho1(matriz,linha_inicio,coluna_inicio)==True and linha_final-linha_inicio>2 and coluna_inicio-coluna_final>1 and ta_livre_pra_comer1(matriz,linha_inicio,coluna_inicio,linha_final,coluna_final)==True:
            valido=True
            captura_dama=True
        elif matriz[linha_inicio][coluna_inicio]=="O" and matriz[linha_final][coluna_final]==" " and ((linha_final-(coluna_inicio-coluna_final)+coluna_final)==(linha_inicio+coluna_inicio)) and tem_comida_no_caminho1(matriz,linha_inicio,coluna_inicio)==True and linha_inicio-linha_final>2 and coluna_final-coluna_inicio>1 and ta_livre_pra_comer1(matriz,linha_inicio,coluna_inicio,linha_final,coluna_final)==True:                                                                                        
            valido=True
            captura_dama=True

        #VERIFICANDO SE NÃO HÁ NENHUMA PEÇA QUE POSSA SER COMIDA, SE HOUVER, O JOGADOR É OBRIGADO A EXECUTAR O MOVIMENTO DE COMÊ-LA
        if (y==True or x==True) and captura==False and captura_dama==False:
            valido=False

        if valido==False:
            jogaCima=False
        if valido:
            #PARA EXECUTAR O MOVIMENTO, TROCA-SE DE LUGAR O ELEMENTOS DAS CORDENADAS INICIAIS COM O ELEMENTO DAS CORDENADAS FINAIS
            aux=matriz[linha_inicio][coluna_inicio]
            matriz[linha_inicio][coluna_inicio]=matriz[linha_final][coluna_final]
            matriz[linha_final][coluna_final]=aux
            global quantidade_de_movimentos 
            quantidade_de_movimentos= quantidade_de_movimentos + 1
            if captura==True:
                #SE O MOVIMENTO FOR DE CAPTURA, ALÉM DE MOVER A PEÇA, APAGA-SE A PEÇA QUE FOI COMIDA.
                #EM CADA SITUAÇÃO, AS CORDENADAS DE CAPTURA GUARDAM A LOCALIZAÇÃO DA PEÇA CAPTURADA
                if coluna_final>coluna_inicio and linha_final>linha_inicio:
                    coluna_captura=coluna_final-1
                    linha_captura=linha_final-2

                elif coluna_final<coluna_inicio and linha_final<linha_inicio:
                    coluna_captura=coluna_final+1
                    linha_captura=linha_final+2

                elif coluna_final>coluna_inicio and linha_final<linha_inicio:
                    coluna_captura=coluna_final-1
                    linha_captura=linha_final+2

                elif coluna_final<coluna_inicio and linha_final>linha_inicio:
                    coluna_captura=coluna_final+1
                    linha_captura=linha_final-2

                #POR FIM, APAGA-SE O ELEMENTO QUE ESTAVA NAS CORDENADAS DE CAPTURA
                matriz[linha_captura][coluna_captura]=" "
                matriz=eh_dama(matriz)
                quantidade_de_peças2 = quantidade_de_peças2 - 1
                #SE UMA PEÇA FOI CAPTURADA, A FUNÇÃO É EXECUTADA NOVAMENTE
                jogaCima=True

            elif captura_dama==True:
                #SE UMA DAMA CAPTURAR, A DIAGONAL SE TORNA VAZIA
                esvaziar_caminho(matriz,linha_inicio,coluna_inicio,linha_final,coluna_final)

                quantidade_de_peças2= quantidade_de_peças2 - 1
                jogaCima=True
            
            if captura==False:
                jogaCima=False

        return matriz, valido

def jogadaoffline_player2(matriz,jogadas):
    '''Função que faz a jogada do player das peças "@"'''
    global quantidade_de_peças1 
    global jogaCima
    global quantidade_de_peças1
    if quantidade_de_peças1 != 0 and quantidade_de_peças2 != 0: 
        entrada=jogadas.split("--")

        cordenadas_inicio=converter(entrada[0])

        coluna_inicio=(ord(cordenadas_inicio[0])-64)

        linha_inicio=(int(cordenadas_inicio[1])*2+2)

        cordenadas_final=converter(entrada[1])

        coluna_final=(ord(cordenadas_final[0])-64)

        linha_final=(int(cordenadas_final[1])*2+2)

        valido=False
        captura=False
        captura_dama=False

        x=dama_pode_comer2(matriz)
        y=pode_ser_comida1(matriz)
        z=dama_ta_livre(matriz,linha_inicio,coluna_inicio,linha_final,coluna_final)
        #MOVIMENTO NORMAL DE PEÇA NORMAL
        if matriz[linha_inicio][coluna_inicio]=="@" and (((linha_final==linha_inicio-2) and (coluna_final==coluna_inicio+1 or coluna_final==coluna_inicio-1))) and matriz[linha_final][coluna_final]==" ":
            valido=True

        #OS DOIS ELIFS VERIFICAM SE É UM MOVIMENTO NORMAL DE UMA DAMA, OLHANDO AS CONDIÇÕES PARA QUE ELE ACONTEÇA 
        elif matriz[linha_inicio][coluna_inicio]=="&" and matriz[linha_final][coluna_final]==" "and ((linha_final+(coluna_inicio-coluna_final)-coluna_final)==(linha_inicio-coluna_inicio)) and z==True:
            valido=True
        elif matriz[linha_inicio][coluna_inicio]=="&" and matriz[linha_final][coluna_final]==" "and ((linha_final-(coluna_inicio-coluna_final)+coluna_final)==(linha_inicio+coluna_inicio)) and z==True:
            valido=True

        #O IF E O ELIF VERIFICAM SE É UM MOVIMENTO DE CAPTURA FEITO POR UMA PEÇA NORMAL
        if matriz[linha_inicio][coluna_inicio]=="@" and (linha_final==linha_inicio+4 and coluna_final==coluna_inicio+2 and (matriz[linha_final-2][coluna_final-1]=="o" or matriz[linha_final-2][coluna_final-1]=="O") or linha_final==linha_inicio-4 and coluna_final==coluna_inicio-2 and (matriz[linha_final+2][coluna_final+1]=="o" or matriz[linha_final+2][coluna_final+1]=="O")) and matriz[linha_final][coluna_final]==" ":
            valido=True
            captura=True
        elif matriz[linha_inicio][coluna_inicio]=="@" and (linha_final==linha_inicio+4 and coluna_final==coluna_inicio-2 and (matriz[linha_final-2][coluna_final+1]=="o" or matriz[linha_final-2][coluna_final+1]=="O") or linha_final==linha_inicio-4 and coluna_final==coluna_inicio+2 and (matriz[linha_final+2][coluna_final-1]=="o" or matriz[linha_final+2][coluna_final-1]=="O")) and matriz[linha_final][coluna_final]==" ":
            valido=True
            captura=True

        #OS PROXIMOS QUATRO ELIFS VERIFICAM SE É UM MOVIMENTO DE CAPTURA FEITO POR UMA DAMA
        elif matriz[linha_inicio][coluna_inicio]=="&" and matriz[linha_final][coluna_final]==" " and ((linha_final+(coluna_inicio-coluna_final)-coluna_final)==(linha_inicio-coluna_inicio)) and tem_comida_no_caminho2(matriz,linha_inicio,coluna_inicio)==True and linha_inicio-linha_final>2 and coluna_inicio-coluna_final>1 and ta_livre_pra_comer2(matriz,linha_inicio,coluna_inicio,linha_final,coluna_final)==True:
            valido=True
            captura_dama=True
        elif matriz[linha_inicio][coluna_inicio]=="&" and matriz[linha_final][coluna_final]==" " and ((linha_final+(coluna_inicio-coluna_final)-coluna_final)==(linha_inicio-coluna_inicio)) and tem_comida_no_caminho2(matriz,linha_inicio,coluna_inicio)==True and linha_final-linha_inicio>2 and coluna_final-coluna_inicio>1 and ta_livre_pra_comer2(matriz,linha_inicio,coluna_inicio,linha_final,coluna_final)==True:
            valido=True
            captura_dama=True
        elif matriz[linha_inicio][coluna_inicio]=="&" and matriz[linha_final][coluna_final]==" " and ((linha_final-(coluna_inicio-coluna_final)+coluna_final)==(linha_inicio+coluna_inicio)) and tem_comida_no_caminho2(matriz,linha_inicio,coluna_inicio)==True and linha_final-linha_inicio>2 and coluna_inicio-coluna_final>1 and ta_livre_pra_comer2(matriz,linha_inicio,coluna_inicio,linha_final,coluna_final)==True:
            valido=True
            captura_dama=True
        elif matriz[linha_inicio][coluna_inicio]=="&" and matriz[linha_final][coluna_final]==" " and ((linha_final-(coluna_inicio-coluna_final)+coluna_final)==(linha_inicio+coluna_inicio)) and tem_comida_no_caminho2(matriz,linha_inicio,coluna_inicio)==True and linha_inicio-linha_final>2 and coluna_final-coluna_inicio>1 and ta_livre_pra_comer2(matriz,linha_inicio,coluna_inicio,linha_final,coluna_final)==True:                                                                                        
            valido=True
            captura_dama=True

        #SE HOUVER UMA PEÇA QUE POSSA SER CAPTURADA, O JOGADOR É OBRIGADO A FAZER ISSO
        if (x==True or y==True) and captura==False and captura_dama==False:
            valido=False

        if valido==False:
            jogaCima=True
        
        if valido:
            aux=matriz[linha_inicio][coluna_inicio]
            matriz[linha_inicio][coluna_inicio]=matriz[linha_final][coluna_final]
            matriz[linha_final][coluna_final]=aux
            global quantidade_de_movimentos 
            quantidade_de_movimentos= quantidade_de_movimentos + 1
            if captura==True:

                if coluna_final>coluna_inicio and linha_final>linha_inicio:
                    coluna_captura=coluna_final-1
                    linha_captura=linha_final-2

                elif coluna_final<coluna_inicio and linha_final<linha_inicio:
                    coluna_captura=coluna_final+1
                    linha_captura=linha_final+2

                elif coluna_final>coluna_inicio and linha_final<linha_inicio:
                    coluna_captura=coluna_final-1
                    linha_captura=linha_final+2

                elif coluna_final<coluna_inicio and linha_final>linha_inicio:
                    coluna_captura=coluna_final+1
                    linha_captura=linha_final-2
                
                matriz[linha_captura][coluna_captura]=" "
                quantidade_de_peças1= quantidade_de_peças1 - 1
                jogaCima=False

            elif captura_dama==True:
                #SE UMA DAMA CAPTURAR, A DIAGONAL SE TORNA VAZIA
                esvaziar_caminho(matriz,linha_inicio,coluna_inicio,linha_final,coluna_final)

                quantidade_de_peças1= quantidade_de_peças1 - 1
                jogaCima=False

            if captura==False:
                jogaCima=True
            
        return matriz, valido


if len(sys.argv)>1: #SE A LINHA DE COMANDO DO TERMINAL FOR MAIOR DO QUE 1 COMANDO (CHAMAR O PROGRAMA E HAVER UM ARQUIVO POR EXEMPLO) ELE ENTRA NESSA CONDICIONAL, QUE PROPICIA O MODO OFFLINE
    modoOffline=True
    with open(sys.argv[1], 'r') as entrada:
        jogadas=entrada.read() #LEMOS AS JOGADAS ...
    jogadasLista=jogadas.splitlines() #...TORNAMOS O CONJUNTO DAS JOGADAS UMA LISTA ...
    jogadasLista=[jogada.strip() for jogada in jogadasLista] #...E RETIRAMOS A QUEBRA DE LINHA DE CADA ELEMENTO DA LISTA.
    turno=1
    jogo=True
    matriz=(tabuleiro_inicio())
    jogador = jogadasLista[0]

    if jogador == "C":
        jogaCima=True
        while jogo:
            if quantidade_de_peças1==0 or quantidade_de_peças2==0 or jogadasLista[turno]=="<Enter>":
                jogo=False
                print_tabuleiro(matriz)
                print("Jogador de cima (o) comeu",15 - quantidade_de_peças2, "peças do jogador adversário.")
                print("Jogador de baixo (@) comeu",15 - quantidade_de_peças1, "peças do jogador adversário.")
                if quantidade_de_peças1==0:
                    print("Jogador de cima ganhou!")
                elif quantidade_de_peças2==0:
                    print("Jogador de baixo ganhou!")
                break
            elif jogaCima:
                matriz,valido=jogadaoffline_player1(matriz,jogadasLista[turno])
                if valido==False:
                    print("Há um erro na " + str(turno + 1) + "ª linha do arquivo durante a jogada do player 1.")
                matriz=eh_dama(matriz)
            elif jogaCima==False:
                matriz,valido=jogadaoffline_player2(matriz,jogadasLista[turno])
                if valido==False:
                    print("Há um erro na " + str(turno + 1) + "ª linha do arquivo durante a jogada do player 2.")
                matriz=eh_dama(matriz)
            turno+=1
            
    if jogador == "B":
        jogaCima=False
        while jogo:
            if quantidade_de_peças1==0 or quantidade_de_peças2==0 or jogadasLista[turno]=="<Enter>":
                jogo=False
                print_tabuleiro(matriz)
                print("Jogador de cima (o) comeu",15 - quantidade_de_peças2, "peças do jogador adversário.")
                print("Jogador de baixo (@) comeu",15 - quantidade_de_peças1, "peças do jogador adversário.")
                if quantidade_de_peças1==0:
                    print("Jogador de cima ganhou!")
                elif quantidade_de_peças2==0:
                    print("Jogador de baixo ganhou!")
                break
            elif jogaCima:
                matriz,valido=jogadaoffline_player1(matriz,jogadasLista[turno])
                if valido==False:
                    print("Há um erro na " + str(turno + 1) + "ª linha do arquivo durante a jogada do player 1.")
                matriz=eh_dama(matriz)
            elif jogaCima==False:
                matriz,valido=jogadaoffline_player2(matriz,jogadasLista[turno])
                if valido==False:
                    print("Há um erro na " + str(turno + 1) + "ª linha do arquivo durante a jogada do player 2.")
                matriz=eh_dama(matriz)
            turno+=1


    '''if jogadasLista[0]=="C":
        del jogadasLista[0]
        while jogo:
            if turno%2==0:
                matriz=jogada_player1(matriz)
                matriz=eh_dama(matriz)
                del jogadasLista[0]
            if turno%2==1:
                matriz=jogada_player2(matriz)
                matriz=eh_dama(matriz)
                del jogadasLista[0]
            if quantidade_de_peças1==0 or quantidade_de_peças2==0 or len(jogadasLista)==0:
                jogo=False
                print_tabuleiro(matriz)
    elif jogadasLista[0]=="B":
        del jogadasLista[0]
        while jogo:
            if turno%2==0:
                matriz=jogada_player2(matriz)
                matriz=eh_dama(matriz)
                del jogadasLista[0]
            if turno%2==1:
                matriz=jogada_player1(matriz)
                matriz=eh_dama(matriz)
                del jogadasLista[0]
            if quantidade_de_peças1==0 or quantidade_de_peças2==0 or len(jogadasLista)==0:
                jogo=False
                print_tabuleiro(matriz)
    print(jogadasLista)'''

else:
    while novamente_bool == True:
        modoOffline=False
        clear()
        quantidade_de_peças1 = 15
        quantidade_de_peças2 = 15
        turno=0
        jogo = True
        print("O tabuleiro inicial é:")

        #É PRINTADO O TABULEIRO INICIAL
        print_tabuleiro(tabuleiro_inicio())

        #É CRIADA UMA VARIÁVEL "MATRIZ" QUE RECEBERÁ O TABULEIRO
        matriz=(tabuleiro_inicio())
        #USUÁRIO ENTRA O CARACTERE "C" OU "B"
        jogador=input("Quem vai começar o jogo (C ou B):\n")

        while jogador!="C" and jogador!="B":

            #SE A ENTRADA NÃO FOR C OU B, O PROGRAMA PEDE POR UMA NOVA ENTRADA
            print("Entrada inválida, por favor, tente novamente")
            jogador=input("Quem vai começar o jogo (C ou B):\n")

        if jogador=="C":
            print("Ok, jogador de cima começa!")

            while jogo == True:
                if turno%2==0: #COMO O TURNO COMEÇA COM 0, ENTÃO AS JOGADAS PARES SERÃO DO JOGADOR 1 (O JOGADOR DE CIMA)
                    matriz=jogada_player1(matriz)

                    #CHECANDO SE NÃO HÁ POSSÍVEIS DAMAS
                    matriz=eh_dama(matriz)

                    clear()
                    print_tabuleiro(matriz)
                if turno%2==1: #E AS JOGADAS ÍMPARES SERÃO DO JOGADOR DE BAIXO, O JOGADOR 2
                    matriz=jogada_player2(matriz)

                    #CHECANDO SE NÃO HÁ POSSÍVEIS DAMAS
                    matriz=eh_dama(matriz)

                    clear()
                    print(15-quantidade_de_peças1,"foram comidas pelo jogador 2")
                    print_tabuleiro(matriz)
                if quantidade_de_peças1 == 0:
                    jogo = False
                if quantidade_de_peças2 == 0:
                    jogo = False
                turno+=1

        elif jogador=="B":
            print("Ok, jogador de baixo começa!")
            while jogo == True:
                if turno%2==0: #COMO O TURNO COMEÇA COM 0, ENTÃO AS JOGADAS PARES SERÃO DO JOGADOR 2 (O JOGADOR DE BAIXO)
                    matriz=jogada_player2(matriz)
                    matriz=eh_dama(matriz)
                    clear()
                    print_tabuleiro(matriz)
                if turno%2==1: #E AS JOGADAS ÍMPARES SERÃO DO JOGADOR DE CIMA, O JOGADOR 1
                    matriz=jogada_player1(matriz)

                    matriz=eh_dama(matriz)

                    clear()
                    print_tabuleiro(matriz)
                if quantidade_de_peças1 == 0:
                    jogo = False
                if quantidade_de_peças2 == 0:
                    jogo = False
                turno+=1
        if quantidade_de_peças1 == 0:
            print("O jogador 2 venceu!")
        if quantidade_de_peças2 == 0:
            print("O jogador 1 venceu!")
        novamente = int(input("Quer jogar outra partida? Digite 1 para sim e 0 para não. "))
        while (novamente != 1 and novamente != 0):
            novamente = int(input("Entrada incorreta, quer jogar outra partida? Digite 1 para sim ou 0 para nao. "))
        if novamente == 1:
            novamente_bool = True
        elif novamente == 0:
            novamente_bool = False
