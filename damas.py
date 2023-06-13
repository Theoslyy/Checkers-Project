import numpy as py
def tabuleiro(n):
    print("A configuraçao é:")
    x = np.zeros((n,n), dtype=int)
    x[1::2, ::2] = 1
    x[::2, 1::2] = 1

    for i in range(n):
        for j in range(n):
            print(x[i][j], end=" ")
        print()
n = 8
tabuleiro(n)