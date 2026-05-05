'''
requirements:
    - table pro_seq
example: 
    - python app.py absd_seq
functions:
    - parse seq_id in table pro_seq and absd_id in table absd_record
'''
import pandas as pd

from ..ab_helper import *
from src.abomics import Absd

def update_status(group_no):
    query = f"""
        UPDATE absd SET is_seq_map = TRUE
        WHERE group_no = {group_no}
    """
    res = UpdateComplex(params['verbose']).execute_update(query, None)
    print(f"Update table absd {res}")

def unique_seqs(prefix, params):
    query = f"""
        SELECT seq_id, seq
        FROM pro_seq
        WHERE source='{params['source']}'
            AND prefix = '{prefix}'
    ;"""    
    df = QueryComplex(params['verbose']).list_data(query, True)
    return df

def current_seqs(prefix, params):
    table_name = params['table_name']
    query = f"""
        SELECT a.seq_id, a.group_no, a.absd_id
        FROM {table_name} a
        LEFT JOIN pro_seq b ON a.seq_id = b.seq_id
        WHERE b.source IN ('ABSD')
            AND b.prefix = '{prefix}'
    ;"""    
    df = QueryComplex(params['verbose']).list_data(query, True)
    return df

def filter(prefix:str, seqs:list, params, meta):
    if params['verbose']:
        print(f"Begin to check prefix={prefix}")
    cols = ['seq_id', 'group_no', 'absd_id']

    # input cols: group_no, absd_id, seq
    df0 = pd.DataFrame(seqs)
    # unique sequences: seq_id, seq
    df1= unique_seqs(prefix, params)
    # parse seq_id ~ absd_id
    df2 = pd.merge(df0, df1, how='left', on='seq')
    df = df2[df2['seq_id'].notna()][cols]

    # mapping seq: seq_id, group_no, absd_id
    df3= current_seqs(prefix, params)
    if (not df.empty) and (not df3.empty):
        #remove seqs which are existing in table
        df4 = df.merge(df3, how='left', on=cols, indicator=True)
        df = df4[df4['_merge']=='left_only'][cols]
    
    #insert
    if not df.empty:
        records = list(df.itertuples(index=False, name=None))
        meta['mapped_seq'] += len(records)
        bc = BuildComplex(records, params['verbose'])
        bc.insert_batch_records(params['table_name'], params['table_cols'])

def retrieve(params, meta):
    query = f"""
        SELECT group_no, faa_file
        FROM absd
        WHERE is_seq_map IS NULL
        ORDER BY release_date, specie
    ;"""
    rows = QueryComplex(params['verbose']).list_data(query)
    meta['faa_files'] += len(rows)

    pool = {}
    for row in rows:
        if params['verbose']:
            print(f"Begin to parse sequences {row['faa_file']}...")
        record_iter = Absd.scan_data(row['faa_file'])
        for record in record_iter:
            desc = record.description.split("|||")
            seq = str(record.seq)
            prefix = seq[:params['prefix_len']]
            rec = {
                'group_no': row['group_no'],
                'absd_id': desc[0],
                'seq': seq,
            }
            if prefix not in pool:
                pool[prefix] = [rec,]
            else:
                pool[prefix].append(rec)
            # push batch records to table if accumuated much
            if len(pool[prefix]) > 1_000:
                filter(prefix, pool[prefix], params, meta)
                del pool[prefix]
        update_status(row['group_no'])
    return pool    
    

if __name__ == "__main__":
    params.update({
        'table_name': 'absd_seq',
        'table_cols': ['seq_id', 'group_no', 'absd_id'],
        'source': 'ABSD',
        'prefix_len': 6,
    })
    seq_pool = retrieve(params, meta)
    for prefix, seqs in seq_pool.items():
        filter(prefix, seqs, params, meta)

    footer(meta)

