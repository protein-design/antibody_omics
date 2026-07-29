'''
requirements:
    - table pro_seq
example: 
    - python app.py ab_faa
functions:
    - export antibody to fasta
'''
from pathlib import Path
import math

from ..ab_helper import *
from bioomics import ProcessFasta

def retrieve(params, meta):
    table_name = params['table_name']
    size = params['chunk_size']
    # antibody only
    query = f"""
        SELECT seq_id, seq
        FROM {table_name}
        WHERE relative_faa IS NULL
            AND source IN ('ABSD', 'INN')
        LIMIT {size}
    """
    rows = QueryComplex(params['verbose']).list_data(query)
    if len(rows) == 0:
        params['do_retrieve'] = False
    meta['rows'] = len(rows)
    return rows

def create_faa(rows, params, meta):
    uc = UpdateComplex(params['verbose'])
    for row in rows:
        seq_id = row['seq_id']
        dir_name = str(int(seq_id/params['chunk_size']))
        outdir = os.path.join(params['output_protein_dir'], params['table_name'], dir_name)
        Path(outdir).mkdir(parents=True, exist_ok=True)

        # to fasta
        file_name = f"{seq_id}.faa"
        outfile = os.path.join(outdir, file_name)
        if params['overwrite'] or (not os.path.isfile(outfile)):
            ProcessFasta(outfile).one_seq(row['seq'], seq_id)
        
        # update records
        if os.path.exists(outfile):
            relative_faa = os.path.join(params['table_name'], dir_name, file_name)
            query = f"""
                UPDATE {params['table_name']}
                SET relative_faa = '{relative_faa}'
                WHERE seq_id = {seq_id}
            ;"""
            res = uc.execute_update(query, None)
            meta['updates'] += res

if __name__ == "__main__":
    params.update({
        'overwrite': True,
        'chunk_size': 2_000,
    })

    for table_name in ('proseq_400', 'proseq_1000', 'proseq_long',):
        params['table_name'] = table_name
        params['do_retrieve'] = True
        while params['do_retrieve']:
            rows = retrieve(params, meta)
            create_faa(rows, params, meta)

    footer(meta)

