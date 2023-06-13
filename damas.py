import numpy as np
def tabuleiro(n):
    print("A configuraçao é:")
    x = np.zeros((n,n), dtype=str)
    x[1::2, ::2] = 1
    x[::2, 1::2] = 1
    x[1::2, 1::2] = 0
    x[::2, ::2]=0
    for i in range(n):
        for j in range(n):
            if i==0:
                x[i][j]=chr(97+j)
            print(x[i][j], end=" ")
        print()
tabuleiro(9)
