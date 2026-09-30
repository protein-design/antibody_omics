#! /usr/bin/bash
APP="uv --direcotry=/home/yuan/bio/antibody_omics run abomics"

# epitope virtual mapping
parallel -j8 ${APP} pdb_epi
parallel -j8 ${APP} uniprot_epi