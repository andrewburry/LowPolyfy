from argparse import ArgumentParser
from lowpolyfy.LowPolyfy import LowPolyfy


def run():
    parser = ArgumentParser()
    parser.add_argument("-s", "--source", help="Source file name")
    parser.add_argument("-a", "--algorithm", help="The point selection algorithm")
    parser.add_argument("-n", "--numpoints", help="The number of points to place in the video cube")
    args = parser.parse_args()

    lp = LowPolyfy()

    if (args.source):
        lp.approximate(args.source, args.algorithm, int(args.numpoints))
    else:
        print("You must include a source file to transform and a point selection algorithm.")
