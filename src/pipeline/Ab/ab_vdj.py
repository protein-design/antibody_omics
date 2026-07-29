'''
requirments:
    - aligner igblast is ready. 
    - aligner blastp is ready.
    - database for igblastp and blastp alignment is ready
example: current total antibody 3,507,107
    - parallel -j8 python app.py ab_vdj ::: {0..400}
    - python app.py ab_vdj 0
functions:
    - igblastp against IMGT v-region
    - blastp against IMGT d/j-region
    - put meta data to table ab_vdj
'''
from pathlib import Path

from ..ab_helper import *
from bioomics import ProcessIgblast, ProcessBlast, ProcessFasta

@header
def retrieve(params, meta):
    min_id = int(params['chunk_size']) * int(params['group_no'])
    max_id = min_id + int(params['chunk_size'])
    table_name = params['table_name']
    query = f"""
        SELECT proseq_name, seq_id, seq
        FROM view_proseq
        WHERE seq_id >= {min_id} AND seq_id < {max_id}
            AND seq IS NOT NULL
            AND source IN ('ABSD', 'IMGT-INN')
            AND seq_id NOT IN(
                SELECT seq_id FROM {table_name}
            )
    ;"""
    rows = QueryComplex(params['verbose']).list_data(query)
    meta['rows'] = len(rows)
    return rows

def run(rows, params, meta):
    for row in rows:
        proseq_name = row['proseq_name']
        seq_id = str(row['seq_id'])
        item = {
            'proseq_name': proseq_name,
            'seq_id': seq_id,
        }

        # output
        endpoint = os.path.join(params['table_name'], proseq_name, seq_id[:3], seq_id)
        outdir = os.path.join(params['output_protein_dir'], endpoint)
        Path(outdir).mkdir(parents=True, exist_ok=True)

        # prepare query fasta
        faa_name = f"{seq_id}.faa"
        query_fa = os.path.join(outdir, faa_name)
        ProcessFasta(query_fa).one_seq(row['seq'], seq_id)
        item['query_faa'] = os.path.join(endpoint, faa_name)

        # v-region using igblastp
        outfmt = 3
        outfile_name = f"{seq_id}.vregion.igblastp{outfmt}"
        aln_file = os.path.join(outdir, outfile_name)
        if params['overwrite'] or not os.path.isfile(aln_file):
            c = ProcessIgblast(params['igblast_bin'], None, params['verbose'])
            status = c.igblastp(query_fa, params['db_vregion'], aln_file, outfmt)
            meta[f'vregion_{status}'] += 1
        else:
            meta['vregion_skip'] += 1
        if os.path.isfile(aln_file):
            item['v_aln'] = os.path.join(endpoint, outfile_name)

        # d-region using blastp
        outfmt = 5
        outfile_name = f"{seq_id}.dregion.blastp{outfmt}"
        aln_file = os.path.join(outdir, outfile_name)
        if params['overwrite'] or not os.path.isfile(aln_file):
            c = ProcessBlast(None, params['verbose'])
            status = c.blastp(query_fa, params['db_dregion'], aln_file, outfmt)
            meta[f'dregion_{status}'] += 1
        else:
            meta['dregion_skip'] += 1
        if os.path.isfile(aln_file):
            item['d_aln'] = os.path.join(endpoint, outfile_name)

        # j-region using blastp
        outfmt = 5
        outfile_name = f"{seq_id}.jregion.blastp{outfmt}"
        aln_file = os.path.join(outdir, outfile_name)
        if params['overwrite'] or not os.path.isfile(aln_file):
            c = ProcessBlast(None, params['verbose'])
            status = c.blastp(query_fa, params['db_jregion'], aln_file, outfmt)
            meta[f'jregion_{status}'] += 1
        else:
            meta['jregion_skip'] += 1
        if os.path.isfile(aln_file):
            item['j_aln'] = os.path.join(endpoint, outfile_name)

        rec = [item.get(col) for col in params['table_cols']]
        yield tuple(rec)

if __name__ == "__main__":
    params.update({
        'overwrite': False,
        'chunk_size': 10_000,
        'igblast_bin': os.getenv("igblast_bin"),
        'db_vregion': os.getenv("db_vregion"),
        'db_dregion': os.getenv("db_dregion"),
        'db_jregion': os.getenv("db_jregion"),
        'table_name': 'ab_vdj',
        'table_cols': ['proseq_name', 'seq_id', 'query_faa', \
            'v_aln', 'd_aln', 'j_aln',],
    }) 
    rows = retrieve(params, meta)
    # igblastp agaist IMGT V/D/J-region
    record_iter = run(rows, params, meta)

    # put meta data to table meta_pdb_igblastp
    bc = BuildComplex(params['verbose'])
    bc.insert_batch_records(record_iter, params['table_name'], params['table_cols'])

    footer(meta)
