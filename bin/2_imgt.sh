#! /usr/bin/bash
APP=/home/yuan/bio/antibody_omics/app.py

echo 'Data from IMGT/INN...'
python ${APP} inn
python ${APP} inn_seq

# identify INN sequences
python ${APP} inn_region &
P1=$!
python ${APP} inn_cdomain &
P2=$!
python ${APP} inn_vdomain &
P3=$!
python ${APP} inn_cdr &
P4=$!
wait $P1 $P2 $P3 $P4

#IMGT/GENE-DB
python ${APP} imgt_genelist &
P1=$!
python ${APP} imgt_gene &
P2=$!
python ${APP} imgt_geneseq &
P3=$!
wait $P1 $P2 $P3

# multiple alignment with IMGT germline
# parallel -j4 python ${APP} imgt_msa ::: {0..237}

