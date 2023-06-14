import numpy as np
def tabuleiro():
    print("A configuraçao é:")
    #inicializando a matriz
    x = np.zeros((23,12), dtype=str)
    x[::4, ::2] = "#"
    x[::4, 1::2] = " "
    x[2::4, ::2]=" "
    x[2::4, 1::2]="#"
    for i in range(23):
        for j in range(12):
            if (i==0 or i==22) and 0<j<=10:
                x[i][j]=chr(65+(j-1))
            if 0<i<7 and ((i%4!=0 and j%2==0) or (i%4==0 and j%2==1)) and 0<j<11:
                x[i][j]="o"
            if 15<=i<22 and ((i%4!=0 and j%2==0) or (i%4==0 and j%2==1)) and 0<j<11:
                x[i][j]="@"
            if i%2==1 and (j!=0 or j!=11):
                x[i][j]="-"
            if (j==0 or j==11) and i%2==0 and (i!=0 and i!=22):
                x[i][j]=str((i/2)-1)
            elif (j==0 or j==11):
                x[i][j]=" "
            if i%2==1 and (i!=0 and i!=22) and (j!=11):
                print(x[i][j], end="+")
            elif (i==0 or i ==22) or j==11:
                print(x[i][j], end=" ")
            else:
                print(x[i][j], end="|")
        print()
tabuleiro()
