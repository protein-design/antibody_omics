#!/usr/bin/python
'''
requirements:
    - an empty database is created.
example: python src/pipelines/create_absd.py
functions:
    - build database known as complex2
    - build tables
'''
import os
import sys
src_dir = os.path.dirname(os.path.dirname(__file__))
if src_dir not in sys.path:
    sys.path.append(src_dir)

from bioomics import BuildComplex

'''
absd -> absd_record
     -> absd_source
     -> pro_seq -> absd_seq
'''


SQL_TEXT = """
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
//
DROP TABLE IF EXISTS absd_record;
CREATE TABLE absd_record (
    group_no     INT,
    absd_id      VARCHAR(100),
    record_id    TEXT,
    CONSTRAINT fk_absd_record_group_no FOREIGN KEY (group_no)
        REFERENCES absd(group_no)
);
//
DROP TABLE IF EXISTS absd_source;
CREATE TABLE absd_source (
    specie          VARCHAR(50),
    absd_id         VARCHAR(100),
    dxref_id        VARCHAR(200),
    vgene_family    VARCHAR(20),
    source          VARCHAR(20)
);
//
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
# //
# DROP TABLE IF EXISTS absd_align_imgt;
# CREATE TABLE absd_align_imgt(
#     seq_id        VARCHAR(20),
#     allele_name     VARCHAR(20),
#     gene_name       VARCHAR(20),
#     gene_family     VARCHAR(20),
#     chain_type      VARCHAR(10),
#     isotype         VARCHAR(10),
#     evalue          DOUBLE,
#     bit_score       INT,
#     CONSTRAINT pk_absd_imgt PRIMARY KEY (seq_id)
# );
# //
# DROP TABLE IF EXISTS absd_align_vregion;
# CREATE TABLE absd_align_vregion (
#     seq_id        VARCHAR(20),
#     region_name     VARCHAR(20),
#     identity        FLOAT,
#     start           INT,
#     end             INT,
#     seq             TEXT,
#     CONSTRAINT pk_absd_vregion PRIMARY KEY (seq_id, region_name)
# );
"""


  
class tmp:
    def insert_absd_align_imgt(self) -> tuple:
        table_name = 'absd_align_imgt'
        insert_query = f"""INSERT INTO {table_name}
            (seq_id, allele_name, gene_name, gene_family,
                chain_type, isotype, evalue, bit_score)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        func = getattr(self.recorder, table_name)
        self.insert(table_name, insert_query, func)

    def insert_absd_align_vregion(self) -> tuple:
        table_name = 'absd_align_vregion'
        insert_query = f"""INSERT INTO {table_name}
            (seq_id, region_name, identity, start, end, seq)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        func = getattr(self.recorder, table_name)
        self.insert(table_name, insert_query, func)


#####################################################################################

if __name__ == "__main__":
    bc = BuildComplex(verbose=True)
    for query in SQL_TEXT.split('//'): 
        res = bc.create_table(query)
        if res is None:
            print(f"ERROR. Check the above SQL: {query}\n\n")
