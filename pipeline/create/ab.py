#!/usr/bin/python
'''
requirements:
    - an empty database is created.
example: python src/pipelines/create/ab.py
functions:
    - build tables
'''
import os
import sys
src_dir = os.path.dirname(os.path.dirname(__file__))
if src_dir not in sys.path:
    sys.path.append(src_dir)

from bioomics import BuildComplex

'''
view_proseq -> ab_vdj -> ab_vfrag
                      -> ab_vregion
                      -> ab_dregion
                      -> ab_jregion
'''


SQL_TEXT = """
DROP TABLE IF EXISTS ab_vdj;
CREATE TABLE ab_vdj(
    proseq_name VARCHAR(10),
    seq_id      INT,
    query_faa   VARCHAR(60),
    v_aln       VARCHAR(60),
    d_aln       VARCHAR(60),
    j_aln       VARCHAR(60),
    UNIQUE(proseq_name, seq_id)
);
//
DROP TABLE IF EXISTS ab_vfrag;
CREATE TABLE ab_vfrag (
    query_id        VARCHAR(60),
    fragment        VARCHAR(20),
    identity        FLOAT,
    seq_from        INT,
    seq_to          INT,
    seq             TEXT,
    UNIQUE(query_id, fragment)
);
//
DROP TABLE IF EXISTS ab_vregion;
CREATE TABLE ab_vregion (
    query_id        VARCHAR(60),
    allele_name     VARCHAR(20),
    specie          VARCHAR(40),
    gene_name       VARCHAR(20),
    gene_family     VARCHAR(20),
    chain_type      VARCHAR(10),
    isotype         VARCHAR(10),
    evalue          DOUBLE,
    bit_score       INT,
    region_names    VARCHAR(100),
    UNIQUE(query_id)
);
//
DROP TABLE IF EXISTS ab_dregion;
CREATE TABLE ab_dregion (
    query_id        VARCHAR(60),
    query_len       INT,
    hit_id          VARCHAR(50),
    organism        VARCHAR(30),
    evalue          DOUBLE,
    bit_score       INT,
    match_seq       VARCHAR(50),
    identities      INT,
    align_len       INT,
    query_seq       VARCHAR(50),
    query_start     INT,
    query_end       INT,
    sbjct_seq       VARCHAR(50),
    sbjct_start     INT,
    sbjct_end       INT
);
//
DROP TABLE IF EXISTS ab_jregion;
CREATE TABLE ab_jregion (
    query_id        VARCHAR(60),
    query_len       INT,
    allele_name     VARCHAR(20),
    specie          VARCHAR(40),
    gene_name       VARCHAR(20),
    gene_family     VARCHAR(20),
    chain_type      VARCHAR(10),
    isotype         VARCHAR(10),
    evalue          DOUBLE,
    bit_score       INT,
    match_seq       VARCHAR(50),
    identities      INT,
    align_len       INT,
    query_seq       VARCHAR(50),
    query_start     INT,
    query_end       INT,
    sbjct_seq       VARCHAR(50),
    sbjct_start     INT,
    sbjct_end       INT
);
# //
# DROP TABLE IF EXISTS ab_anarci;
# CREATE TABLE ab_anarci (
#     chain_id            VARCHAR(20),
#     domain_no           INT,
#     hmm_species         VARCHAR(50),
#     chain_type          VARCHAR(5),
#     evalue              FLOAT,
#     score               FLOAT,
#     seqstart_index      INT,
#     seqend_index        INT,
#     identity_species    VARCHAR(50),
#     v_gene              VARCHAR(50),
#     v_identity          FLOAT,
#     j_gene              VARCHAR(50),
#     j_identity          FLOAT,
#     aligned_seq         TEXT
# );
"""

#####################################################################################

if __name__ == "__main__":
    bc = BuildComplex(verbose=True)
    for query in SQL_TEXT.split('//'): 
        res = bc.create_table(query)
        if res is None:
            print(f"ERROR. Check the above SQL: {query}\n\n")
