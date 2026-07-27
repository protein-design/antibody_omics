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
'''


SQL_TEXT = """

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
