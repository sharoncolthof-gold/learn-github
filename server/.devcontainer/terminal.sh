eval "$(/bin/micromamba shell hook -s bash)"
micromamba activate /opt/conda/
export PYTHONPATH="/workspace/server/src:$PYTHONPATH"
