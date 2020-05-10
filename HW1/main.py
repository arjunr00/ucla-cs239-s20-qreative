import argparse
from dj import DJ

class Algo():
    def measure(self, result, n, t, args):
        if v:
            print("====================================")
            print("Measured Qubit State Accross Trials:\n")
            print(result)
            print("====================================\n")

        for i in range(t):
            measured_bits = [result[q][i] for q in range(n)]
            if v:
                print("====================================")
                print("Measured State for Iteration {}:\n".format(i+1))
                print(measured_bits)
                print("====================================\n")
            if not self.check_valid(measured_bits, args):
                return False
        return True

    def obtain_parameters(self):


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CS239 - Spring 20 - HW1', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.set_defaults(verbose=False)
    parser.add_argument("--verbose", "-v", action="store_true", help='Print out measured bits and steps')
    parser.add_argument()
    args = parser.parse_args()

    v = args.verbose

    algo = Algo()
