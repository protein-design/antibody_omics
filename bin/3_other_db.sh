#! /usr/bin/bash
APP="uv --direcotry=/home/yuan/bio/antibody_omics run abomics"

echo "Try to download data from database AACDB"
${APP} aacdb

echo "Try to download data from database SAbDab"
${APP} sabdab
${APP} sabdab_chain

echo "Try to download data from database abYbank"
${APP} abybank
