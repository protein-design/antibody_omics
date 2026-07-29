'''
set imports required by all pipelines
'''
from pathlib import Path
from collections import defaultdict
from dotenv import load_dotenv
import functools
import os
import sys
import socket

bioomics_path = '/home/yuan/bio/bio_omics/src'
for _path in (bioomics_path,):
    if _path not in sys.path:
        sys.path.append(_path)

# env_file = os.path.join(src_dir, '.env')
# load_dotenv(env_file)
load_dotenv()

# initiate parameters
params = {
    'chunk_size':100,
    'group_no': sys.argv[1] if len(sys.argv) > 1 else None,
    'verbose': True if os.getenv('verbose') == 'true' else False,
    'rawdata_dir': Path(os.getenv('rawdata_dir')),
    'output_dir': Path(os.getenv('output_dir')),
    'host': socket.gethostname(),
}
params['rawdata_pdb_dir'] = params['rawdata_dir'] / 'pdb'
params['absd_dir'] = params['rawdata_dir'] / 'ABSD'
params['output_pdb_dir'] = params['output_dir'] / 'pdb'
params['output_protein_dir'] = params['output_dir'] / 'protein'
params['simulate_dir'] = params['output_dir'] / 'simulate'
params['predict_dir'] = params['output_dir'] / 'predict'
params['design_dir'] = params['output_dir'] / 'design'
meta = defaultdict(int)


from bioomics.database import DeleteComplex, BuildComplex, UpdateComplex, QueryComplex

def header(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        params, meta = args
        group_no = params.get('group_no')
        table = params.get('table_name')
        print("#########\n")
        print(f"pdb group = {group_no}")
        print(f"Try to retrieve data from {table}...")
        meta['group_no'] = group_no
        meta['host'] = socket.gethostname()
        result = func(*args, **kwargs)
        return result
    return wrapper

def validate_data(col_name, params, meta):
    group_no = params['group_no']
    table_name = params['table_name']
    # scan no existing files
    print(f"Scan {table_name}.{col_name}, group={group_no}.", end=' ')
    query = f"""
        SELECT S.pdb_id, S.{col_name}
        FROM {table_name}  S
        LEFT JOIN meta_pdb P ON S.pdb_id = P.pdb_id
        WHERE P.group_no = {group_no}
            AND S.{col_name} IS NOT NULL
    ;"""
    rows = QueryComplex(params['verbose']).list_data(query)
    del_pool = []
    for row in rows:
        pdb_file = params['output_pdb_dir'] / row[col_name]
        if pdb_file.is_file():
            del_pool.append(row[col_name])
    
    # delete rows
    n = len(del_pool)
    if n > 0:
        print(f"Number of {n} out of {len(rows)} are not existing.", end=' ')
        print(f"Try to delete rows in {table_name}...", end='')
        uc = UpdateComplex(table_name, params['verbose'])
        chunk_size = 100
        for i in range(0, n-chunk_size, chunk_size):
            values = del_pool[i:i+chunk_size]
            uc.delete_rows(col_name, values)
            meta['delete_rows'] += len(values)
            print(i, end=' ')
        print(f'{n}\n')

def footer(meta, params:dict={}):
    # update table meta_execute with end time
    if params.get('meta_execute'):
        UpdateComplex('meta_execute', params['verbose']).execute_end_time(params)
    # print statistics of this run
    print('Statistics of this run', meta)
    print("Done!\n\n")