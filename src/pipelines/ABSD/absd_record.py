'''
example:
    - parallel -j8 abomics absd_record ::: {1..57}
    - abomics absd_record 1
functions:
    - retrieve record_id in fasta, and absd_id
'''
from src.ab_helper import *
from abomics import Absd

def update_status(group_no):
    query = f"""
        UPDATE absd SET is_record = TRUE
        WHERE group_no = {group_no}
    """
    res = UpdateComplex(params['verbose']).execute_update(query, None)
    print(f"Update table absd {res}")

def retrieve(params):
    table_name = params['table_name']
    group_no = params['group_no']
    query = f"""
        SELECT specie, relative_fasta
        FROM absd
        WHERE group_no = {group_no} 
            AND group_no NOT IN (
                SELECT DISTINCT group_no FROM {table_name}
            )
    ;"""
    rows = QueryComplex(params['verbose']).list_data(query)
    if rows:
        params['specie'] = rows[0]['specie']
        faa_file = params['absd_dir'] / rows[0]['relative_fasta']
        return faa_file
    return None

def build(faa_file, params, meta):
    if params['verbose']:
        print('Scan ', params['specie'], faa_file, end=': ')
    n = 0
    for record in Absd.scan_data(faa_file):
        record_name = record.description.split("|||")[0]
        seq = str(record.seq)
        rec = (params['group_no'], record_name, seq)
        n += 1 
        yield rec
    meta[f"{params['specie']}_new"] += n
    print(f"new records = {n}.")
    update_status(params['group_no'])


if __name__ == "__main__":
    params.update({
        'overwrite': False,
        'chunk_size': 200,
        'table_name': 'absd_record',
        'table_cols': ['group_no', 'record_name', 'seq'],
    })
    if params['overwrite']:
        # empty data
        dc = DeleteComplex(params['verbose'])
        res = dc.delete_rows(params['table_name'], 'group_no', [params['group_no'],])
        print(f"Delete {res} before insertion")
    
    # retrieve data
    faa_file = retrieve(params)
    if faa_file:
        record_iter = build(faa_file, params, meta)
        bc = BuildComplex(params['verbose'], params['chunk_size'])
        bc.insert_batch_records(record_iter, params['table_name'], params['table_cols'])
    
    footer(meta)
