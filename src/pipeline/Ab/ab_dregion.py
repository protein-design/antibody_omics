#!/usr/bin/python
'''
requirements:
    - table ab_vdj
example:
    - parallel -j4 python app.py ab_dregion ::: {0..400}
    - python app.py ab_dregion 0
function:
    - parase alignment and insert D-region into table ab_dregion
'''

from ..ab_helper import *
from bioomics import ParseBlastXml

@header
def retrieve(params, meta):
    min_id = int(params['group_no']) * int(params['chunk_size'])
    max_id = min_id + int(params['chunk_size'])
    table_name = params['table_name']
    query = f"""
        SELECT d_aln FROM ab_vdj a
        WHERE seq_id >= {min_id} AND seq_id < {max_id}
            AND NOT EXISTS (
                SELECT 1 FROM {table_name} b
                WHERE a.seq_id = b.query_id
            )
    ;"""
    rows = QueryComplex(params['verbose']).list_data(query)
    meta['rows'] = len(rows)
    for row in rows:
        row['aln_file'] = os.path.join(params['output_protein_dir'], row['d_aln'])
        if os.path.isfile(row['aln_file']):
            yield row

def build(row_iter, params, meta):
    for row in row_iter:
        hits = ParseBlastXml(row['aln_file']).hits()
        for hit in hits:
            meta['hits'] += 1
            item = {
                'query_id': hit['query'],
                'evalue': hit.get('evalue'),
                'bit_score': hit.get('bit_score'),
                'identities': hit.get('identities'),
                'query_len': hit.get('query_len'),
                'align_len': hit.get('align_len'),
                'query_start': hit.get('query_start'),
                'query_end': hit.get('query_end'),
                'query_seq': hit.get('query_seq'),
                'match_seq': hit.get('match_seq'),
                'sbjct_seq': hit.get('sbjct_seq'),
                'sbjct_start': hit.get('sbjct_start'),
                'sbjct_end': hit.get('sbjct_end'),
            }
            if 'hit_id' in hit:
                items = hit['hit_id'].split('|')
                item['hit_id'] = items[0]
                if len(items) > 1:
                    item['organism'] = items[1]
            rec = [item.get(col) for col in params['table_cols']]
            yield tuple(rec)

if __name__ == "__main__":
    params.update({
        'chunk_size': 10_000,
        'table_name': 'ab_dregion',
        'table_cols': ['query_id', 'hit_id', 'organism', 'evalue', 'bit_score',
            'identities', 'query_len', 'align_len', 'query_start', 'query_end',
            'query_seq', 'match_seq', 'sbjct_seq', 'sbjct_start', 'sbjct_end',],
    })

    # parse alignments
    rows = retrieve(params, meta)
    #  build records
    record_iter = build(rows, params, meta)
    print(f"Try to insert data into {params['table_name']}...")
    bc = BuildComplex(params['verbose'])
    bc.insert_batch_records(record_iter, params['table_name'], params['table_cols'])

    footer(meta)