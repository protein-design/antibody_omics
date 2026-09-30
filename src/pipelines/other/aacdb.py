'''
example: 
    - abomics aacdb
functions:
    - download protein_table.txt from AACDB, No sequences
    - put meta data to table aacdb
'''
import pandas as pd

from src.ab_helper import *

def retrieve_data(params, meta):
    infile = params['rawdata_dir'] / params['source'] / 'protein_table.txt'
    df = pd.read_csv(infile, sep='\t')
    if params['verbose']:
        print('Size of AACDB: ', df.shape)
    meta['rows'] = len(df)
    rows = df.to_dict(orient='records')
    if params['verbose']:
        print('columns: ', list(rows[0]))
    for row in rows:
        pdb_id = row.get('pdb')
        if pdb_id:
            chains = row['chains'].split('_')
            rec = (
                pdb_id.upper(),
                chains[0] if chains else None, #antiboby_chains
                chains[1] if len(chains) > 1 else None, # antigen_chains
                row.get('antibody'),
                row.get('protein'),
                row.get('INN(clinical_trial)'), #drug
                row.get('targets'),
                row.get('method'),
                row.get('organism'),
                row.get('resolution'),
                row.get('reference'),
            )
            yield rec


if __name__ == "__main__":
    params.update({
        'chunk_size': 50,
        'source': 'AACDB', 
        'table_name': 'aacdb',
        'table_cols': ['pdb_id', 'antibody_chains', 'antigen_chains',
            'antibody', 'protein', 'drug', 'targets', 'method',
            'organism', 'resolution', 'reference'],

    })
    
    DeleteComplex(params['verbose']).empty_table(params['table_name'])
    
    # prepare data
    record_iter = retrieve_data(params, meta)

    # insertion
    print(f"Try to update data from AACDB into table {params['table_name']}.")
    bc = BuildComplex(params['verbose'], params['chunk_size'])
    bc.insert_batch_records(record_iter, params['table_name'], params['table_cols'])

    footer(meta)



