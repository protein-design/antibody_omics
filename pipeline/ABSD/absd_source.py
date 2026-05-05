'''
example:
    - python app.py absd_source
functions:
    - retrieve database source
'''
from ..ab_helper import *
from src.abomics import Absd

def update_status(group_no):
    query = f"""
        UPDATE absd SET is_source = TRUE
        WHERE group_no = {group_no}
    """
    res = UpdateComplex(params['verbose']).execute_update(query, None)
    print(f"Update table absd {res}")

def retrieve_faa(params, meta):
    query = f"""
        SELECT group_no, specie, faa_file
        FROM absd
        WHERE is_source IS NULL
        ORDER BY specie, release_date
    ;"""
    df = QueryComplex(params['verbose']).list_data(query, True)
    meta['faa_files'] += len(df)
    g = df.groupby('specie')
    return g

def unique_ids(specie, params, meta):
    table_name = params['table_name']
    query = f"""
        SELECT absd_id, source FROM {table_name}
        WHERE specie = '{specie}'
    ;"""
    rows = QueryComplex(params['verbose']).list_data(query)
    meta[f'{specie}_records'] += len(rows)
    ids = [(i['absd_id'], i['source']) for i in rows]
    return ids

if __name__ == "__main__":
    params.update({
        'chunk_size': 500,
        'table_name': 'absd_source',
        'table_cols': ['specie', 'absd_id', 'dxref_id', 'vgene_family', 'source'],
    })
    records = []
    faa_iter = retrieve_faa(params, meta)
    for specie, sub in faa_iter:
        ids = unique_ids(specie, params, meta)
        for _, row in sub.iterrows():
            faa_file = row['faa_file']
            for seq_record in Absd.scan_data(faa_file):
                desc = seq_record.description.split("|||")
                absd_id = desc[0]
                for _desc in desc[1:]:
                    header, dxref_id, vgene_family, source = _desc.split(';')
                    if (absd_id, source) not in ids:
                        rec = (specie, absd_id, dxref_id, vgene_family, source)
                        meta[f"{specie}_new"] += 1
                        if rec not in records:
                            records.append(rec)
                # insertion
                if len(records) > params['chunk_size']:
                    bc = BuildComplex(records, params['verbose'])
                    bc.insert_batch_records(params['table_name'])
                    records = []
            update_status(row['group_no'])
    if records:
        bc = BuildComplex(records, params['verbose'])
        bc.insert_batch_records(params['table_name'], params['table_cols'])
        records = []
    footer(meta)
