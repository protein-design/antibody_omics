'''
example:
    - python app.py inn_blastp
functions:
    - collect antibody chain sequences of INN
    - blastp against pdb antibody
    - put alignment to table
'''

from ..ab_helper import *
from bioomics import ProcessFasta, ProcessBlast

def pull_data(params, meta):
    query = '''
        SELECT DISTINCT pro_id AS id, chain_seq AS seq
        FROM inn_seq C
        LEFT JOIN protein_source S
        ON C.chain_id = S.source_id
        WHERE S.source_name = 'imgt_inn_chain';
    '''
    rows = QueryComplex(params['verbose']).list_data(query)
    meta['num_records'] = len(rows)
    return rows

if __name__ == "__main__":
    params.update({
        'overwrite': True,
        'db_pdb_antibody': os.getenv("db_pdb_antibody"),
        'table_name': 'inn_blastp',
    })


    params['outdir'] = os.path.join(params['output_protein_dir'], params['table_name'])
    Path(params['outdir']).mkdir(parents=True, exist_ok=True)

    # prepare query fasta
    name = 'inn_mabs'
    fa_file = os.path.join(params['outdir'], f'{name}.faa')
    if params['overwrite'] or not os.path.isfile(fa_file):
        rows = pull_data(params, meta)
        ProcessFasta(fa_file).row_seq(rows)

    # blastp, reference is pdb antibody
    outfmt = 5
    aln_file = os.path.join(params['outdir'], f'{name}_pdb_antibody.blastp{outfmt}')
    if params['overwrite'] or not os.path.isfile(aln_file):
        pb = ProcessBlast(params['outdir'], params['verbose'])
        pb.blastp(fa_file, params['db_pdb_antibody'], aln_file, outfmt)
    

    # insert aignment
    table_name = 'imgt_inn_blastp'
    bc = BuildComplex([aln_file,], params['verbose'])
    bc.empty_table(table_name)
    bc.insert_imgt_inn_blastp()

    print(meta)

