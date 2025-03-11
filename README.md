# DrugRefiner

## Description

Drug activity deconvolution using high-throughput screening, ultra-fast protemics, and machine learning. 

## Requirements

- Python 3.11.5 (download dependencies in local or virtual environment from 'requirements.txt') 

- R 4.3.1 (use renv package to restore dependencies from 'renv.lock')

## Downloads

1. Download data from figshare

2. Copy all contents into `DrugRefiner-ML/data/`.

## Running the Code

1. Navigate into `DrugRefiner-ML/scripts/`. 

   ```sh
   cd DrugRefiner-ML/allscripts

2. Execute the scripts in alphanumerical order. i.e.:

   ```sh
   Python3 fda_01_globalvarianceanalysis_250304a.py
   Rscript fda_02_limma_drug_250304a.R
   Python3 fda_03_de_pca_250304a.py
   ...

3. View regenerated files and outputs in `DrugRefiner-ML/data/` & `DrugRefiner-ML/figures/`