'''
example: 
    - abomics inn_cdr
functions:
    - download data from IMGT
    - put data to table inn_cdr
'''

from src.ab_helper import *
from abomics import PullData


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
        'table_name': 'inn_cdr',
        'table_cols': ['chain_id', 'cdr_type', 'seq', 'seq_align',
            'align_start', 'align_end', 'align_length',],
    })
    
    # pull records from IMGT
    data_iter = PullData(params['imgt_dir'], meta).flat_inn()
    record_iter = build(data_iter, meta)

    # insertion
    bc = BuildComplex(params['verbose'], params['chunk_size'])
    bc.empty_table(params['table_name'])
    bc.insert_batch_records(record_iter, params['table_name'], params['table_cols'])
    
    print(meta)


