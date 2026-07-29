#!/usr/bin/python
'''
requirements:
    - meta_combo2
example:
    - parallel -j8 python app.py test ::: {0..117}
    - python app.py test
    - uv run test-pp 1
    - parallel -j4 uv run test-pp ::: {1..10}
function:
    - test concurrency
'''

import time
from ab_helper import *

def main():
    params.update({
        'script': sys.argv[0],
        'pdb_group': None,
        'overwrite': False,
        'verbose': True,
        'test': False,
        'output_pdb_dir': os.getenv('output_pdb_dir'),
        'predict_dir': os.getenv('predict_dir'),
        'table_name': 'meta',
    })

    #update record
    time.sleep(3)
    footer(params, meta)

if __name__ == "__main__":
    main()