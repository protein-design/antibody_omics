#!/usr/bin/python
'''
requirements:
    - table ab_vdj
example:
    - parallel -j4 python app.py ab_jregion ::: {0..400}
    - python app.py ab_jregion 0
function:
    - parase alignment and insert J-region into table ab_jregion
'''

from ..ab_helper import *
from bioomics import ParseBlastXml

@header
def retrieve(params, meta):
    min_id = int(params['group_no']) * int(params['chunk_size'])
    max_id = min_id + int(params['chunk_size'])
    table_name = params['table_name']
    query = f"""
        SELECT d_aln FROM ab_vdj
        WHERE seq_id >= {min_id} AND seq_id < {max_id}
            AND seq_id NOT IN (
                SELECT query_id FROM {table_name}
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
            allele = ParseBlastXml.parse_imgt_allele(hit['hit_id'])
            item.update(allele)
            rec = [item.get(col) for col in params['table_cols']]
            yield tuple(rec)

if __name__ == "__main__":
    params.update({
        'chunk_size': 10_000,
        'table_name': 'ab_jregion',
        'table_cols': ['query_id', 'allele_name', 'specie', 'gene_name', 'gene_family',
            'chain_type', 'isotype', 'evalue', 'bit_score', 'identities', 'query_len',
            'align_len', 'query_start', 'query_end', 'query_seq', 'match_seq',
            'sbjct_seq', 'sbjct_start', 'sbjct_end',],
    })

    # parse alignments and build records
    rows = retrieve(params, meta)
    record_iter = build(rows, params, meta)
    print(f"Try to insert data into {params['table_name']}...")
    bc = BuildComplex(params['verbose'])
    bc.insert_batch_records(record_iter, params['table_name'], params['table_cols'])

    footer(meta)

