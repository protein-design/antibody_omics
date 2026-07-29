'''
example: 
    - python aap.py aacdb
functions:
    - download protein_table.txt from AACDB, No sequences
    - put meta data to table aacdb
'''
from pathlib import Path
import pandas as pd

from ..ab_helper import *

def download(params):
    outdir = os.path.join(params['rawdata_dir'], params['source'])
    Path(outdir).mkdir(parents=True, exist_ok=True)
    url = 'https://i.uestc.edu.cn/AACDB/data_zip'
    os.system(f"wget -c {url}/protein_table.txt -P {outdir}")
    return outdir

def retrieve_data(params, meta, outdir):
    infile = os.path.join(outdir, 'protein_table.txt')
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
        'rawdata_dir': os.getenv("rawdata_dir"),
        'source': 'AACDB', 
        'table_name': 'aacdb',
        'table_cols': ['pdb_id', 'antibody_chains', 'antigen_chains',
            'antibody', 'protein', 'drug', 'targets', 'method',
            'organism', 'resolution', 'reference'],

    })
    # prepare data
    outdir = download(params)
    record_iter = retrieve_data(params, meta, outdir)

    # insertion
    print(f"Try to update data from AACDB into table {params['table_name']}.")
    bc = BuildComplex(params['verbose'], params['chunk_size'])
    bc.empty_table(params['table_name'])
    bc.insert_batch_records(record_iter, params['table_name'], params['table_cols'])

    footer(meta)



