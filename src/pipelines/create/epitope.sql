

DROP TABLE IF EXISTS pdb_epi;
CREATE TABLE pdb_epi(
    chain_id        VARCHAR(20) NOT NULL,
    predictor       VARCHAR(20) NOT NULL,
    relative_outdir VARCHAR(100) NOT NULL,
    UNIQUE(chain_id, predictor)
);

DROP TABLE IF EXISTS uniprot_epi;
CREATE TABLE uniprot_epi(
    uniprot_acc     VARCHAR(20) NOT NULL,
    predictor       VARCHAR(20) NOT NULL,
    relative_outdir VARCHAR(100) NOT NULL,
    UNIQUE(uniprot_acc, predictor)
);