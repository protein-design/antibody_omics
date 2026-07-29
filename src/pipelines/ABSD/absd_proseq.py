'''
example: 
    - abomics absd_proseq
functions:
    - put unique sequences to proseq_* tables
'''
from src.ab_helper import *

   
def retrieve(params, seq_len):
    table_name = params['table_name']
    # column name must be 'seq'
    query = f"""
        SELECT a.group_no, a.absd_seq_id, a.seq
        FROM absd_record       a
        LEFT JOIN {table_name} b ON a.absd_seq_id = b.absd_seq_id
        WHERE a.seq_len = {seq_len}
            AND a.seq IS NOT NULL
            AND b.seq_id IS NULL
    """
    qc = QueryComplex(params['verbose'])
    return qc.pack_proseq(query)

def build(data_iter, params, meta):
    qc = QueryComplex(params['verbose'])
    bc = BuildComplex(params['verbose'])
    
    for (table_name, seq_len), rows in data_iter:
        # detect known seqs
        parsed, unparsed = qc.parse_seqid(table_name, seq_len, rows)
        meta['parsed'] += len(parsed)
        
        # insert new seqs into proseq_* tables
        proseq_cols = ['source', 'seq']
        new_records = []
        for i in unparsed:
            rec = (params['source'], i['seq'])
            if rec not in new_records:
                new_records.append(rec)
        num_insertion, fail = bc.insert_batch_records(new_records, table_name, proseq_cols)
        meta['new_insertion'] += num_insertion
        meta['fail_insert'] += len(fail)
        # parse new seqs with seqid
        new_parsed, fail = qc.parse_seqid(table_name, seq_len, unparsed)
        meta['fail_insert'] += len(fail)

        #build record for inertion into uniprot_proseq
        for row in parsed + new_parsed:
            yield tuple([row[i] for i in params['table_cols']])
            meta['records'] += 1

    
if __name__ == "__main__":
    params.update({
        'source': 'ABSD',
        'table_name': 'absd_proseq',
        'table_cols': ['group_no', 'absd_seq_id', 'proseq_name', 'seq_id']
    })

    pool = QueryComplex(params['verbose']).unique_values('absd_record', 'seq_len')
    for seq_len in pool:
        data_iter = retrieve(params, seq_len)
        record_iter = build(data_iter, params, meta)
        
        bc = BuildComplex(params['verbose'])
        bc.insert_batch_records(record_iter, params['table_name'], params['table_cols'])

        # update status in table absd
        meta['seq_len'] = seq_len
        footer(meta)



