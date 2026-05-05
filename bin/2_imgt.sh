#! /usr/bin/bash
APP=/home/yuan/bio/antibody_omics/app.py

echo 'Data from IMGT/INN...'
python ${APP} inn
python ${APP} inn_seq

# identify INN sequences
python ${APP} inn_region
python ${APP} inn_cdomain
python ${APP} inn_vdomain
python ${APP} inn_cdr

#IMGT/GENE-DB
python ${APP} imgt_genelist
python ${APP} imgt_gene
python ${APP} imgt_geneseq

# multiple alignment with IMGT germline
# parallel -j4 python ${APP} imgt_msa ::: {0..237}

