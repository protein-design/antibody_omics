'''
Download data from database SAbDab https://opig.stats.ox.ac.uk
example: 
    - python app.py sabdab_chain
functions:
    - download data from SAbDab
    - put data to table sabdab_chain
'''
import pandas as pd
import numpy as np

from ..ab_helper import *

def retrieve(params, meta):
    query = """
        SELECT * FROM sabdab
        WHERE summary_file IS NOT NULL
    """
    rows = QueryComplex(params['verbose']).list_data(query)
    meta['rows'] = len(rows)
    return rows

def prepare_data(rows):
    for row in rows:
        pdb_id = row['pdb_id']
        path = row['summary_file']
        df = pd.read_csv(path, sep='\t')
        for _, row in df.iterrows():
            row = row.replace({
                np.nan: None,
                'NOT': None,
            })
            if row.get('pdb'):
                pdb_id = str(row['pdb']).upper()
                resolution = row.get('resolution')
                if resolution is None:
                    resolution = 0
                elif isinstance(resolution, str):
                    resolution = float(resolution.split(',')[0])
                record = (
                    pdb_id,
                    row['model'],
                    row['Hchain'],
                    row['Lchain'],
                    row['antigen_chain'],
                    row['antigen_type'],
                    resolution,
                )
                yield record
        

if __name__ == '__main__':
    params.update({
        'chunk_size': 5,
        'source': 'SAbDab',
        'table_name': 'sabdab_chain',
        'table_cols': ['pdb_id', 'model', 'heavy_chain', 'light_chain',
            'antigen_chain', 'antigen_type', 'resolution'],
    })

    rows = retrieve(params, meta)    
    record_iter = prepare_data(rows)
    bc = BuildComplex(params['verbose'], params['chunk_size'])
    bc.empty_table(params['table_name'])
    bc.insert_batch_records(record_iter, params['table_name'], params['table_cols'])

    print(meta)
