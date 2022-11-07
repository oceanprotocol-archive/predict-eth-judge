# predict-eth-judge

For judges of the predict-eth competition, a script to compute each submission's nmse.


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

# Main Usage: CLI

`pej` is the main tool. In the terminal:
```console
#top-level help, lists all tools
pej

#see help for key functions
pej getentries
pej getpreds
pej getnmses
...
```

The order is getentries -> getpreds -> getnmses.

