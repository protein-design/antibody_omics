#! /usr/bin/python
'''
example:
    - python app.py <module name>
'''
import os
import sys
import subprocess

pool = {
    #ABSD
    'absd': 'pipeline.ABSD.absd',
    'absd_record': 'pipeline.ABSD.absd_record',
    'absd_source': 'pipeline.ABSD.absd_source',
    'absd_pro_seq': 'pipeline.ABSD.absd_pro_seq',
    'absd_seq': 'pipeline.ABSD.absd_seq',

    # IMGT-INN
    'inn': 'pipeline.IMGT.inn',
    'inn_seq': 'pipeline.IMGT.inn_seq',
    'inn_region': 'pipeline.IMGT.inn_region',
    'inn_cdomain': 'pipeline.IMGT.inn_cdomain',
    'inn_vdomain': 'pipeline.IMGT.inn_vdomain',
    'inn_cdr': 'pipeline.IMGT.inn_cdr',

    #IMGT-GENE
    'imgt_genelist': 'pipeline.IMGT.imgt_genelist',
    'imgt_gene': 'pipeline.IMGT.imgt_gene',
    'imgt_geneseq': 'pipeline.IMGT.imgt_geneseq',

    # data from other datbases
    'aacdb': 'pipeline.other.aacdb',
    'sabdab': 'pipeline.other.sabdab',
    'sabdab_chain': 'pipeline.other.sabdab_chain',
    'abybank': 'pipeline.other.abybank',

    #antibody
    'ab_faa': 'pipeline.Ab.ab_faa',
    'ab_vdj': 'pipeline.Ab.ab_vdj',
    'ab_vfrag': 'pipeline.Ab.ab_vfrag',
    'ab_vregion': 'pipeline.Ab.ab_vregion',
    'ab_dregion': 'pipeline.Ab.ab_dregion',
    'ab_jregion': 'pipeline.Ab.ab_jregion',

    # demo
    'test': 'pipeline.test',
}

# build cmd
project_dir = os.path.dirname(__file__)
name = sys.argv[1] if len(sys.argv) > 1 else None


cmd = ['python', '-m',]
if name in pool:
    cmd.append(pool[name])
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
