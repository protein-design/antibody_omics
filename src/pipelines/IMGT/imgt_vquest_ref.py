'''
example: 
    - abomics imgt_vquest_ref
functions:
    - prepare references for Igblast
'''
from src.ab_helper import *
from abomics import ImgtVquest, ProcessIgblast


def build(params):
    p = ProcessIgblast(params['igblast_bin'])
    

    for region in list('VDJ'):
        data_dir = params['imgt_dir'] / 'V-QUEST' / 'IMGT_V-QUEST_reference_directory'
        outdir = params['imgt_dir'] / 'V-QUEST' / 'database' / region
        outdir.mkdir(parents=True, exist_ok=True)
        
        #export fasta
        fa_file = ImgtVquest(data_dir).pro_ref(outdir, region)
        
        #build database for igblast alignment
        p.build_pro_db(fa_file, outdir)

if __name__ == "__main__":
    params.update({
        'igblast_bin': os.getenv('igblast_bin'),
    })
    
    build(params)
    
    
