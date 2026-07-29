'''
install blast: sudo apt install ncbi-blast+
'''
from pathlib import Path
import sys
import subprocess


class ProcessIgblast:

    def __init__(self, bin_dir:Path, outdir:Path=None, verbose:bool=False):
        # igblast bin
        self.bin_dir = bin_dir
        if self.bin_dir not in sys.path:
            sys.path.append(str(self.bin_dir))
        # outdir
        self.outdir = outdir
        outdir.mkdir(parents=True, exist_ok=True)
        # print information
        self.verbose = verbose

    def build_prot_db(self, fa_file:Path, bin_dir:Path=None):
        exe = 'makeblastdb' if bin_dir is None else bin_dir / 'makeblastdb'
        outdir = self.outdir if self.outdir else fa_file.parent
        outprefix = str(outdir  / fa_file.stem)
        cmd = [exe, '-parse_seqids', '-dbtype', 'prot', '-in', str(fa_file), '-out', outprefix,]
        try:
            if self.verbose:
                print('build igblastp database: ', ' '.join(cmd))
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            if self.verbose:
                print("Command output:", result.stdout.strip())
            return outprefix
        except subprocess.CalledProcessError as e:
            if self.verbose:
                print(f"Command failed with error: {e}")
                print(f"Stderr: {e.stderr}")
        return None

    def igblastp(self, fa_file:Path, db_path:str, outfile:Path, outfmt:int=None):
        '''
        -outfmt <String> alignment view options:
            3 = Flat query-anchored, show identities,
            4 = Flat query-anchored, no identities,
            7 = Tabular with comment lines
            19 = Rearrangement summary report (AIRR format)
        '''
        outfmt = 5 if outfmt is None else outfmt
        cmd = [
            str(self.bin_dir / 'igblastp'),
            '-query', str(fa_file),
            '-outfmt', str(outfmt),
            '-out', str(outfile),
            '-germline_db_V', db_path,
        ]
        try:
            if self.verbose:
                print('\n##igblastp: ', ' '.join(cmd))
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            if self.verbose:
                print("Command output:", result.stdout.strip())
            return 'succeed'
        except subprocess.CalledProcessError as e:
            if self.verbose:
                print(f"Command failed with error: {e}")
                print(f"Stderr: {e.stderr}")
        return 'fail'