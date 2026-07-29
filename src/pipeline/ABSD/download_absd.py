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


if __name__ == "__main__":
    params.update({
        'absd_dir': os.getenv('absd_dir'),
        'table_name': 'absd',
        'table_cols': ['release_date', 'specie', 'faa_file'],
    })
    
    footer(meta)

