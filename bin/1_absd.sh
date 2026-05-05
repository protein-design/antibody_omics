#! /usr/bin/bash
APP=/home/yuan/bio/antibody_omics/app.py


echo "Try to put data of database ABSD into database"
python ${APP} absd
python ${APP} absd_record
python ${APP} absd_source
python ${APP} absd_pro_seq
python ${APP} absd_seq
