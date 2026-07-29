'''
example:
    - parallel -j8 abomics absd_source ::: {1..57}
    - abomics absd_source 1
functions:
    - retrieve database source
'''
from src.ab_helper import *
from abomics import Absd

def update_status(group_no):
    query = f"""
        UPDATE absd SET is_source = TRUE
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
            AND {group_no} NOT IN (
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
    for seq_record in Absd.scan_data(faa_file):
        desc = seq_record.description.split("|||")
        record_name = desc[0]
        seq_source = seq_record.id.split("|||")[-1]
        for _desc in desc[1:]:
            header, dxref_id, vgene_family, source = _desc.split(';')
            meta[f"{params['specie']}_new"] += 1
            rec = (params['group_no'], record_name, seq_source, dxref_id, vgene_family, source)
            yield rec
    update_status(params['group_no'])
            
if __name__ == "__main__":
    params.update({
        'overwrite': False,
        'chunk_size': 500,
        'table_name': 'absd_source',
        'table_cols': ['group_no', 'record_name', 'seq_source', 'dxref_id', 'vgene_family', 'source'],
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
        bc = BuildComplex(params['verbose'])
        bc.insert_batch_records(record_iter, params['table_name'], params['table_cols'])

    footer(meta)
