# code_analyser

**code_analyser** - first homework of OTUS Python course. Run script to get unique verbs from code 

## Installation
```
sudo -H pip3 install .../code_analyser.zip

```

## Usage
```
usage: python3 -m code_analyser [-p HOME_PATH] [-t WORDS_TOP_SIZE] [-P PACKAGES] [-e EXTENSION] [-f FILES_NUMBER_LIMIT]

analyses use of verbs in functions names

optional arguments:
  -p HOME_PATH          Directory path for code analysis
  -t WORDS_TOP_SIZE     Maximum number of top useful words
  -P PACKAGES           Packages names for code analysis
  -e EXTENSION          Extension of files
  -f FILE_NUMBER_LIMIT  Limit of files number for analysis

```

## Requirements
```
nltk==3.4.1
six==1.12.0
```
