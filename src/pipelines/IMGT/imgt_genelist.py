'''
requirements:
    - IMGT GeneList
example:
    - abomics imgt_genelist
functions:
    - build table imgt_genelist
'''

from src.ab_helper import *
from abomics import ImgtGenedb

def build(data:dict, meta):
    names = ['Species', 'IMGT/GENE-DB', 'IMGT gene functionality', \
        'IMGT and HGNC gene definition', 'Number of alleles', \
        'Chromosome', 'Chromosomal localization', \
        'IMGT/LIGM-DB reference sequence(s) for allele *01', \
        'NCBI Gene', 'chain', 'domain']
    for record in data:
        meta['records'] += 1
        rec = [record.get(i, '') for i in names]
        yield tuple(rec)


if __name__ == "__main__":
    params.update({
        'table_name': 'imgt_genelist',
        'table_cols': ['species', 'gene_db', 'gene_function',
            'gene_definition', 'number_alleles', 'chromosome',
            'chromosomal_loc','ligm_db_ref_gene', 'ncbi_gene',
            'chain', 'domain',],
    })
    # empty table
    DeleteComplex(params['verbose']).empty_table(params['table_name'])
    
    #retrieve data
    ig = ImgtGenedb(params['imgt_dir'], params['verbose'])
    genelist = ig.parse_genelist(to_df=True)
    data = genelist.to_dict(orient='records')
    meta['rows'] = len(data)

    print(f"Try to insert genelist into table {params['table_name']}")
    record_iter = build(data, meta)
    bc = BuildComplex(params['verbose'])
    bc.insert_batch_records(record_iter, params['table_name'], params['table_cols'])

    footer(meta)