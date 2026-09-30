'''
example: 
    - abomics imgt_collect
functions:
    - build reference sequencs in fasta
    - build igblast db by specie or VDJ regions
'''

from src.ab_helper import *
from abomics import ImgtGenedb



if __name__ == "__main__":
    params.update({
        'overwirte': True,
    })

    ig = ImgtGenedb(params['imgt_dir'], params['verbose'])

    print('\nRetrieve from gene list to json by spcies')
    ig.build_specie_genelist_json()


    print("\nRetrieve AA sequences to fasta by v-regions")
    ig.build_region_fasta()

    print("Build igblastp database given region fasta ")
    ig.build_igblastp_region(params['igblast_bin'])


    print("\nBuild fa and db by organism+spcie")
    ig.build_organism_fasta()
    
    print("Build igblastp database given organism fasta ")
    ig.build_igblastp_organism(params['igblast_bin'])

