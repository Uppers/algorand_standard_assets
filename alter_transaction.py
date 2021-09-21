from algosdk.v2client import algod
from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn, AssetFreezeTxn
import private_info as pi # this file is included in the gitignore file.

# Initialize an algod client 
algod_client = algod.AlgodClient(algod_token=pi.algod_token, algod_address=pi.algod_address)

# the current manager (Account 2) issues an asset configuration transaction that assigns Account 1 as the new manager.
# the account controlling the reserve, freeze and clawback parameters remain the same as before (Account 2)
params = algod_client.suggested_params()

# The Id. No. of the ASA created in create_asa.py  
ASSET_ID = 5

txn = AssetConfigTxn(
    sender = 
)