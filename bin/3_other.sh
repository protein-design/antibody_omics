#! /usr/bin/bash

APP=/home/yuan/bio/antibody_omics/app.py

echo "Try to download data from database AACDB"
python ${APP} aacdb

echo "Try to download data from database SAbDab"
python ${APP} sabdab
python ${APP} sabdab_chain

echo "Try to download data from database abYbank"
python ${APP} abybank
