'''
example: 
    - python app.py abybank
functions:
    - download data from abYbank
    - put data to table abybank
'''

from ..ab_helper import *
from src.abomics import Abybank


if __name__ == "__main__":
    params.update({
        'chunk_size': 20,
        'source': 'abYbank',
        'table_name': 'abybank',
        'table_cols': ['pdb_id', 'chain_type', 'chain_numbering'],
    })
    # pull records from abYbank
    abYbank_pdb = Abybank().pull_pdb_records()
    meta['rows'] = len(abYbank_pdb)

    # insertion
    bc = BuildComplex(params['verbose'], params['chunk_size'])
    bc.empty_table(params['table_name'])
    bc.insert_batch_records(abYbank_pdb, params['table_name'], params['table_cols'])
    
    footer(meta)

