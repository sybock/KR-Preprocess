from kr_preprocess import PreProcessing
import argparse
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", \
                        required=True, type=str, help="Input file path")
    parser.add_argument("-o", "--output", \
                        type=str, default="ouput.txt", help="Output file path")
    parser.add_argument("-m", "--min_length", \
                        type=int, default=7, help="Minimum length of line")
    parser.add_argument("--news", \
                        required=False, type=bool, default=False, \
                        help="Text has news articles")
    parser.add_argument("-dt","--datetime", \
                        required=False, type=bool, default=False, \
                        help="Text has date time text to be erased")

    args = parser.parse_args()
    txt = PreProcessing(args)
    '''Add custom regex here'''
    txt.apply()