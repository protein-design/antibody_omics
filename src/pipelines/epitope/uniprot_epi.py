'''
example: 
    - abomics uniprot_epi
functions:
    - epitope mapping of uniprot-sprot proteins
'''
import json
from src.ab_helper import *
from abomics import EpitopeMapping

@header
def validate_dir_row(params, meta):
    group_no = params['group_no']
    table_name = params['table_name']
    col_name = 'relative_outdir'
    # scan no existing files
    print(f"Scan {table_name}.{col_name}, group={group_no}.", end=' ')
    query = f"""
        SELECT S.predictor, S.{col_name}
        FROM {table_name}  S
        LEFT JOIN view_pdb_chain P ON S.chain_id = P.chain_id
        WHERE P.pdb_group = {group_no}
    ;"""
    rows = QueryComplex(params['verbose']).list_data(query)
    del_pool = []
    for row in rows:
        _dir = params['output_protein_dir'] / row[col_name]
        if not _dir.is_dir():
            del_pool.append(row[col_name])
    
    # delete rows
    DeleteComplex(params['verbose']).remove_null_rows(table_name, col_name, del_pool)

def retrieve(params, meta):
    group_no = params['group_no']
    table_name = params['table_name']
    predictor = params['predictor']
    query = f"""
        WITH tmp AS (
            SELECT chain_id FROM {table_name}
            WHERE predictor = '{predictor}'
        )
        SELECT c.pdb_id, c.chain_id, c.chain_no, c.relative_faa
        FROM view_pdb_chain    c
        WHERE c.pdb_group = {group_no}
            AND c.pro_len >= 20
            AND c.chain_id = c.first_chain_id
            AND NOT EXISTS (
                SELECT 1 FROM tmp t
                WHERE c.chain_id = t.chain_id
            )
    ;"""
    rows = QueryComplex(params['verbose']).list_data(query)
    meta[f"{predictor}_rows"] = len(rows)
    frows = []
    for row in rows:
        faa_file = params['output_pdb_dir'] / row['relative_faa']
        if faa_file.is_file():
            row['query_fasta'] = faa_file
            frows.append(row)
    print(f"Retrieve {len(frows)} rows")
    return frows

def run(rows, params, meta):
    em = EpitopeMapping(params)
    for row in rows:
        endpoint = Path(params['table_name']) / row['pdb_id'][:2] / row['pdb_id'] / row['chain_id']
        output_dir = params['output_protein_dir'] / endpoint
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # build settings
        json_file = output_dir / 'settings.json'
        if params['verbose'] or not json_file.is_file():
            settings = {
                "output_dir": str(output_dir),
                'query_fasta': str(row['query_fasta']),
                'chain_name': row['chain_no'],
            }
            with open(json_file, 'w') as f:
                json.dump(settings, f, indent=4)
        
        #prediction
        done_txt = output_dir / params['predictor'] / 'DONE.txt'
        if not done_txt.exists():
            res = em.predict(json_file)
            if res == 0:
                meta[f"{params['predictor']}_good"] += 1
            else:
                meta[f"{params['predictor']}_fail"] += 1
        else:
            meta[f"{params['predictor']}_skip"] += 1

        # build record
        if done_txt.exists():
            relative_outdir = str(endpoint / params['predictor'])
            rec = (row['chain_id'], params['predictor'], relative_outdir)
            meta[f"{params['predictor']}_insertion"] += 1
            yield rec


        

if __name__ == "__main__":
    params.update({
        'overwrite': False,
        'chunk_size': 10,
        'epi_ann_dir': os.getenv('epi_ann_dir'),
        'epi_rnn_dir': os.getenv('epi_rnn_dir'),
        'table_name': 'pdb_epi',
        'table_cols': ['chain_id', 'predictor', 'relative_outdir',],
    }) 
    validate_dir_row(params, meta)
    
    for predictor in ('ANN', 'RNN'):
        params['predictor'] = predictor
        rows = retrieve(params, meta)
        record_iter = run(rows, params, meta)
        bc = BuildComplex(params['verbose'], params['chunk_size'])
        bc.insert_batch_records(record_iter, params['table_name'], params['table_cols'])

    footer(meta)
