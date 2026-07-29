#! /usr/bin/python
'''
example:
    python src/collect/distance.py
'''
import os
import sys
import subprocess

pool = {
    #ABSD
    'download_absd': 'ABSD.download_absd',
    'absd': 'ABSD.absd',
    'absd_record': 'ABSD.absd_record',
    'absd_source': 'ABSD.absd_source',
    'absd_proseq': 'ABSD.absd_proseq',

    #IMGT
    'inn': 'IMGT.inn',
    'inn_seq': 'IMGT.inn_seq',
    'inn_region': 'IMGT.inn_region',
    'inn_cdomain': 'IMGT.inn_cdomain',
    'inn_vdomain': 'IMGT.inn_vdomain',
    'inn_cdr': 'IMGT.inn_cdr',
    'imgt_genelist': 'IMGT.imgt_genelist',
    'imgt_gene': 'IMGT.imgt_gene',
    'imgt_geneseq': 'IMGT.imgt_geneseq',
    
    # align
    'align_vfrag': 'align.align_vfrag',
    'align_vregion': 'align.align_vregion',
    'align_dregion': 'align.align_dregion',
    'align_jregion': 'align.align_jregion',
    'label_antibody': 'align.label_antibody',
    # 'anarci': 'immune.anarci',

    #other
    'move': 'clean.move',
    'test': 'test',
}

def main():
    # build cmd
    project_dir = os.path.dirname(__file__)
    name = sys.argv[1] if len(sys.argv) > 1 else None


    cmd = ['python', '-m',]
    path_prefix = 'src.pipelines.'
    if name in pool:
        cmd.append(path_prefix + pool[name])
    else:
        print("\nError: The argument <module_name> is not defined.\n")
        print("Usage: python app.py <module_name> [pdb_group]\n")
        sys.exit(1)

    # pass arguments
    args = sys.argv[2:] if len(sys.argv) > 2 else []
    cmd += args
    print(f"Run python script: {cmd}")

    # run
    result = subprocess.run(cmd)

if __name__ == "__main__":
    main()