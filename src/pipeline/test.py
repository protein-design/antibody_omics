#!/usr/bin/python
'''
example:
    - parallel -j8 python app.py test ::: {0..9}
    - python app.py test
function:
    - test concurrency
'''

import time
from .ab_helper import *

if __name__ == "__main__":
    params.update({
        'overwrite': False,
        'test': False,
        'table_name': 'meta',
    })
    add_params(params)

    #update record
    time.sleep(30)
    footer(params, meta)
