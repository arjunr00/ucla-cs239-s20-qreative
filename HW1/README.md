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

We decided that function input from the user could lead to undefined behavior, so we ended up choosing a **randomized function** approach to test validity. 

If you want to see the nitty gritty details of the state of our algorithm during run time and not just an output telling you if the algorithm worked or not, make sure to add the **-v** or **--verbose** flag.

## Deutsch-Josza

**Problem Statement:**
Given function **f(x): {0,1}^n -> {0, 1}** determine whether the function is *balanced* or *constant*.



Extensive documentation visible inside dj.py file.

## Bernstein-Vazirani

**Problem Statement:**
Given function **f(x): {0,1}^n -> {0,1}^n** where **f(x) = a\*x + b** find *a* and *b*.

Extensive documentation visible inside bv.py file.

## Simon's

**Problem Statement:**
Given function **f(x): {0,1}^n -> {0,1}^m** and that there exists **f(x0) = f(x1)** for all **x0, x1** if and only if **x0 + x1 = {0^n, s}**. Find *s*.

Extensive documentation visible inside simon.py file.

## Grover's

**Problem Statement:**
Given function **f(x): {0,1}^n -> {0, 1}** where there exist an **x in {0,1}^n** where f(x) = 1. Find *x*.

Extensive documentation visible inside grover.py file.
