'''
example:  5 species
    - parallel -j5 abomics absd_source 4 ::: {0..4}
    - abomics absd_source 4
functions:
    - download data from ABSD https://absd.pasteur.cloud/
'''
import json
import subprocess
import requests
from src.ab_helper import *


def retrieve(params):
    url = 'https://absd.pasteur.cloud/api/downloads'
    res = requests.get(url)
    versions = json.loads(res.text)
    for i, file_name in enumerate(versions):
        local_file = params['absd_dir'] / file_name
        version = file_name.replace('.tar.gz', '')
        version_path = params['absd_dir'] / version
        if params['overwrite'] or not local_file.is_file():
            cmd = ['wget', f'{url}/{file_name}', '-P', params['absd_dir'],]
            try:
                print(f"Try to download {version} fro ABSD.")
                result= subprocess.run(cmd, check=True, capture_output=True, text=True)
            except Exception as e:
                print(e)
        else:
            print(f"Skip download {version} fro ABSD.")
        
        if local_file.is_file():
            yield version, local_file
                
def unzip(params, file_iter):
    for version, local_file in file_iter:
        outdir = params['absd_dir'] / version
        if params['overwrite'] or not outdir.is_dir():
            outdir.mkdir(parents=True, exist_ok=True)
            cmd = ['tar', 'zxvf', str(local_file), '-C', str(outdir)]
            try:
                print(f"Try decompress {local_file}")
                result= subprocess.run(cmd, check=True, capture_output=True, text=True)
            except Exception as e:
                print(e)
        else:
            print(f"Skip decompress {local_file}")


if __name__ == "__main__":
    params.update({
        'overwrite': False,
    })
    params['absd_dir'] = params['rawdata_dir'] / 'ABSD'
    params['absd_dir'].mkdir(parents=True, exist_ok=True)

    file_iter = retrieve(params)
    unzip(params, file_iter)
   
