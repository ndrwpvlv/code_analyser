# -*- coding: utf-8 -*-

import os

config = {
    'HOME_PATH': os.getcwd(),
    'WORDS_TOP_SIZE': 200,
    'PACKAGES': [
        'django',
        'flask',
        'pyramid',
        'reddit',
        'requests',
        'sqlalchemy',
    ],
    'EXTENSION': '.py',
    'FILES_NUMBER_LIMIT': 10000
}
