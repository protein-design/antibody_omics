'''
example: 
    - parallel -j12 python src/pipelines/absd_faa.py ::: {0..400}
    - python src/pipelines/absd_faa.py 0
functions:
    - download data from ABSD
    - put data to table absd_faa
'''
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

from ..ab_helper import *
from src.bioomics import ProcessFasta

def get_data(idx, params, meta):
    end = (idx + 1 ) * 10_000
    start = end - 10_000
    table_name = params['table_name']
    query = f"""
        SELECT seq_id , pro_seq
        FROM absd_seq
        WHERE seq_id >= {start}
            AND seq_id < {end}
            AND seq_id NOT IN (
                SELECT seq_id FROM {table_name}
            );
    """
    rows= QueryComplex(params['verbose']).list_data(query)
    meta['rows'] = len(rows)
    return rows 

def to_fasta(rows, params):
    data_dir = os.path.join(params['absd_dir'], 'data')
    for row in rows:
        seq_id = row['seq_id']
        g = str(int(int(seq_id)/5000))
        outdir = os.path.join(data_dir, g, str(seq_id))
        Dir(outdir).init_dir()
        fa_file = os.path.join(outdir, f'{seq_id}.faa')
        if params['overwrite'] or not os.path.isfile(fa_file):
            record = SeqRecord(
                Seq(row['pro_seq']),
                id = str(seq_id),
                description=''
            )
            ProcessFasta(fa_file).to_fasta(record)
            meta['to_fasta'] += 1
        else:
            meta['skip'] += 1
        if os.path.isfile(fa_file):
            yield seq_id, fa_file


if __name__ == "__main__":
    params.update({
        'overwrite': False,
        'chunk_size': 100,
        'absd_dir': os.getenv('absd_dir'),
        'table_name': 'absd_faa',
    })
    idx = int(sys.argv[1])
    rows = get_data(idx, params, meta)
    if len(rows) > 0:
        record_iter = to_fasta(rows, params)
    
        # insertion
        bc = BuildComplex(record_iter, params['verbose'], params['chunk_size'])
        bc.insert_batch_records(params['table_name'])
    
    print(meta)

