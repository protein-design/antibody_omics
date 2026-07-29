//
DROP TABLE IF EXISTS absd_align_imgt;
CREATE TABLE absd_align_imgt(
    seq_id        VARCHAR(20),
    allele_name     VARCHAR(20),
    gene_name       VARCHAR(20),
    gene_family     VARCHAR(20),
    chain_type      VARCHAR(10),
    isotype         VARCHAR(10),
    evalue          DOUBLE,
    bit_score       INT,
    CONSTRAINT pk_absd_imgt PRIMARY KEY (seq_id)
);
//
DROP TABLE IF EXISTS absd_align_vregion;
CREATE TABLE absd_align_vregion (
    seq_id        VARCHAR(20),
    region_name     VARCHAR(20),
    identity        FLOAT,
    start           INT,
    end             INT,
    seq             TEXT,
    CONSTRAINT pk_absd_vregion PRIMARY KEY (seq_id, region_name)
);
//
DROP TABLE IF EXISTS ab_anarci;
CREATE TABLE ab_anarci (
    chain_id            VARCHAR(20),
    domain_no           INT,
    hmm_species         VARCHAR(50),
    chain_type          VARCHAR(5),
    evalue              FLOAT,
    score               FLOAT,
    seqstart_index      INT,
    seqend_index        INT,
    identity_species    VARCHAR(50),
    v_gene              VARCHAR(50),
    v_identity          FLOAT,
    j_gene              VARCHAR(50),
    j_identity          FLOAT,
    aligned_seq         TEXT
);
//
DROP TABLE IF EXISTS msa_vregion;
CREATE TABLE msa_vregion (
    chain_id        VARCHAR(20),
    chain_types     VARCHAR(20),
    query_fa        VARCHAR(100),
    aln_file        VARCHAR(100),
    pickle_file     VARCHAR(100),
    UNIQUE (chain_id, chain_types)
);