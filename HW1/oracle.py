from enum import Enum

import numpy as np
import itertools
import random

class Algos(Enum):
    DJ    = 0
    BV    = 1
    SIMON = 2

class DJ(Enum):
    CONSTANT = 0
    BALANCED = 1

class Simon(Enum):
    ONE_TO_ONE = 0
    TWO_TO_ONE = 1

def init_bit_mapping(n, algo=None, func=None):
    """
    Generates a bit mapping for a given function:
        f: {0,1}^n -> {0,1}^m
    
    Args:
        n: the length of a input bitstring
        algo: the algorithm in question (select from Enum[Algos]) 
        func: the function f in question for bit mapping

    Returns:
        A bit mapping oracle_map of size 2^n. For every input bitstring x, oracle_map 
        maps x to f(x). 
            i.e. oracle_map = {x: f(x)} for all x in {0,1}^n
    """
    qubits = []       
    # itertools.product does a cross product between two components ([0, 1] x [0, 1] x ... x [0, 1])
    # https://stackoverflow.com/questions/1457814/get-every-combination-of-strings
    for i in itertools.product(['0','1'], repeat=n):            
        qubits.append(''.join(i))
    # resulting qubits = ['000', '001', '010', '011', '100', '101', '110', '111']

    if algo is Algos.DJ: 
        # Constant: f(x) returns 0 or 1 for all x
        if func is DJ.CONSTANT:       
            val = np.random.choice(['0','1'])
            oracle_map = {i: val for i in qubits}
        # Balanced: f(x) returns 0 or 1 for all x
        # val1 represents set of x that f(x) = 1
        # val0 represents set of x that f(x) = 0
        elif func is DJ.BALANCED:
            val1 = random.sample(qubits, k=int(len(qubits)/2))  
            val0 = set(qubits) - set(val1)
            oracle_map = {i: '1' for i in val1}
            temp = {i: '0' for i in val0}
            oracle_map.update(temp)
    elif algo is Algos.SIMON:
        oracle_map = {}
        if func is Simon.ONE_TO_ONE:
            for x in qubits:
                while True:
                    fx = np.random.choice(qubits)
                    if fx not in oracle_map.values():
                        break
                oracle_map[x] = fx
        elif func is None or func is Simon.TWO_TO_ONE:
            s = ""
            for i in range(0,n):
                s += np.random.choice(['0', '1'])

            for x in qubits:
                sXx = f'{int(x, 2) ^ int(s, 2):0{n}b}'
                while True:
                    fx = np.random.choice(qubits)
                    if fx not in oracle_map.values():
                        break

                if x not in oracle_map:
                    oracle_map[x] = fx
                    oracle_map[sXx] = fx
    
    # oracle_map is bit map from {x: f(x)} for all {0,1}^n
    return oracle_map

def gen_matrix(f, n, m):
    """
    Generates the quantum oracle corresponding to f, where f is defined as:
        f : {0,1}^n -> {0,1}^m

    Let x and b be bitstrings of length n. Let (*) represent the tensor product
    and + represent bitwise XOR. Then:
        U_f = Sum(|x><x| (*) |b + f(x)><b|)
    Here, `Sum` sums over all bitstrings xb.

    Args:
        f: The function as defined above.
        n: The dimension of f's domain.
        m: The dimension of f's range.

    Returns:
        A (2^n)x(2^m) matrix U_f which represents the quantum oracle corresponding
        to f.
    """

    # Accumulator to hold the value of the summation
    U_f=np.zeros((2**(n+m),2**(n+m)))
    for xb in range(0, int(2**(n+m))):
        # Convert index to binary and split it down the middle
        x  = f'{xb:0{n+m}b}'[:int(n)]
        b  = f'{xb:0{n+m}b}'[int(n):]
        # Apply f to x
        fx = f[x]
        # Calculate b + f(x)
        bfx = f'{int(b, 2) ^ int(fx, 2):0{n}b}'

        # Vector representations of x, b, and b+f(x)
        xv = np.zeros((2**n,1))
        xv[int(x, 2)] = 1.
        bv = np.zeros((2**m,1))
        bv[int(b, 2)] = 1.
        bfxv = np.zeros((2**m,1))
        bfxv[int(bfx, 2)] = 1.

        # Accumulate (|x><x| (*) |b + f(x)><b|) into the sum
        # (*) is the tensor product
        U_f = np.add(np.kron(np.outer(xv, xv), np.outer(bfxv, bv)), U_f)

    return U_f