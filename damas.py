import numpy as np
def converter(string):
    x=[i for i in string]
    return x
def tabuleiro_inicio():
    print("A configuraçao é:")
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
def dama(x):
    matriz=x
    for i in range(2,21,18):
        for j in range(12):
            if (matriz[i][j]=="@" and i==2):
                matriz[i][j]="&"
            if (matriz[i][j]=="o" and i==20):
                matriz[i][j]="O"
    return x
def jogada_player1(x):
    matriz=x
    entrada=input().split("--")
    cordenadas_inicio=converter(entrada[0])
    coluna_inicio=(ord(cordenadas_inicio[0])-64)
    linha_inicio=(int(cordenadas_inicio[1])*2+2)
    cordenadas_final=converter(entrada[1])
    coluna_final=(ord(cordenadas_final[0])-64)
    linha_final=(int(cordenadas_final[1])*2+2)
    valido=False
    if matriz[linha_inicio][coluna_inicio]=="o" and (((linha_final==linha_inicio+2) and (coluna_final==coluna_inicio+1 or coluna_final==coluna_inicio-1)) and matriz[linha_final][coluna_final]==" "):
        valido=True
    while valido==False:
        print("Input não aceito, por favor, tente novamente")
        entrada=input().split("--")
        cordenadas_inicio=converter(entrada[0])
        coluna_inicio=(ord(cordenadas_inicio[0])-64)
        linha_inicio=(int(cordenadas_inicio[1])*2+2)
        cordenadas_final=converter(entrada[1])
        coluna_final=(ord(cordenadas_final[0])-64)
        linha_final=(int(cordenadas_final[1])*2+2)
        if  matriz[linha_inicio][coluna_inicio]=="o" and (((linha_final==linha_inicio+2) and (coluna_final==coluna_inicio+1 or coluna_final==coluna_inicio-1)) and matriz[linha_final][coluna_final]==" "):
            valido=True
