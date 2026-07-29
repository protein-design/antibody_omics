#! /usr/bin/bash
APP="uv --direcotry=/home/yuan/bio/antibody_omics run abomics"

${APP} download_absd
${APP} absd

echo "Try to put data of database ABSD into database"
parallel -j8 ${APP} absd_record ::: {1..57}
parallel -j8 ${APP} absd_source ::: {1..57}

#parse seq_id in proseq_* tables
${APP} absd_proseq

