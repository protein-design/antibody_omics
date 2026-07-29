'''
example: 
    - python app.py inn_seq
functions:
    - put data to table inn_seq
'''

from ..ab_helper import *
from src.abomics import Dir, Imgt, ParseImgtAnnot

def pull_data(params, meta):
    res = []
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

def build(inn_data, meta):
    # retrieve
    records, seqs = [], []
    for inn_data in data_iter:
        inn_number = ','.join(inn_data['inn_number'])
        for chain in inn_data.get('chains', []):
            meta['records'] += 1
            seq = chain.get('chain_seq')
            rec = [
                inn_number,
                chain['chain_id'],
                chain['chain_description'],
                seq,
            ]
            records.append(rec)
            seqs.append(seq)

    #insert seq into pro_seq
    bc = BuildComplex(params['verbose'])
    num_succeed, fail = bc.insert_proseq(seqs, params['source'])
    meta['new_seqs'] = num_succeed
    meta['no_insertion'] = len(fail)

    #parse id
    qc = QueryComplex(params['verbose'])
    seq_seqids, unparsed = qc.parse_seqid(seqs)
    meta['parsed_ids'] = len(seq_seqids)
    meta['unparse'] = len(unparsed)
    for rec in records:
        seq = rec[-1]
        if seq in seq_seqids:
            seq_id = seq_seqids[seq]
            rec.append(seq_id)
        else:
            rec.append(None)
        yield tuple(rec)
    
if __name__ == "__main__":
    params.update({
        'chunk_size': 50,
        'imgt_dir': os.getenv('imgt_dir'),
        'table_name': 'inn_seq',
        'table_cols': ['inn_number', 'inn_chain_id', 
            'description', 'seq', 'seq_id',],
        'source': 'IMGT-INN',
    })
    # pull records from IMGT
    inn = Imgt(params['imgt_dir'], params['verbose'])
    data_iter = pull_data(params, meta)
    record_iter = build(data_iter, meta)
    
    bc = BuildComplex(params['verbose'], params['chunk_size'])
    bc.empty_table(params['table_name'])
    bc.insert_batch_records(record_iter, params['table_name'], params['table_cols'])
    
    footer(meta)

