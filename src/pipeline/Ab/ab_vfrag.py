#!/usr/bin/python
'''
requirements:
    - table ab_vdj
example:
    - parallel -j4 python app.py ab_vfrag ::: {0..400}
    - python app.py ab_vfrag 0
function:
    - parse alignments and insert FRs and CDRs of V-region into table ab_vfrag
'''

from ..ab_helper import *
from bioomics import ParseIgblast

@header
def retrieve(params, meta):
    min_id = int(params['group_no']) * int(params['chunk_size'])
    max_id = min_id + int(params['chunk_size'])
    table_name = params['table_name']
    query = f"""
        SELECT b.relative_faa, a.v_aln
        FROM ab_vdj a, view_proseq b
        WHERE a.seq_id = b.seq_id
            AND a.seq_id >= {min_id} AND a.seq_id < {max_id}
            AND a.seq_id NOT IN (
                SELECT query_id FROM {table_name}
            )
    ;"""
    rows = QueryComplex(params['verbose']).list_data(query)
    meta['rows'] = len(rows)
    for row in rows:
        row['faa_file'] = os.path.join(params['output_protein_dir'], row['relative_faa'])
        row['aln_file'] = os.path.join(params['output_protein_dir'], row['v_aln'])
        if os.path.isfile(row['faa_file']) and os.path.isfile(row['aln_file']):
            yield row

def build(rows, params, meta):
    records = []
    for row in rows:
        c = ParseIgblast(row['aln_file'], row['faa_file'], params['verbose'])
        for region in c.retrieve_regions():
            item = {'query_id': region['query_id'],}
            if 'percent identity' in region:
                region_name = region['region'] 
                item.update({
                    'identity': region['percent identity'],
                    'seq': region['seq'],
                })
                if  region_name == 'Total':
                    item.update({
                        'fragment': 'Total',
                        'seq_from': 1,
                        'seq_to': len(region['seq']),
                    })
                else:
                    item.update({
                        'fragment': region_name.replace('-IMGT', ''),
                        'seq_from': region['from'],
                        'seq_to': region['to'],
                    })
            rec = tuple([item.get(col) for col in params['table_cols']])
            if rec not in records:
                records.append(rec)
            meta['regions'] += 1
    return records

if __name__ == "__main__":
    params.update({
        'chunk_size': 10_000,
        'table_name': 'ab_vfrag',
        'table_cols': ['query_id', 'fragment', 'identity', \
            'seq_from', 'seq_to', 'seq',],
    })

    # parse alignments and build records
    rows = retrieve(params, meta)
    records = build(rows, params, meta)
    if records:
        print(f"Try to insert data into {params['table_name']}...")
        bc = BuildComplex(params['verbose'])
        bc.insert_batch_records(records, params['table_name'], params['table_cols'])

    footer(meta)

