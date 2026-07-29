'''
requirements:
    - IMGT/INN data are downloaded
example: 
    - python app.py inn
functions:
    - put data to table inn
'''

from ..ab_helper import *
from bioomics import Dir
from src.abomics import ParseImgtAnnot

def retrieve(params, meta):
    indir = os.path.join(params['imgt_dir'], '3Dstructure-DB', 'IMGT3DFlatFiles')
    for gz_file in Dir(indir).recursive_files():
        if gz_file.endswith('.inn.gz'):
            try:
                inn_data = ParseImgtAnnot(gz_file)()
                meta['inn_data'] += 1
                yield inn_data
            except Exception as e:
                print(f"{gz_file}, error={e}")
                meta['invalid_inn'] += 1

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
        'imgt_dir': os.getenv('imgt_dir'),
        'table_name': 'inn',
        'table_cols': ['inn_file', 'inn_number', 'cas_number',
            'common_name', 'inn_name', 'proposed_list',
            'recommended_list', 'receptor_type',
            'receptor_description', 'species',
            'molecular_formula', 'glycosylation_sites',]
    })
    # pull records from IMGT
    data_iter = retrieve(params, meta)
    record_iter = build(data_iter, meta)
    bc = BuildComplex(params['verbose'], params['chunk_size'])
    bc.empty_table(params['table_name'])
    bc.insert_batch_records(record_iter, params['table_name'], params['table_cols'])
    
    footer(meta)

