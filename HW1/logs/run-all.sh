rundj() {
    cd .. && python dj.py -v -t 1 -n 2 ; \
    cd .. && python dj.py -v -t 1 -n 3 ; \
    cd .. && python dj.py -v -t 1 -n 4 ; \
    cd .. && python dj.py -v -t 1 -n 5 ; \
    cd .. && python dj.py -v -t 1 -n 6 ; \
    cd .. && python dj.py -v -t 1 -n 7 ; \
    cd .. && python dj.py -v -t 1 -n 8 ; \
    cd .. && python dj.py -v -t 1 -n 9
}

runbv() {
    cd .. && python bv.py -v -t 1 -n 2 ; \
    cd .. && python bv.py -v -t 1 -n 3 ; \
    cd .. && python bv.py -v -t 1 -n 4 ; \
    cd .. && python bv.py -v -t 1 -n 5 ; \
    cd .. && python bv.py -v -t 1 -n 6 ; \
    cd .. && python bv.py -v -t 1 -n 7 ; \
    cd .. && python bv.py -v -t 1 -n 8 ; \
    cd .. && python bv.py -v -t 1 -n 9
}

runsimon() {
    cd .. && python simon.py -v -n 1 ; \
    cd .. && python simon.py -v -n 2 ; \
    cd .. && python simon.py -v -n 3 ; \
    cd .. && python simon.py -v -n 4 ; \
    cd .. && python simon.py -v -n 5 ; \
    cd .. && python simon.py -v -n 6 ; \
    cd .. && python simon.py -v -n 7
}

rungrover() {
    cd .. && python grover.py -v -n 1 ; \
    cd .. && python grover.py -v -n 2 ; \
    cd .. && python grover.py -v -n 3 ; \
    cd .. && python grover.py -v -n 4 ; \
    cd .. && python grover.py -v -n 5 ; \
    cd .. && python grover.py -v -n 6 ; \
    cd .. && python grover.py -v -n 7 ; \
    cd .. && python grover.py -v -n 8
}

# rundj > dj.log 2>&1
# runbv > bv.log 2>&1
# runsimon > simon.log 2>&1
rungrover > grover.log 2>&1
