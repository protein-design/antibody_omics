# antibody_omics

## introduction
Antibody sequences, labeling, numbering, etc.


## Development
### build UV environment

build new venv
```
cd ~/bio/antibody_omics
uv sync --group dev
```

install pyrosetta after uv sync
```
uv pip install pyrosetta --find-links https://west.rosettacommons.org/pyrosetta/quarterly/release
```

Rebuild venv if there is any updates in venv in the future
```
uv sync --group dev --inexact
```

test installation
```
uv run test-env
uv run test-pp
```

step into venv for development, then run piplines
```
source .venv/bin/activate
```

Usage: abomics <pipeline name> [...]
