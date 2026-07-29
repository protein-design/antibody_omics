/*
absd -> absd_record
     -> absd_source
     -> pro_seq -> absd_seq

*/

DROP TABLE IF EXISTS absd;
CREATE TABLE absd (
    group_no        INT AUTO_INCREMENT PRIMARY KEY,
    release_date    DATE,
    specie          VARCHAR(50),
    faa_file        VARCHAR(100),
    is_record       BOOLEAN,
    is_source       BOOLEAN,
    is_pro_seq      BOOLEAN,
    is_seq_map      BOOLEAN
);

DROP TABLE IF EXISTS absd_record;
CREATE TABLE absd_record (
    group_no     INT,
    absd_id      VARCHAR(100),
    record_id    TEXT,
    CONSTRAINT fk_absd_record_group_no FOREIGN KEY (group_no)
        REFERENCES absd(group_no)
);

DROP TABLE IF EXISTS absd_source;
CREATE TABLE absd_source (
    specie          VARCHAR(50),
    absd_id         VARCHAR(100),
    dxref_id        VARCHAR(200),
    vgene_family    VARCHAR(20),
    source          VARCHAR(20)
);

DROP TABLE IF EXISTS absd_seq;
CREATE TABLE absd_seq(
    seq_id        INT,
    group_no      INT,
    absd_id       VARCHAR(100),
    UNIQUE(seq_id, group_no, absd_id),
    CONSTRAINT fk_absdseq_proseq FOREIGN KEY (seq_id)
        REFERENCES pro_seq(seq_id),
    CONSTRAINT fk_absdseq_absd FOREIGN KEY (group_no)
        REFERENCES absd(group_no)
);
