'''
example:  5 species
    - parallel -j5 abomics absd_source 4 ::: {0..4}
    - abomics absd_source 4
functions:
    - download data from ABSD
    - put data to table absd_source
'''
import re
from src.ab_helper import *
from abomics import Absd

def scan(params):
    files = QueryComplex(params['verbose']).unique_values(params['table_name'], 'faa_file')
    records = []
    file_iter = Absd(params['absd_dir'], params['verbose']).scan_files('fasta')
    for specie, path in file_iter:
        if path not in files:
            version = re.findall(r'absd-(\d+-\d+-\d+)/', path)
            rec = (version[0], specie, path)
            records.append(rec)
    return records

if __name__ == "__main__":
    params.update({
        'absd_dir': os.getenv('absd_dir'),
        'table_name': 'absd',
        'table_cols': ['release_date', 'specie', 'faa_file'],
    })

    records = scan(params)
    bc = BuildComplex(records, params['verbose'])
    bc.insert_batch_records(params['table_name'], params['table_cols'])
    
    footer(meta)

