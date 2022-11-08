# adapted from df-py/util/oceanutil.py as of Nov 7, 2022

import hashlib

from enforce_typing import enforce_types

@enforce_types
def calcDID(nft_addr: str, chainID: int) -> str:
    # adapted from ocean.py/ocean_lib/ocean/ocean_assets.py
    did = f"did:op:{create_checksum(nft_addr + str(chainID))}"
    return did

# from ocean.py/ocean_lib/utils/utilities.py
@enforce_types
def create_checksum(text: str) -> str:
    """
    :return: str
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
