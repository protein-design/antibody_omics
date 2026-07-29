'''
example:  5 species
    - abomics absd
functions:
    - load ABSD meta data
'''
import re
from src.ab_helper import *
from abomics import Absd

def scan(params):
    files = QueryComplex(params['verbose']).unique_values(params['table_name'], 'relative_fasta')
    records = []
    file_iter = Absd(params['absd_dir'], params['verbose']).scan_fasta()
    for release_date, specie, path in file_iter:
        relative_fasta = re.sub(f'{params['absd_dir']}/', '', str(path))
        if relative_fasta not in files:
            rec = (release_date, specie, relative_fasta)
            records.append(rec)
    return records

if __name__ == "__main__":
    params.update({
        'table_name': 'absd',
        'table_cols': ['release_date', 'specie', 'relative_fasta'],
    })

    records = scan(params)
    bc = BuildComplex(params['verbose'])
    bc.insert_batch_records(records, params['table_name'], params['table_cols'])
    
    footer(meta)

