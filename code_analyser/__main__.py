# -*- coding: utf-8 -*-

import argparse
import os
import sys

from code_analyser.config import config
from code_analyser.core import get_all_verbs_in_path, create_words_top


def get_args():
    parser = argparse.ArgumentParser('Usage of verbs in functions names')
    parser.add_argument('-p', '--path', default=config['HOME_PATH'],
                        help="directory path for code analysis", type=str)
    parser.add_argument('-t', '--words_top_size', default=config['WORDS_TOP_SIZE'],
                        help="maximum number of top useful words", type=int)
    parser.add_argument('-P', '--packages', default=config['PACKAGES'], help="packages names for code analysis",
                        type=list)
    parser.add_argument('-e', '--extension', default=config['EXTENSION'], help="extension of files", type=str)
    parser.add_argument('-f', '--files_number_limit', default=config['FILES_NUMBER_LIMIT'],
                        help="Limit of files number for analysis", type=int)

    return parser.parse_args(sys.argv[1:])


if __name__ == '__main__':
    args = get_args()

    words = []

    for package in args.packages:
        path = os.path.join(args.path, package)
        words += get_all_verbs_in_path(path, args.extension, args.files_number_limit)
    words_top = create_words_top(words, args.words_top_size)

    print('Find total %s verbs, %s unique' % (len(words), len(set(words))))
    print('VERB: COUNT')
    for word in words_top:
        print('%s: %i' % (word[0], word[1]))
