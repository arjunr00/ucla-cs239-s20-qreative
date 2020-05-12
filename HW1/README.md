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

We also save all our matrices in a ```/uf/{algo}``` folder to reduce compute time during testing. Use the **-r** or **--reload** flag to reload U_f matrix.

## Deutsch-Josza

### Problem Statement
Given function ```f(x): {0,1}^n -> {0, 1}```. Determine whether the function is ***balanced*** or ***constant***.

### Usage
We randomized the function f(x) but allow users to select whether they want their function to be ***balanced*** or ***constant***.

```
To run:
    python3 dj.py [-h] [--num NUM] [--trials TRIALS] [--reload] [--balanced] [--verbose]

Defaults:
    num     (size of bitstring): 4
    trials   (number of trials): 2
    reload   (reload Uf matrix): False (loads matrix if it exists)
    balanced    (function type): False (function by default is constant)
    verbose     (Display state): False
```

Run ```python3 dj.py -v``` for defaults and to look at state of algorithm. 

### Output
Since we added a **--verbose** flag, we decided to take a minimalist approach to outputing validity. Without the **--verbose** flag, dj.py will simply return whether the algorithm was successful or not. 

```
With --verbose flag:
    Message to where U_f matrix is saved
    Display of U_f matrix.
    Measured values of all qubits across iterations
    Measured state of each iteration
    Validity Message (Success or Failure)
```

Extensive documentation visible inside dj.py file.

## Bernstein-Vazirani

### Problem Statement
Given function ```f(x): {0,1}^n -> {0,1}^n``` where ```f(x) = a*x + b```. Find ***a*** and ***b***.

### Usage
We randomized the function f(x) with different ***a*** and ***b*** to reduce undefined behavior from the user. Mostly because our ***a*** must be stored as a bitstring so it seemed functional to keep it abstracted.

```
To run:
    python3 bv.py [-h] [--num NUM] [--trials TRIALS] [--reload] [--verbose]

Defaults:
    num     (size of bitstring): 4
    trials   (number of trials): 2
    reload   (reload Uf matrix): False (loads matrix if it exists)
    verbose     (Display state): False
```

Run ```python3 bv.py -v``` for defaults and to look at state of algorithm. 

### Output
Since we added a **--verbose** flag, we decided to take a minimalist approach to outputing validity. Without the **--verbose** flag, bv.py will simply return whether the algorithm was successful or not. 

```
With --verbose flag:
    Display of alpha
    Display of beta
    Message to where U_f matrix is saved
    Display of U_f matrix.
    Measured values of all qubits across iterations
    Measured state of each iteration [must match alpha]
    Validity Message (Success or Failure)
```

Extensive documentation visible inside bv.py file.

## Simon's

### Problem Statement
Given function ```f(x): {0,1}^n -> {0,1}^m``` and that there exists ```f(x0) = f(x1)``` for all ```x0, x1``` if and only if ```x0 + x1 = {0^n, s}```. Find ***s***.

### Usage
We randomized the function f(x) with load or generated ***s*** to reduce undefined behavior from the user. Mostly because our ***s*** must be stored as a bitstring so it seemed robust to keep it abstracted.

```
To run:
    python3 simon.py [-h] [--num NUM] [--trials TRIALS] [--reload] [--verbose]

Defaults:
    num     (size of bitstring): 3
    trials   (number of trials): 1
    reload   (reload Uf matrix): False (loads matrix if it exists)
    verbose     (Display state): False
```

Run ```python3 simon.py -v``` for defaults and to look at state of algorithm. 

### Output
Since we added a **--verbose** flag, we decided to take a minimalist approach to outputing validity. Without the **--verbose** flag, simon.py will simply return whether the algorithm was successful or not. 

```
With --verbose flag:
    Display of measured qubits.
    Display of [y] values across trials 
    Display of s
    Validity Message (Success or Failure)
    Time to Completion
```

Extensive documentation visible inside simon.py file.

## Grover's

### Problem Statement
Given function ```f(x): {0,1}^n -> {0, 1}``` where there exist an ```x in {0,1}^n``` where ```f(x) = 1```. Find ***x***.

### Usage
We randomized the function f(x) with randomly determined ***x*** to reduce undefined behavior from the user. Mostly because our ***x*** must be stored as a bitstring so it seemed robust to keep it abstracted.

```
To run:
    python3 grover.py [-h] [--num NUM] [--reload] [--verbose]

Defaults:
    num     (size of bitstring): 4
    reload   (reload Uf matrix): False (loads matrix if it exists)
    verbose     (Display state): False
```

Run ```python3 grover.py -v``` for defaults and to look at state of algorithm. 

### Output
Since we added a **--verbose** flag, we decided to take a minimalist approach to outputing validity. Without the **--verbose** flag, grover.py will simply return whether the algorithm was successful or not. 

```
With --verbose flag:
    Display of parameters
    Number of rotations [k]
    Measured values of valid qubits
    Display of measured bits equivalent to one
    Validity Message (Success or Failure)
    Time to Completion
```

Extensive documentation visible inside grover.py file.
