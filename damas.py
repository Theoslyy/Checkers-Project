import numpy as np
def converter(string):
    x=[i for i in string]
    return x
def tabuleiro_inicio():
    print("A configuraçao é:")
    #inicializando a matriz
    matriz = np.zeros((23,12), dtype=str)
    #colocando as # na matriz de forma alternada
    matriz[::4, ::2] = "#"
    matriz[::4, 1::2] = " "
    matriz[2::4, ::2]=" "
    matriz[2::4, 1::2]="#"
    for i in range(23):
        for j in range(12):
            #colocando o íncice das colunas
            if (i==0 or i==22) and 0<j<=10:
                matriz[i][j]=chr(65+(j-1))
            #colocando o índice das linhas
            if (j==0 or j==11) and i%2==0 and (i!=0 and i!=22):
                matriz[i][j]=str((i/2)-1)
            #colocando as peças
            if 0<i<7 and ((i%4!=0 and j%2==0) or (i%4==0 and j%2==1)) and 0<j<11:
                matriz[i][j]="o"
            if 15<=i<22 and ((i%4!=0 and j%2==0) or (i%4==0 and j%2==1)) and 0<j<11:
                matriz[i][j]="@"
            #colocando os "-"" nas linhas ímpares
            if i%2==1 and (j!=0 or j!=11):
                matriz[i][j]="-"
            #deixando a primeira e última coluna vazias
            elif (j==0 or j==11):
                matriz[i][j]=" "
    return matriz
def print_tabuleiro(x):
    matriz=x
    for i in range(23):
        for j in range(12):
            #printando os elemenntos com seus respectivos separadores 
            if i%2==1 and (i!=0 and i!=22) and (j!=11):
                print(matriz[i][j], end="+")
            elif (i==0 or i ==22) or j==11:
                print(matriz[i][j], end=" ")
            else:
                print(matriz[i][j], end="|")
        print()
def dama(x):
    matriz=x
    #um for que passsa apenas pelas linhas 2 e 20
    for i in range(2,21,18):
        for j in range(12):
            #verificando a posição e a peça para ver se é dama e, se for, trocá-la pelio seu símbolo
            if (matriz[i][j]=="@" and i==2):
                matriz[i][j]="&"
            if (matriz[i][j]=="o" and i==20):
                matriz[i][j]="O"
    return x
def jogada_player1(x):
    matriz=x
    #recebendo o input completo e dividinddo-o em 2
    entrada=input().split("--")
    #pegando a primeira metade e a  dividindo novamente, obtendo a coluna e a linha iniciais, com uma conversão para que se possa trabalhar com elas na matriz
    cordenadas_inicio=converter(entrada[0])
    coluna_inicio=(ord(cordenadas_inicio[0])-64)
    linha_inicio=(int(cordenadas_inicio[1])*2+2)
    #faz-se a mesma coisa, só que agora para a segunda metade da entrada, obtendo a coluna e linha finais
    cordenadas_final=converter(entrada[1])
    coluna_final=(ord(cordenadas_final[0])-64)
    linha_final=(int(cordenadas_final[1])*2+2)
    valido=False
    #verificando as condições de validade (falta fazer com a dama e com a captura)
    if matriz[linha_inicio][coluna_inicio]=="o" and (((linha_final==linha_inicio+2) and (coluna_final==coluna_inicio+1 or coluna_final==coluna_inicio-1)) and matriz[linha_final][coluna_final]==" "):
        valido=True
    while valido==False:
        print("Input não aceito, por favor, tente novamente")
        #se as condições não forem cumpridas, o código se repetirá
        entrada=input().split("--")
        cordenadas_inicio=converter(entrada[0])
        coluna_inicio=(ord(cordenadas_inicio[0])-64)
        linha_inicio=(int(cordenadas_inicio[1])*2+2)
        cordenadas_final=converter(entrada[1])
        coluna_final=(ord(cordenadas_final[0])-64)
        linha_final=(int(cordenadas_final[1])*2+2)
        if  matriz[linha_inicio][coluna_inicio]=="o" and (((linha_final==linha_inicio+2) and (coluna_final==coluna_inicio+1 or coluna_final==coluna_inicio-1)) and matriz[linha_final][coluna_final]==" "):
            valido=True
