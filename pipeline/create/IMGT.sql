/*
inn -> inn_seq
    -> inn_region
    -> inn_cdomain
    -> inn_vdomain
    -> inn_cdr
    -> inn_gene -> inn_genelist
                -> inn_gene_seq

view_inn_pdb

*/

DROP TABLE IF EXISTS inn;
CREATE TABLE inn (
    inn_number              VARCHAR(50),
    cas_number              VARCHAR(100),
    common_name             VARCHAR(100),
    inn_name                VARCHAR(100),
    proposed_list           VARCHAR(50),
    recommended_list        VARCHAR(50),
    receptor_type	        VARCHAR(50),
    receptor_description    VARCHAR(100),
    species    	            VARCHAR(50),
    molecular_formula       VARCHAR(50),
    glycosylation_sites     VARCHAR(200),
    inn_file                VARCHAR(100),
    CONSTRAINT pk_inn PRIMARY KEY (inn_number)
);
//
DROP TABLE IF EXISTS inn_seq;
CREATE TABLE inn_seq (
    inn_number      VARCHAR(50),
    inn_chain_id    VARCHAR(50) PRIMARY KEY,
    description     VARCHAR(200),
    seq_len         INT GENERATED ALWAYS AS (LENGTH(seq)) STORED,
    seq             TEXT,
    seq_id          INT,
    CONSTRAINT fk_innseq_inn FOREIGN KEY (inn_number)
        REFERENCES inn(inn_number) ON DELETE CASCADE
);
//
DROP TABLE IF EXISTS inn_region;
CREATE TABLE inn_region (
    chain_id        VARCHAR(50),
    region_name     VARCHAR(50),
    region_type     VARCHAR(50),
    start           INT,
    end             INT,
    seq             TEXT
);
//
DROP TABLE IF EXISTS inn_cdomain;
CREATE TABLE inn_cdomain (
    chain_id        VARCHAR(50),
    domain_name     VARCHAR(50),
    gene_allele     TEXT,
    seq             TEXT,
    seq_align       TEXT
);
//
DROP TABLE IF EXISTS inn_vdomain;
CREATE TABLE inn_vdomain (
    chain_id            VARCHAR(50),
    domain_name         VARCHAR(50),
    cdr_length          VARCHAR(50),
    fr_length           VARCHAR(50),
    gene_allele         TEXT,
    seq                 TEXT,
    seq_cdr             TEXT,
    seq_align           TEXT,
    seq_align_cdr       TEXT,
    seq_cdr_mask        TEXT,
    seq_align_cdr_mask  TEXT
);
//
DROP TABLE IF EXISTS inn_cdr;
CREATE TABLE inn_cdr (
    chain_id        VARCHAR(50),
    cdr_type        VARCHAR(50),
    seq             VARCHAR(200),
    seq_align       VARCHAR(200),
    align_start     INT,
    align_end       INT,
    align_length    INT
);
//
DROP TABLE IF EXISTS imgt_genelist;
CREATE TABLE imgt_genelist (
    species             VARCHAR(50),
    gene_db             VARCHAR(20),
    gene_function       VARCHAR(20),
    gene_definition     VARCHAR(200),
    number_alleles      VARCHAR(5),
    chromosome          VARCHAR(5),
    chromosomal_loc     VARCHAR(20),
    ligm_db_ref_gene    VARCHAR(100),
    ncbi_gene           VARCHAR(20),
    chain               VARCHAR(10),
    domain              VARCHAR(5)
);
//
DROP TABLE IF EXISTS imgt_gene;
CREATE TABLE imgt_gene (
    record_id       VARCHAR(100),
    specie          VARCHAR(100),
    isotype         VARCHAR(10),
    chain_type      VARCHAR(10),
    gene_name       VARCHAR(20),
    allele_name     VARCHAR(20),
    region_name     VARCHAR(50)
);
//
DROP TABLE IF EXISTS imgt_geneseq;
CREATE TABLE imgt_geneseq (
    record_id       VARCHAR(100),
    seq_type        VARCHAR(100),
    seq             TEXT
);

DROP VIEW IF EXISTS view_inn_pdb;
CREATE VIEW view_inn_pdb AS 
    SELECT B.inn_chain_id, B.pdb_chain_id, P.pdb_id,
        I.inn_number, A.common_name, A.inn_name,
        A.receptor_type, A.receptor_description, I.chain_seq
    FROM inn_blastp     B
    LEFT JOIN pdb_chainid    P ON B.pdb_chain_id = P.chain_id
    LEFT JOIN inn_chain I ON B.inn_chain_id = I.chain_id
    LEFT JOIN inn       A ON I.inn_number = A.inn_number
    WHERE B.identity = 1
;
