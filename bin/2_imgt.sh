#! /usr/bin/bash
APP="uv --direcotry=/home/yuan/bio/antibody_omics run abomics"

echo 'Data from IMGT/INN...'
${APP} inn
${APP} inn_seq

# identify INN sequences
${APP} inn_region &
P1=$!
${APP} inn_cdomain &
P2=$!
${APP} inn_vdomain &
P3=$!
${APP} inn_cdr &
P4=$!
wait $P1 $P2 $P3 $P4

#IMGT/GENE-DB
${APP} imgt_genelist &
P1=$!
${APP} imgt_gene &
P2=$!
${APP} imgt_geneseq &
P3=$!
wait $P1 $P2 $P3

# multiple alignment with IMGT germline
# parallel -j4 ${APP} imgt_msa ::: {0..237}

