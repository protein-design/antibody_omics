'''
example: 
    - python app.py inn_region
functions:
    - download data from IMGT
    - put data to table inn_region
'''

from ..ab_helper import *
from bioomics import Dir, ParseImgtAnnot

def pull_data(params, meta):
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
        'imgt_dir': os.getenv('imgt_dir'),
        'table_name': 'inn_region',
        'table_cols': ['chain_id', 'region_name', \
            'region_type', 'start', 'end', 'seq'],
    })
    # pull records from IMGT
    data_iter = pull_data(params, meta)
    record_iter = build(data_iter, meta)

    # insertion
    bc = BuildComplex(params['verbose'], params['chunk_size'])
    bc.empty_table(params['table_name'])
    bc.insert_batch_records(record_iter, params['table_name'], params['table_cols'])
    
    footer(meta)

