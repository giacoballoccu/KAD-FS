import argparse
from utils import *
from mappers import *
import csv
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, default=BEAUTY, help='Dataset name check utils for the current implemented list')
    parser.add_argument('--from', type=str, default="pgpr", help='Model name of the data format you have')
    parser.add_argument('--to', type=str, default='kgat', help='Model name of the data format you want')
    parser.add_argument('--use_words', type=bool, default=True, help='Use words from reviews as additional knowledge')
    args = parser.parse_args()

    PGPR2KGAT(args)



