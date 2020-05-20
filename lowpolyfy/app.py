from argparse import ArgumentParser
from lowpolyfy.LowPolyfy import LowPolyfy
import logging
from os import makedirs


def setup_logger():
    LOG_DIRECTORY = "logs"
    LOG_NAME = "lowpolyfy.log"

    # Ensure the log directory is created
    makedirs(LOG_DIRECTORY, exist_ok=True)

    # Set up the root logger
    LOG_FORMAT = "[%(levelname)s %(asctime)s] %(name)s - %(message)s"
    logging.basicConfig(filename = LOG_DIRECTORY + "/" + LOG_NAME,
                        level = logging.INFO,
                        format = LOG_FORMAT,
                        filemode = 'w')

def run():
    # Set up the logger
    setup_logger()

    # Parse the input arguments
    parser = ArgumentParser()
    parser.add_argument("-s", "--source", help="Source file name")
    parser.add_argument("-a", "--algorithm", help="The point selection algorithm")
    parser.add_argument("-n", "--numpoints", help="The number of points to place in the video cube")
    args = parser.parse_args()

    # Create the lowpolyfy object
    lp = LowPolyfy()

    if (args.source):
        # Approximate the source video with the input arguments
        lp.approximate(args.source, args.algorithm, int(args.numpoints))
    else:
        print("You must include a source file to transform and a point selection algorithm.")
