# predict-eth-judge

For predict-eth judges, a script to compute each submission's nmse

```text
Usage: pej getentries|getpreds|getnmses|..
```


# Installation

### Prerequisites

Ensure prerequisites:
- Linux/MacOS
- Python 3.8.5+

### Install pej

Then, open a new terminal and:

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
```


# Main Usage: CLI

`pej` is the main tool. In main terminal:
```console
#top-level help, lists all tools
pej

#see help for key functions
pej getentries
pej getpreds
...
```

Then, simply follow the usage directions:)
