'''
example: 
    - abomics inn_region
functions:
    - download data from IMGT
    - put data to table inn_region
'''

from src.ab_helper import *
from abomics import PullData

def build(data_iter, meta):
    for inn_data in data_iter:
        for chain in inn_data.get('chains', []):
            for region in chain.get('regions', []):
                rec = (
                    chain['chain_id'],
                    region.get('region'),
                    region.get('type'),
                    region.get('start'),
                    region.get('end'),
                    region.get('seq'),
                )
                yield rec
                meta['records'] += 1

    
if __name__ == "__main__":
    params.update({
        'chunk_size': 50,
        'table_name': 'inn_region',
        'table_cols': ['chain_id', 'region_name', 'region_type', 'start', 'end', 'seq'],
    })
    
    # empty table
    DeleteComplex(params['verbose']).empty_table(params['table_name'])
    
    # pull records from IMGT
    data_iter = PullData(params['imgt_dir'], meta).flat_inn()
    record_iter = build(data_iter, meta)

    # insertion
    bc = BuildComplex(params['verbose'], params['chunk_size'])
    bc.insert_batch_records(record_iter, params['table_name'], params['table_cols'])
    
    footer(meta)