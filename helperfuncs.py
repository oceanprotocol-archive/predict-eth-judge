#these come from predict-eth/blob/main/challenges/main2.md, Nov 7, 2022

#imports
import datetime
from datetime import timezone
import numpy as np
from pathlib import Path
import os
import time

from brownie.network import accounts
import matplotlib
import matplotlib.pyplot as plt

from ocean_lib.example_config import get_config_dict
from ocean_lib.ocean.ocean import Ocean 
from ocean_lib.web3_internal.utils import connect_to_network

JUDGES_ADDRESS = "0xA54ABd42b11B7C97538CAD7C6A2820419ddF703E"

#helper functions: setup
def create_ocean_instance() -> Ocean:
    connect_to_network("polygon")
    config = get_config_dict("polygon")
    ocean = Ocean(config)
    return ocean

def create_alice_wallet(ocean: Ocean):
    alice_private_key = os.getenv('REMOTE_TEST_PRIVATE_KEY1')
    alice_wallet = accounts.add(alice_private_key)
    bal = accounts.at(alice_wallet.address).balance()
    print(f"alice_wallet.address={alice_wallet.address}. bal={bal/1e18} MATIC")
    assert alice_wallet.address == JUDGES_ADDRESS, \
        f"Wrong address. Need: {JUDGES_ADDRESS}"
    assert bal > 0, "Alice needs MATIC"
    return alice_wallet
    

#helper functions: time
def to_unixtime(dt: datetime.datetime):
    #must account for timezone, otherwise it's off
    ut = dt.replace(tzinfo=timezone.utc).timestamp()
    dt2 = datetime.datetime.utcfromtimestamp(ut) #to_datetime() approach
    assert dt2 == dt, f"dt: {dt}, dt2: {dt2}"
    return ut


def to_unixtimes(dts: list) -> list:
    return [to_unixtime(dt) for dt in dts]


def to_datetime(ut) -> datetime.datetime:
    dt = datetime.datetime.utcfromtimestamp(ut)
    ut2 = dt.replace(tzinfo=timezone.utc).timestamp() #to_unixtime() approach
    assert ut2 == ut, f"ut: {ut}, ut2: {ut2}"
    return dt


def to_datetimes(uts: list) -> list:
    return [to_datetime(ut) for ut in uts]


def round_to_nearest_hour(dt: datetime.datetime) -> datetime.datetime:
    return (dt.replace(second=0, microsecond=0, minute=0, hour=dt.hour)
            + datetime.timedelta(hours=dt.minute//30))


def pretty_time(dt: datetime.datetime) -> str:
    return dt.strftime('%Y/%m/%d, %H:%M:%S')


def print_datetime_info(descr:str, uts: list):
    dts = to_datetimes(uts)
    print(descr + ":")
    print(f"  starts on: {pretty_time(dts[0])}")
    print(f"    ends on: {pretty_time(dts[-1])}")
    print(f"  {len(dts)} datapoints")
    print(f"  time interval between datapoints: {(dts[1]-dts[0])}")


def target_12h_unixtimes(start_dt: datetime.datetime) -> list:
    target_dts = [start_dt + datetime.timedelta(hours=h) for h in range(12)]
    assert target_dts[0] == start_dt
    
    target_uts = to_unixtimes(target_dts)
    assert to_datetime(target_uts[0]) == start_dt
    
    return target_uts


#helper-functions: higher level
def load_from_ohlc_data(file_name: str) -> tuple:
    """Returns (list_of_unixtimes, list_of_close_prices)"""
    with open(file_name, "r") as file:
        data_str = file.read().rstrip().replace('"', '')
    x = eval(data_str) #list of lists
    uts = [xi[0]/1000 for xi in x]
    vals = [xi[4] for xi in x]
    return (uts, vals)


def filter_to_target_uts(target_uts:list, unfiltered_uts:list, unfiltered_vals:list) -> list:
    """Return filtered_vals -- values at at the target timestamps"""
    filtered_vals = [None] * len(target_uts)
    for i, target_ut in enumerate(target_uts):
        time_diffs = np.abs(np.asarray(unfiltered_uts) - target_ut)
        tol_s = 1 #should always align within e.g. 1 second
        target_ut_s = pretty_time(to_datetime(target_ut))
        assert min(time_diffs) <= tol_s, \
            f"Unfiltered times is missing target time: {target_ut_s}"
        j = np.argmin(time_diffs)
        filtered_vals[i] = unfiltered_vals[j]
    return filtered_vals


#helpers: save/load list
def save_list(list_: list, file_name: str):
    """Save a file shaped: [1.2, 3.4, 5.6, ..]"""
    p = Path(file_name)
    p.write_text(str(list_))


def load_list(file_name: str) -> list:
    """Load from a file shaped: [1.2, 3.4, 5.6, ..]"""
    p = Path(file_name)
    s = p.read_text()
    list_ = eval(s)
    return list_


#helpers: prediction performance
def calc_nmse(y, yhat) -> float:
    assert len(y) == len(yhat)
    y, yhat = np.asarray(y), np.asarray(yhat)
    range_y = max(y) - min(y)    
    nmse = np.sqrt(np.average(((yhat - y) / range_y) ** 2))
    return nmse


def plot_prices(cex_vals, pred_vals):
    matplotlib.rcParams.update({'font.size': 22})
    
    x = [h for h in range(0,12)]
    assert len(x) == len(cex_vals) == len(pred_vals)
    
    fig, ax = plt.subplots()
    ax.plot(x, cex_vals, '--', label="CEX values")
    ax.plot(x, pred_vals, '-', label="Pred. values")
    ax.legend(loc='lower right')
    plt.ylabel("ETH price")
    plt.xlabel("Hour")
    fig.set_size_inches(18, 18)
    plt.xticks(x)
    plt.show()

