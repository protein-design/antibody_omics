'''
example: 
    - python app.py absd_pro_seq
functions:
    - put unique sequences to table pro_seq
'''
from ..ab_helper import *
from src.abomics import Absd

def update_status(group_no):
    query = f"""
        UPDATE absd SET is_pro_seq = TRUE
        WHERE group_no = {group_no}
    """
    res = UpdateComplex(params['verbose']).execute_update(query, None)
    print(f"Update table absd {res}")

def retrieve(params, meta):
    query = f"""
        SELECT group_no, faa_file FROM absd
        WHERE is_pro_seq IS NULL
        ORDER BY release_date, specie
    ;"""
    rows = QueryComplex(params['verbose']).list_data(query)
    meta['faa_files'] += len(rows)

    pool = {}
    uc = UpdateComplex(params['verbose'])
    for row in rows:
        if params['verbose']:
            print(f"Begin to parse sequences {row['faa_file']}...")
        record_iter = Absd.scan_data(row['faa_file'])
        for record in record_iter:
            seq = str(record.seq)
            prefix = (seq[:params['seq_head_len']], len(seq))
            if prefix not in pool:
                pool[prefix] = [seq,]
            else:
                pool[prefix].append(seq)
            # push batch records to table if accumuated much
            if len(pool[prefix]) > 1_000:
                uc.put_pro_seq(prefix, pool[prefix], params['source'])
                pool[prefix] = []
        update_status(row['group_no'])
    return pool    
    

if __name__ == "__main__":
    params.update({
        'chunk_size': 100,
        'table_name': 'pro_seq',
        'source': 'ABSD',
        'seq_head_len': 6,
    })
    # put most new sequences
    seq_pool = retrieve(params, meta)

    # put the remaining finally
    uc = UpdateComplex(params['verbose'])
    for prefix, seqs in seq_pool.items():
        uc.put_pro_seq(prefix, seqs, params['source'])

    print(meta)

