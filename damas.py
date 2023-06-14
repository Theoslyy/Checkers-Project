import numpy as np
def tabuleiro(n):
    print("A configuraçao é:")
    x = np.zeros((n,n), dtype=str)
    x[1::2, ::2] = "*"
    x[::2, 1::2] = "*"
    x[1::2, 1::2] = "%"
    x[::2, ::2]=  "%"
    for i in range(n):
        for j in range(n):
            if i == 0 and j+1<n:
                x[i][j+1]=chr(97+j)
            if j == 0 and i+1<n:
                x[i+1][j] = i
            print(x[i][j], end=" ")
        print()
tabuleiro(10)
