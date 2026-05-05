'''
example:
    - python app.py absd_record
functions:
    - retrieve record_id in fasta, and absd_id
'''
from ..ab_helper import *
from src.abomics import Absd

def update_status(group_no):
    query = f"""
        UPDATE absd SET is_record = TRUE
        WHERE group_no = {group_no}
    """
    res = UpdateComplex(params['verbose']).execute_update(query, None)
    print(f"Update table absd {res}")

def retrieve_faa(params, meta):
    query = f"""
        SELECT group_no, specie, faa_file
        FROM absd
        WHERE is.record IS NULL
        ORDER BY specie, release_date
    ;"""
    df = QueryComplex(params['verbose']).list_data(query, True)
    meta['faa_files'] += len(df)
    g = df.groupby('specie')
    return g

def unique_ids(specie, params, meta) -> dict:
    table_name = params['table_name']
    query = f"""
        SELECT r.record_id
        FROM {table_name} r
        LEFT JOIN absd    a on r.group_no = a.group_no
        WHERE a.specie = '{specie}'
    ;"""
    rows = QueryComplex(params['verbose']).list_data(query)
    meta[f'{specie}_records'] += len(rows)
    ids = {} 
    for row in rows:
        _id = row['record_id']
        k = _id[:3]
        if k not in ids:
            ids[k] = [_id,]
        else:
            ids[k].append(_id)
    return ids

def build(faa_iter, params, meta):
    for specie, sub in faa_iter:
        ids = unique_ids(specie, params, meta)
        for _, row in sub.iterrows():
            group_no = row['group_no']
            faa_file = row['faa_file']
            if params['verbose']:
                print('Scan ', specie, faa_file, end=': ')
            n = 0
            for record in Absd.scan_data(faa_file):
                record_id = record.id
                k = record_id[:3]
                if k not in ids or (k in ids and record_id not in ids[k]):
                    absd_id = record.description.split("|||")[0]
                    rec = (group_no, absd_id, record_id,)
                    n += 1 
                    yield rec
            meta[f"{specie}_new"] += n
            print(f"new records = {n}.")
            update_status(row['group_no'])


if __name__ == "__main__":
    params.update({
        'chunk_size': 200,
        'table_name': 'absd_record',
        'table_cols': ['group_no', 'absd_id', 'record_id',],
    })

    faa_iter = retrieve_faa(params, meta)

    record_iter = build(faa_iter, params, meta)

    bc = BuildComplex(record_iter, params['verbose'], params['chunk_size'])
    bc.insert_batch_records(params['table_name'], params['table_cols'])
    
    footer(meta)
