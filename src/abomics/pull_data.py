from pathlib import Path

from .parse_imgt_annot import ParseImgtAnnot

class PullData:
    def __init__(self, data_dir:Path, meta):
        self.data_dir = data_dir
        self.meta = meta
    
    def flat_inn(self):
        indir = self.data_dir / '3Dstructure-DB' / 'IMGT3DFlatFiles'
        files = [f for f in indir.iterdir() if f.is_file()]
        for gz_file in files:
            if str(gz_file).endswith('.inn.gz'):
                try:
                    inn_data = ParseImgtAnnot(gz_file)()
                    self.meta['inn_data'] += 1
                    yield inn_data
                except Exception as e:
                    print(f"{gz_file}, error={e}")
                    self.meta['invalid_inn'] += 1


