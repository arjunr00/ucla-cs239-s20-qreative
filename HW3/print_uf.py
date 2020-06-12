import numpy as np

x = np.load('uf/grover/f_list.npy', allow_pickle=True).item()

for item in x:
    total = 0
    for i in x[item]:
        if x[item][i] == '1':
            total += 1
    print(f'{item}: {total}')