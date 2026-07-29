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
    relative_fasta  VARCHAR(80),
    is_record       BOOLEAN,
    is_source       BOOLEAN,
    is_seq_map      BOOLEAN,
    UNIQUE(relative_fasta)
);

DROP TABLE IF EXISTS absd_record;
CREATE TABLE absd_record (
    absd_seq_id  INT AUTO_INCREMENT PRIMARY KEY,
    group_no     INT,
    record_name  VARCHAR(100),
    seq_len      INT GENERATED ALWAYS AS (LENGTH(seq)) STORED,
    seq          TEXT,
    CONSTRAINT fk_absd_record_group_no FOREIGN KEY (group_no)
        REFERENCES absd(group_no) ON DELETE CASCADE
);
CREATE INDEX index_absd_record ON absd_record(seq_len);

DROP TABLE IF EXISTS absd_source;
CREATE TABLE absd_source (
    group_no      INT,
    record_name   VARCHAR(100),
    seq_source    VARCHAR(200),
    dxref_id      VARCHAR(200),
    vgene_family  VARCHAR(20),
    source        VARCHAR(20),
    CONSTRAINT fk_absd_source_absd FOREIGN KEY (group_no)
        REFERENCES absd(group_no) ON DELETE CASCADE
);

DROP TABLE IF EXISTS absd_proseq;
CREATE TABLE absd_proseq(
    group_no      INT,
    absd_seq_id   INT,
    proseq_name   VARCHAR(20),
    seq_id        INT,
    CONSTRAINT fk_absdseq_record FOREIGN KEY (absd_seq_id)
        REFERENCES absd_record(absd_seq_id) ON DELETE CASCADE,
    CONSTRAINT fk_absdseq_absd FOREIGN KEY (group_no)
        REFERENCES absd(group_no) ON DELETE CASCADE
);
