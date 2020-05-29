import numpy as np
import argparse
import math
import os
import oracle
import time

def z0(n):

def 
def qc_program(n, reload, verbose):


parser = argparse.ArgumentParser(description='CS239 - Spring 20 - Grover', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.set_defaults(reload=False, verbose=False)
parser.add_argument("--num", "-n", type=int, default=2, help="Set length of input bitstring")
parser.add_argument("--reload", "-r", action="store_true", help='Reload new U_f matrix')
parser.add_argument("--verbose", "-v", action="store_true", help='Print out measured bits and steps')
args = parser.parse_args()

if __name__ == '__main__':
    n = args.num
    r = args.reload
    v = args.verbose

    print('=======================================================')
    print('Testing Grover\'s Algorithm')
    if v:
        print(f'\n   Running with bit string of size n = {n},')
        print(f'                   reload U_f matrix = {r}')
    print('=======================================================\n')

    start = time.time()
    ret = qc_program(n, r, v)
    end = time.time()

    if ret is True:
        ret_str = "Success!"
    else:
        ret_str = "Fail :("

    print(f'Grover\'s Algorithm: {ret_str}')
    print(f'(Took {end - start:.2f} s to complete.)'