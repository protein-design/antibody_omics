'''
requirements:
    - IMGT/INN data are downloaded
example: 
    - abomics inn
functions:
    - put data to table inn
'''

from src.ab_helper import *
from abomics import PullData

def build(data_iter, meta):
    names = ('inn_number', 'cas_number', 'common_name', 'inn_name',
        'proposed_list', 'recommended_list', 'receptor_type',
        'receptor_description', 'species',
        'molecular_formula', 'glycosylation_sites')
    for inn_data in data_iter:
        meta['records'] += 1
        rec = [inn_data['inn_file'], ]
        for name in names:
            val = inn_data.get(name)
            if isinstance(val, list):
                rec.append(','.join(val))
            else:
                rec.append(None)
        yield rec

if __name__ == "__main__":
    params.update({
        'chunk_size': 50,
        'table_name': 'inn',
        'table_cols': ['inn_file', 'inn_number', 'cas_number',
            'common_name', 'inn_name', 'proposed_list',
            'recommended_list', 'receptor_type',
            'receptor_description', 'species',
            'molecular_formula', 'glycosylation_sites',]
    })
    # pull records from IMGT
    data_iter = PullData(params['imgt_dir'], meta).flat_inn()
    record_iter = build(data_iter, meta)
    bc = BuildComplex(params['verbose'], params['chunk_size'])
    bc.empty_table(params['table_name'])
    bc.insert_batch_records(record_iter, params['table_name'], params['table_cols'])
    
    footer(meta)