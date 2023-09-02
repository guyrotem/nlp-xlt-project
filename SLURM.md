ssh {user}@c-002.cs.tau.ac.il
cd /home/joberant/NLP_2223/{user}/
bash	# init conda etc
pip install torch
pip install transformers[sentencepiece]
https://www.cs.tau.ac.il/system/slurm
sbatch example.slurm
squeue --user {user} # check for running jobs
sacct -u {user}		# show user's running jobs history

configure huggingface cache:

### python

import os
os.environ['TRANSFORMERS_CACHE'] = '/home/joberant/NLP_2223/{user}/.cache'

### bash

export TRANSFORMERS_CACHE=/home/joberant/NLP_2223/{user}/.cache
