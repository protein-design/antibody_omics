'''
example: 
    - python app.py inn_vdomain
functions:
    - download data from IMGT
    - put data to table inn_vdomain
'''

from ..ab_helper import *
from bioomics import Dir, ParseImgtAnnot

def pull_data(params, meta):
    indir = os.path.join(params['imgt_dir'], '3Dstructure-DB', 'IMGT3DFlatFiles')
    for gz_file in Dir(indir).recursive_files():
        if gz_file.endswith('.inn.gz'):
            try:
                inn_data = ParseImgtAnnot(gz_file)()
                meta['inn_data'] += 1
                yield inn_data
            except Exception as e:
                print(f"{gz_file}, error={e}")
                meta['invalid_inn'] += 1


def build(data_iter, meta):
    for inn_data in data_iter:
        for chain in inn_data.get('chains', []):
            for domain in chain.get('v_domain', []):
                rec = (
                    chain['chain_id'],
                    domain.get("IMGT domain description"),
                    domain.get("CDR-IMGT length"),
                    domain.get("FR-IMGT length"),
                    ','.join(domain.get("IMGT gene and allele", [])),
                    domain.get('seq'),
                    domain.get('seq_cdr'),
                    domain.get('seq_align'),
                    domain.get('seq_align_cdr'),
                    domain.get('seq_cdr_mask'),
                    domain.get('seq_align_cdr_mask'),
                )
                yield rec
                meta['records'] += 1

if __name__ == "__main__":
    params.update({
        'chunk_size': 50,
        'imgt_dir': os.getenv('imgt_dir'),
        'table_name': 'inn_vdomain',
        'table_cols': ['chain_id', 'domain_name', 'cdr_length', \
            'fr_length', 'gene_allele', 'seq', 'seq_cdr', 'seq_align', \
            'seq_align_cdr', 'seq_cdr_mask', 'seq_align_cdr_mask',],
    })
    # pull records from IMGT
    data_iter = pull_data(params, meta)
    record_iter = build(data_iter, meta)

    # insertion
    bc = BuildComplex(params['verbose'], params['chunk_size'])
    bc.empty_table(params['table_name'])
    bc.insert_batch_records(record_iter, params['table_name'], params['table_cols'])
    
    print(meta)

