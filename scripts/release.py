'''
Script to generate a dataset release for hosting. It runs all available datasets with 'use_precomputed=False'. If a scratch location (--scratch) is passed (default), the raw dataset will be downloaded to the scratch and afterwards copied to the target folder (--path).

How to generate a new release:
1. run release.py
2. make a new release on GitHub, attach the .json.gz file of each dataset
3. tag it after date of download, like '12JUL2022'
4. change the default argument 'release' in proteinshake.datasets.dataset.Dataset to the new release tag

How to add a new dataset to the release pipeline:
1. import the dataset class
2. add it to the first loop
3. run release

'''

import os, shutil, argparse
from datetime import datetime
from proteinshake.datasets import PDBBindRefined, PDBBindPPI, TMScoreBenchmark, GODataset, ECDataset, PfamDataset, RCSBDataset
from proteinshake.utils import zip_file

RELEASE = datetime.now().strftime('%d%b%Y').upper()
assert not os.path.exists(os.path.expandvars(f'$SCRATCH/Datasets/proteinshake/{RELEASE}'))
os.makedirs(os.path.expandvars(f'$SCRATCH/Datasets/proteinshake/{RELEASE}/upload'), exist_ok=True)

parser = argparse.ArgumentParser(description='Script to generate all datasets for release.')
parser.add_argument('--path', type=str, help='Path to store the final dataset objects.', default='.')
parser.add_argument('--scratch', type=str, help='Path to scratch (if on cluster).', default=os.path.expandvars(f'$SCRATCH/Datasets/proteinshake/{RELEASE}'))
parser.add_argument('--njobs', type=int, help='Number of jobs.', default=20)
args = parser.parse_args()

PATH = args.path
SCRATCH = args.scratch if args.scratch != '' else args.path
n_jobs = args.njobs

'''
###################
# PDB Datasets
###################
os.makedirs(f'{PATH}/release', exist_ok=True)
for Dataset in [RCSBDataset, ECDataset, GODataset, PfamDataset, PDBBindRefined, PDBBindPPI, TMScoreBenchmark]:
    # name it after class name
    name = Dataset.__name__
    print()
    print(name)
    # create dataset
    ds = Dataset(root=f'{SCRATCH}/release/{name}', use_precomputed=False, n_jobs=n_jobs)
    print('Length:', len(ds.proteins))
    print('Compressing...')
    zip_file(f'{SCRATCH}/release/{name}/{name}.json')
    # delete to free memory
    del ds
    # copy from scratch to target
    if SCRATCH != PATH and not os.path.exists(f'{PATH}/release/{name}.json.gz'):
        print('Copying...')
        shutil.copyfile(f'{SCRATCH}/release/{name}/{name}.json.gz', f'{PATH}/release/{name}.json.gz')

# copy the extra file (pairwise distances) from the TM dataset
if SCRATCH != PATH and not os.path.exists(f'{PATH}/release/tmalign.json.gz'):
    print('Copying TM scores...')
    shutil.copyfile(f'{SCRATCH}/release/TMScoreBenchmark/tmalign.json.gz', f'{PATH}/release/tmalign.json.gz')
'''

###################
# AlphaFold Datasets
###################
from proteinshake.datasets.alphafold import AF_DATASET_NAMES
from proteinshake.datasets import AlphaFoldDataset

# create one dataset for each organism
for organism in AF_DATASET_NAMES.keys():
    print()
    print('AlphaFoldDataset', organism)
    ds = AlphaFoldDataset(root=f'{SCRATCH}/AlphaFoldDataset_{organism}', organism=organism, use_precomputed=False, n_jobs=n_jobs)
    print('Compressing...')
    zip_file(f'{SCRATCH}/AlphaFoldDataset_{organism}/AlphaFoldDataset.residue.avro')
    zip_file(f'{SCRATCH}/AlphaFoldDataset_{organism}/AlphaFoldDataset.atom.avro')
    del ds
    print('Copying...')
    shutil.copyfile(f'{SCRATCH}/AlphaFoldDataset_{organism}/AlphaFoldDataset.residue.avro.gz', f'{SCRATCH}/upload/AlphaFoldDataset_{organism}.residue.avro.gz')
    shutil.copyfile(f'{SCRATCH}/AlphaFoldDataset_{organism}/AlphaFoldDataset.atom.avro.gz', f'{SCRATCH}/upload/AlphaFoldDataset_{organism}.atom.avro.gz')
    #if SCRATCH != PATH and not os.path.exists(f'{PATH}/AlphaFoldDataset_{organism}.json.gz'):
    #    print('Copying...')
    #    shutil.copyfile(f'{SCRATCH}/AlphaFoldDataset_{organism}/AlphaFoldDataset.json.gz', f'{PATH}/AlphaFoldDataset_{organism}.json.gz')
