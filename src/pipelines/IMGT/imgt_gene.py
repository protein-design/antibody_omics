'''
requirements:
    - IMGT GeneDB
example:
    - abomics imgt_gene
functions:
    - build table imgt_gene
'''

from src.ab_helper import *
from abomics import ImgtGenedb

def build_records(params, meta):
    ig = ImgtGenedb(params['imgt_dir'], params['verbose'])
    # read fasta and integrate sequences to self.data
    ig.parse_fasta()

    for specie, sub1 in ig.data.items():
        meta['specie'] += 1
        for gene_name, sub2 in sub1.items():
            for region_name, sub3 in sub2.items():
                for allele_name, sub4 in sub3.items():
                    meta['records'] += 1
                    record = (
                        sub4['record_id'],
                        specie,
                        gene_name[:2].upper(),
                        gene_name[2].upper(),
                        gene_name,
                        allele_name,
                        region_name,
                    )
                    yield record


if __name__ == "__main__":
    params.update({
        'chunk_size': 50,
        'table_name': 'imgt_gene',
        'table_cols': ['record_id', 'specie', 'isotype', 'chain_type',
        'gene_name', 'allele_name', 'region_name'],
    })
    
    # empty table
    DeleteComplex(params['verbose']).empty_table(params['table_name'])

    # retrieve data
    record_iter = build_records(params, meta)
        
    print(f"Try to insert genelist into table {params['table_name']}")
    bc = BuildComplex(params['verbose'], params['chunk_size'])
    bc.insert_batch_records(record_iter, params['table_name'], params['table_cols'])

    footer(meta)