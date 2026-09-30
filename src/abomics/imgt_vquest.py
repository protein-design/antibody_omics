from Bio.Seq import Seq
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from pathlib import Path
import re
import requests

from .dir import Dir
from .process_data import ProcessData

class ImgtVquest(ProcessData):
    url = 'https://www.imgt.org'

    def __init__(self, data_dir:Path, verbose:bool=False):
        super().__init__(data_dir, verbose)

    '''
    download V-quest
    '''
    def download_vquest(self):
        info = {}
        endpoint = f"{self.url}/download/V-QUEST/IMGT_V-QUEST_reference_directory/"
        response = requests.get(endpoint)
        species = re.findall(r'<a.*>(.+)/</a>', response.text)
        for specie in species:
            info[specie] = {}
            specie_url = f"{endpoint}{specie}/"
            response = requests.get(specie_url)
            specie_types = re.findall(r'<a.*>(.+)/</a>', response.text)
            for specie_type in specie_types:
                info[specie][specie_type] = []
                specie_type_url = f"{specie_url}{specie_type}/"
                response = requests.get(specie_type_url)
                file_names = re.findall(r'<a.*>(.+\.fasta)</a>', response.text)
                outdir = self.data_dir / 'V-QUEST' / specie / specie_type
                self.init_dir(outdir)
                for file_name in file_names:
                    file_url = specie_type_url / file_name
                    outfile = outdir / file_name
                    if not outfile.is_file():
                        with open(outfile, 'w') as f:
                            response = requests.get(file_url)
                            f.write(response.text)
                    info[specie][specie_type].append(outfile)
        return info

    def pro_ref(self, outdir:Path, region:str):
        '''
        collect VDJ from V-quest and build *.fasta as references
        '''
        records = []
        outfile = outdir / f'IMGT_{region}.fasta'
        with open(outfile, 'w') as OUT:
            for path in Dir(self.data_dir).recursive_files():
                if path.is_file() and str(path).endswith(f'{region}.fasta'):
                    with open(path, 'r') as f:
                        parser = SeqIO.parse(f, 'fasta')
                        for rec in parser:
                            dna_seq = str(rec.seq)
                            dna_seq = re.sub('\.', '', dna_seq)
                            record = SeqRecord(
                                Seq(dna_seq).translate(),
                                id=rec.id,
                                description=rec.description
                            )
                            if record.id not in records:
                                records.append(record.id)
                                SeqIO.write(record, OUT, "fasta")
        print(f"region={region}, sequences={len(records)}, outfile={outfile}")
        return outfile