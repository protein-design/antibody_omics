#!/usr/bin/python
'''
requirements:
    - table ab_vdj
example:
    - parallel -j4 python app.py ab_vregion ::: {0..360}
    - python app.py ab_vregion 0
function:
    - parse alignments and insert data into table ab_vregion
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
        for hit in c.retrieve_hits():
            item = {'query_id': hit['query_id'],}
            if 'allele_name' in hit:
                allele_name, specie = hit['allele_name'].split('|')
                region_names = [i.replace('-IMGT', '') for i in hit.get('region_names', [])]
                item.update({
                    'allele_name': allele_name,
                    'specie': specie,
                    'gene_name': hit['gene_name'],
                    'gene_family': hit['gene_family'],
                    'chain_type': hit['chain_type'].upper(),
                    'isotype': hit['isotype'].upper(), 
                    'evalue': float(hit['e-value']),
                    'bit_score': float(hit['bits-score']),
                    'region_names': ','.join(region_names) if region_names else None,
                })
            rec = tuple([item.get(col) for col in params['table_cols']])
            if rec not in records:
                records.append(rec)
                meta['regions'] += 1
    return records
 
if __name__ == "__main__":
    params.update({
        'chunk_size': 10_000,
        'table_name': 'ab_vregion',
        'table_cols': ['query_id', 'allele_name', 'specie', \
            'gene_name', 'gene_family', 'chain_type', 'isotype', \
            'evalue', 'bit_score', 'region_names',],
    })

    # parse alignments and build records
    rows = retrieve(params, meta)
    records = build(rows, params, meta)
    if records:
        print(f"Try to insert data into {params['table_name']}...")
        bc = BuildComplex(params['verbose'])
        bc.insert_batch_records(records, params['table_name'], params['table_cols'])

    footer(meta)