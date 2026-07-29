#!/usr/bin/bash
#download data from IMGT

IMGT="https://www.imgt.org/download"

RAWDATA_DIR="/home/yuan/omics/rawdata"
SOURCE="IMGT"


DB="3Dstructure-DB"
OUTDIR="${RAWDATA_DIR}/${SOURCE}/${DB}/"
mkdir -p ${OUTDIR}
files = (
    "${IMGT}/${DB}/IMGT3DNumComp.tgz"
    "${IMGT}/${DB}/IMGT3DFlatFiles.tgz"
    "${IMGT}/${DB}/pMHContactFiles.tgz"
)
for url in "${files[@]}"; do
    wget -c -qO- ${url} | gunzip | tar xvf - -C ${OUTDIR}/
done

DB="GENE-DB"
OUTDIR="${RAWDATA_DIR}/${SOURCE}/${DB}/"
mkdir -p ${OUTDIR}
files=(
    "${IMGT}/${DB}/IMGTGENEDB-GeneList"
    "${IMGT}/${DB}/IMGTGENEDB-ReferenceSequences.fasta-AA-WithGaps-F%2BORF%2BinframeP"
    "${IMGT}/${DB}/IMGTGENEDB-ReferenceSequences.fasta-AA-WithoutGaps-F%2BORF%2BinframeP"
    "${IMGT}/${DB}/IMGTGENEDB-ReferenceSequences.fasta-nt-WithGaps-F%2BORF%2BinframeP"
    "${IMGT}/${DB}/IMGTGENEDB-ReferenceSequences.fasta-nt-WithoutGaps-F%2BORF%2BallP"
    "${IMGT}/${DB}/IMGTGENEDB-ReferenceSequences.fasta-nt-WithoutGaps-F%2BORF%2BinframeP"
)
for URL in  "${files[@]}"; do
    wget -c $URL -P ${OUTDIR}/
done
