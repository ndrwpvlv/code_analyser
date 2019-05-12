# -*- coding: utf-8 -*-

import ast
import collections
import glob
import itertools

import nltk


def flat(l: list) -> list:
    """
    Flatten list of tuples to list

    :param l: List of tuples for flatten, list
    :return: Flattened list, list
    """
    return [item for sublist in l for item in sublist]


def is_verb(word: str) -> bool:
    """
    Check string for VERB type
    :param word: String with one word, str
    :return: Check of result for verb (True or False), bool
    """
    return False if not word else nltk.pos_tag([word])[0][1] == 'VB'


def get_files_paths(path: str, file_extension: str, list_size_limit: int) -> list:
    """
    Make list of files paths with needed extension
    :param path: Path of working directory, str
    :param file_extension: File extension for analysis, str
    :param list_size_limit: Number of files for analysis, int
    :return: List of files paths, list
    """
    return list(
        itertools.islice((f for f in glob.glob(path + '**/*.' + file_extension, recursive=True)), list_size_limit))


def get_trees(files_paths: list, with_file_path: bool = False, with_file_content: bool = False) -> ast:
    """
    Generate ast trees of find files
    :param files_paths: List with files paths, list
    :param with_file_path: Key of add file path to tree, bool
    :param with_file_content: Key of add file content to tree, bool
    :return: ast trees
    """
    trees = []
    for file_path in files_paths:
        with open(file_path, 'r', encoding='utf-8') as attempt_handler:
            file_content = attempt_handler.read()
        try:
            tree = ast.parse(file_content)
        except SyntaxError as e:
            print(e)
            tree = None
        if with_file_path:
            trees.append((file_path, file_content, tree)) if with_file_content else trees.append((file_path, tree))
        else:
            trees.append(tree)
    return trees


def get_all_names(tree: ast) -> list:
    """
    Get all names of tree nodes
    :param tree: ast tree
    :return: List of names, ist
    """
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def get_verbs_from_function_name(function_name: str) -> list:
    """
    Extract verbs from string
    :param function_name: string with function name, str
    :return: list of verbs
    """
    return [word for word in function_name.split('_') if is_verb(word)]


def get_functions_names_from_trees(trees: ast) -> list:
    """
    Extract function names from ast trees
    :param trees: ast trees
    :return: List of names, list
    """
    return [[node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)] for tree in trees]


def extract_functions_names(names: list) -> list:
    """
    Extract function names from list of names (names with '__' is not included)
    :param names: List of names, list
    :return: List of extracted filtered names
    """
    return [f for f in flat(names) if not (f.startswith('__') and f.endswith('__'))]


def get_all_words_in_path(path: str, file_extension: str, list_size_limit: int) -> list:
    """
    Get all words in function names
    :param path: Path of working directory, str
    :param file_extension: File extension for analysis, str
    :param list_size_limit: Number of files for analysis, int
    :return: List of find words, list
    """
    files_paths = get_files_paths(path, file_extension, list_size_limit)
    trees = [tree for tree in get_trees(files_paths) if tree]
    function_names = extract_functions_names(
        [get_all_names(tree) for tree in trees]
    )
    return flat([[substr for substr in name.split('_') if substr] for name in function_names])


def get_all_functions_names_in_path(path: str, file_extension: str, list_size_limit: int) -> list:
    """
    Get all function names
    :param path: Path of working directory, str
    :param file_extension: File extension for analysis, str
    :param list_size_limit: Number of files for analysis, int
    :return: List of find functions names, list
    """
    files_paths = get_files_paths(path, file_extension, list_size_limit)
    trees = get_trees(files_paths)
    functions_names_from_trees = get_functions_names_from_trees(trees)
    return extract_functions_names(functions_names_from_trees)


def get_all_verbs_in_path(path: str, file_extension: str, list_size_limit: int) -> list:
    """
    Get all verbs from functions names
    :param path: Path of working directory, str
    :param file_extension: File extension for analysis, str
    :param list_size_limit: Number of files for analysis, int
    :return: List of find verbs, list
    """
    function_names = get_all_functions_names_in_path(path, file_extension, list_size_limit)
    return flat([get_verbs_from_function_name(name) for name in function_names])


def create_words_top(words: list, words_list_size: int) -> list:
    """
    Make top of popular words
    :param words: List of words, list
    :param words_list_size: Size of top list, int
    :return: List of top words with count, list
    """
    return [[word, count] for word, count in collections.Counter(words).most_common(words_list_size)]
