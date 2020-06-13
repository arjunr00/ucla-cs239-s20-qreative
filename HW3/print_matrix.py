import numpy
import sys
from colorama import Fore

numpy.set_printoptions(threshold=numpy.inf, linewidth=numpy.inf)
matrix=numpy.load(f'uf/{sys.argv[1]}').astype(int)

print(str(matrix).replace('1 ', '\u2593\u2593').replace('1', '\u2593\u2593').replace('0 ', '\u2591\u2591').replace('0', '\u2591\u2591').replace('[[',' ').replace('[', '').replace(']',''))

if len(sys.argv) != 3:
    exit(0)

n=int(sys.argv[2])
for i in range(0, 2**n):
    start=i*(2**n)
    end=start+(2**n)
    print(str(matrix[start:end,start:end]).replace('1 ', '\u2593\u2593').replace('1', '\u2593\u2593').replace('0 ', '\u2591\u2591').replace('0', '\u2591\u2591').replace('[[',' ').replace('[', '').replace(']',''))
    print('')
