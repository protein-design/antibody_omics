'''
Download data from database SAbDab https://opig.stats.ox.ac.uk
example: 
    - python app.py sabdab
functions:
    - download data from SAbDab
    - put data to table sabdab
'''

from ..ab_helper import *
from src.abomics import Sabdab


if __name__ == '__main__':
    params.update({
        'overwrite': False,
        'chunk_size': 50,
        'source': 'SAbDab',
        'table_name': 'sabdab',
        'table_cols': ['pdb_id', 'summary_file'],
    })
    sab = Sabdab(params['rawdata_dir'], params['overwrite'])

    # retrieve list of pdb_id from sabdab_pdbs_list.txt
    # Warning: the list pdb in this file doesn't cover all pdb in sabdab.
    sabdab_ids = sab.retrieve_sabdab_pdb_ids()
    meta['sabdab_pdb_ids'] = len(sabdab_ids)

    # filter pdb_ids
    qc = QueryComplex(params['verbose'])
    pdb_ids = qc.unique_values(params['table_name'], 'pdb_id')
    if pdb_ids:
        sabdab_ids = list(set(sabdab_ids).difference(pdb_ids))
    meta['filtered_pdb_ids'] = len(sabdab_ids)

    # download summary/*.tsv
    record_iter = sab.download_summary(sabdab_ids, meta)

    # insertion
    bc = BuildComplex(params['verbose'], params['chunk_size'])
    bc.empty_table(params['table_name'])
    bc.insert_batch_records(record_iter, params['table_name'], params['table_cols'])

    footer(meta)
