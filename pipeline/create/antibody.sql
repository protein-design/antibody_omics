/*
aacdb
abybank
sabdab -> sabdab_chain


view_proseq -> ab_vdj -> ab_vfrag
                      -> ab_vregion
                      -> ab_dregion
                      -> ab_jregion

*/


/* antibody database*/
DROP TABLE IF EXISTS aacdb;
CREATE TABLE aacdb (
    pdb_id          VARCHAR(10),
    antibody_chains VARCHAR(20),
    antigen_chains  VARCHAR(20),
    antibody        VARCHAR(100),
    protein	        VARCHAR(200),
    drug	        VARCHAR(500),
    targets	        VARCHAR(200),
    method          VARCHAR(50),
    organism        VARCHAR(200),
    resolution      FLOAT,
    reference       VARCHAR(500)
);

DROP TABLE IF EXISTS abybank;
CREATE TABLE abybank (
    pdb_id          VARCHAR(10),
    chain_type      VARCHAR(20),
    chain_numbering VARCHAR(20)
);

DROP TABLE IF EXISTS sabdab;
CREATE TABLE sabdab (
    pdb_id          VARCHAR(10) PRIMARY KEY,
    summary_file    VARCHAR(200)
);

DROP TABLE IF EXISTS sabdab_chain;
CREATE TABLE sabdab_chain (
    pdb_id          VARCHAR(100),
    model           INT,
    heavy_chain     VARCHAR(20),
    light_chain     VARCHAR(20),
    antigen_chain   VARCHAR(30),
    antigen_type    VARCHAR(50),
    resolution      FLOAT
);


/*  antibody numbering */
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

