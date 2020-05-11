# CS239 - PyQuil Implementation - HW1
Pyquil implementation of the following algorithms:

- Deutsch-Josza
- Bernstein-Vazirani
- Simon's
- Grover's

Every file tests for correctness of algorithm through **randomized** function parameters. 

## Prerequisites

Python modules necessary for use:
```
Needs installation:
    sympy
    numpy
    pyquil

Preinstalled (Python3)):
    random
    itertools
    time
    argparse
    os
    math
```

# Usage
Below we discuss how to use our files to test and verify the 4 programs stated above.

We decided that function input from the user could lead to undefined behavior, so we ended up choosing a randomized function approach to test validity. 

If you want to see the nitty gritty details of the state of our algorithm during run time and not just an output telling you if the algorithm worked or not, make sure to add the **-v** or **--verbose** flag.

## Deutsch-Josza


Extensive documentation visible inside dj.py file.

## Bernstein-Vazirani


Extensive documentation visible inside bv.py file.

## Simon's


Extensive documentation visible inside simon.py file.

## Grover's


Extensive documentation visible inside grover.py file.
