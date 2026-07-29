'''
example: 
    - abomics inn_seq
functions:
    - put data to table inn_seq
'''
from src.ab_helper import *
from abomics import PullData

def build(inn_data, meta):
    # retrieve
    rows = []
    for inn_data in data_iter:
        inn_number = ','.join(inn_data['inn_number'])
        for chain in inn_data.get('chains', []):
            meta['records'] += 1
            seq = chain.get('chain_seq')
            row = {
                'inn_number': inn_number,
                'inn_chain_id': chain['chain_id'],
                'chain_desc': chain['chain_description'],
                'seq': seq,
            }
            rows.append(row)

    #insert seq into pro_seq
    bc = BuildComplex(params['verbose'])
    qc = QueryComplex(params['verbose'])
    packed_rows = qc.pack_proseq(rows)
    for (table_name, seq_len), rows in packed_rows:
        # detect known seqs
        parsed, unparsed = qc.parse_seqid(table_name, seq_len, rows)

        # insert new seqs
        num_insertion, fail = bc.insert_proseq(params['source'], table_name, unparsed)
        meta['new_insertion'] += num_insertion
        meta['fail_insert'] += len(fail)
        # parse new seqs
        new_parsed, fail = qc.parse_seqid(table_name, seq_len, unparsed)
        meta['fail_insert'] += len(fail)

        #build record
        for row in parsed + new_parsed:
            yield tuple([row[i] for i in params['table_cols']])
            meta['records'] += 1    

    
if __name__ == "__main__":
    params.update({
        'chunk_size': 50,
        'source': 'IMGT-INN',
        'table_name': 'inn_seq',
        'table_cols': ['inn_number', 'inn_chain_id', 'chain_desc',
            'seq', 'proseq_name', 'seq_id',],
    })
    # empty table
    DeleteComplex(params['verbose']).empty_table(params['table_name'])
        
    # pull records from IMGT
    data_iter = PullData(params['imgt_dir'], meta).flat_inn()
    record_iter = build(data_iter, meta)
    
    # insert data to inn_seq    
    bc = BuildComplex(params['verbose'], params['chunk_size'])
    bc.insert_batch_records(record_iter, params['table_name'], params['table_cols'])
    
    footer(meta)