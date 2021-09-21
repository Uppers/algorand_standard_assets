import json
from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn, AssetFreezeTxn
import private_info as pi # this file is included in the gitignore file.

###########
## SETUP ##
###########


# For ease of reference, add account public and private keys to an accounts dict.
accounts = {}
counter = 1
for m in [pi.account1_mnemonic, pi.account2_mnemonic, pi.account3_mnemonic]:
    accounts[counter] = {}
    accounts[counter]['pk'] = mnemonic.to_public_key(m)
    accounts[counter]['sk'] = mnemonic.to_private_key(m)
    counter += 1

# Initialize an algod client 
algod_client = algod.AlgodClient(algod_token=pi.algod_token, algod_address=pi.algod_address)

######################################################
## Print Accounts, Utility Functions and Structures ##
######################################################

def wait_for_confirmation(client, txid):
    """ Utillity function to wait until the transaction is confirmed before proceeding """
    last_round = client.status().get("last-round")
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get("confirmed-round") and txinfo.get("confirmed-round")>0):
        print("Waiting for confirmation")
        last_round +=1 
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    confirmed_round = txinfo.get("confirmed-round")
    print(f"Transaction {txid} confirmed in round {confirmed_round}.")
    return txinfo

def print_created_asset(algod_client, account, asset_id):
    """ 
    Prints the created asset for the given account and asset id
    Note: Easier to use an indexer.
    """
    account_info = algod_client.account_info(account)
    idx = 0 
    for my_account_info in account_info["created-assets"]:
        scrutinized_asset = account_info["created-assets"][idx]
        idx = idx + 1
        if (scrutinized_asset["asset-id"]== asset_id):
            id = scrutinized_asset["asset-id"]
            print(f"Asset ID: {id}")
            print(json.dumps(scrutinized_asset, indent=4))
            break

def print_asset_holding(algod_client, account, asset_id):
    """ Prints the amount the account is holding of the asset """
    account_info = algod_client.account_info(account)
    idx = 0
    for my_account_info in account_info["assets"]:
        scrutinised_asset = account_info["assets"][idx]
        idx += 1
        if scrutinised_asset["asset-id"] == asset_id:
            id = scrutinised_asset["asset-id"]
            print(f"Asset ID: {id}")
            print(json.dumps(scrutinised_asset, indent=4))
            break

print(f"Account 1 Address: {accounts[1]['pk']}")
print(f"Account 1 Address: {accounts[2]['pk']}")
print(f"Account 1 Address: {accounts[3]['pk']}")



