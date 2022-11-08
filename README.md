# predict-eth-judge

For judges of the predict-eth competition, a script to compute each submission's nmse.

# CLI

```text
Usage: pej getentries|getpreds|getnmses

  pej getentries ST FIN CSV_DIR - query chain, output 1 entries.csv
  pej getpreds CSV_DIR - from 1 entries.csv, output N predvals_DTADDRX.csv
  pej getnmses CSV_DIR - from N predvals_DTADDRX.csv, output 1 nmses.csv

  pej getdid DT_ADDR - from datatoken address, output did
```


# Installation

Open a new terminal and:

```console
#clone repo
git clone https://github.com/oceanprotocol/predict-eth-judge.git
cd predict-eth-judge

#create a virtual environment
python -m venv venv

#activate env
source venv/bin/activate

#install dependencies
pip install wheel
pip install -r requirements.txt

#add pwd to bash path
export PATH=$PATH:.

#set judges private key (needed for "getpreds")
export JUDGES_KEY=<judges key> 
```
