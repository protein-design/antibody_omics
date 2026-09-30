import os
from pathlib import Path
import subprocess

class EpitopeMapping:
    
    def __init__(self, params:dict):
        self.params= params
       
    
    def predict(self, json_file:Path):
        project_dir = None
        if self.params['predictor'] == 'ANN':
            project_dir = self.params['epi_ann_dir']
        elif self.params['predictor'] == 'RNN':
            project_dir = self.params['epi_rnn_dir']
        elif self.params['predictor'] == 'ESM':
            project_dir = self.params['epi_esm_dir']

        cmd = [
            'uv', 'run', 
            '--project', str(project_dir),
            'python', 'app.py', str(json_file),
        ]
        print('Run predictor: ', ' '.join(cmd))
        try:
            result = subprocess.run(
                cmd,
                cwd=str(project_dir),
                check=True,
                text=True
            )
            return result.returncode
        except Exception as e:
            print(f"error={e}")
        return 1

