#! /usr/bin/bash
APP="uv --direcotry=/home/yuan/bio/antibody_omics run abomics"

echo "Sequence alignments: Blastp + IgBlastp"
parallel -j8 ${APP} ab_vdj
parallel -j8 ${APP} ab_vfrag ::: {0..360}
parallel -j8 ${APP} ab_vregion ::: {0..360}
parallel -j8 ${APP} ab_dregion ::: {0..360}
parallel -j8 ${APP} ab_jregion ::: {0..360}
