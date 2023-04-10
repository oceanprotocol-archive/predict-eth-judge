# predict-eth-judge

For judges of the predict-eth competition, a script to compute each submission's nmse.

To use: first do installation, then follow the CLI steps.

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
pip install ocean-lib predict-eth ccxt enforce_typing numpy matplotlib

#add pwd to bash path
export PATH=$PATH:.

#set judges private key (needed for "getpreds")
export REMOTE_TEST_PRIVATE_KEY1=<judges key> 
```

# CLI

```text
Usage: pej getentries|getpreds|getnmses

  Follow these steps:
  1. pej getentries - from chain, output 1 entries.csv
  2. pej getpreds CSV_DIR - from 1 entries.csv, output N predvals_NFT_ADDRX.csv
  3. pej getnmses CSV_DIR - from N predvals*.csv, output 1 nmses.csv

Hard-coded values: NETWORK_NAME={NETWORK_NAME}, CHAINID={CHAINID}
Ennvar expected: REMOTE_TEST_PRIVATE_KEY1 (for judges' account)
```
