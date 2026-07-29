'''
example: 
    - python src/pipelines/imgt_inn_cdr.py
functions:
    - download data from IMGT
    - put data to table imgt_inn_cdr
'''

from ..ab_helper import *
from bioomics import Dir, ParseImgtAnnot

def pull_data(args, meta):
    indir = os.path.join(args['imgt_dir'], '3Dstructure-DB', 'IMGT3DFlatFiles')
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
            for domain in chain.get('v_domain', []):
                for cdr in domain.get('cdr', []):
                    start, end = cdr.get("start"), cdr.get("end")
                    len = None
                    try:
                        len = end - start + 1
                    except Exception as e:
                        pass
                    rec = (
                        chain['chain_id'],
                        cdr.get("name"),
                        cdr.get("seq"),
                        cdr.get("align"),
                        start,
                        end,
                        len,
                    )
                    yield rec
                    meta['records'] += 1
   
if __name__ == "__main__":
    params.update({
        'chunk_size': 50,
        'imgt_dir': os.getenv('imgt_dir'),
        'table_name': 'inn_cdr',
        'table_cols': ['chain_id', 'cdr_type', 'seq', 'seq_align',
            'align_start', 'align_end', 'align_length',],
    })
    # pull records from IMGT
    data_iter = pull_data(params, meta)
    record_iter = build(data_iter, meta)

    # insertion
    bc = BuildComplex(params['verbose'], params['chunk_size'])
    bc.empty_table(params['table_name'])
    bc.insert_batch_records(record_iter, params['table_name'], params['table_cols'])
    
    print(meta)


