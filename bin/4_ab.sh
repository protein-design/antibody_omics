#! /usr/bin/bash
APP=/home/yuan/bio/antibody_omics/app.py

echo "Sequence alignments: Blastp + IgBlastp"
parallel -j8 python ${APP} ab_vdj
parallel -j8 python ${APP} ab_vfrag ::: {0..360}
parallel -j8 python ${APP} ab_vregion ::: {0..360}
parallel -j8 python ${APP} ab_dregion ::: {0..360}
parallel -j8 python ${APP} ab_jregion ::: {0..360}
