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
    """
    Utility function to wait until the transaction is
    confirmed before proceeding.
    """
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print("Waiting for confirmation")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('confirmed-round')))
    return txinfo

#   Utility function used to print created asset for account and assetid
def print_created_asset(algodclient, account, assetid):    
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then use 'account_info['created-assets'][0] to get info on the created asset
    account_info = algodclient.account_info(account)
    idx = 0
    for my_account_info in account_info['created-assets']:
        scrutinized_asset = account_info['created-assets'][idx]
        idx = idx + 1       
        if (scrutinized_asset['index'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['index']))
            print(json.dumps(my_account_info['params'], indent=4))
            break


#   Utility function used to print asset holding for account and assetid
def print_asset_holding(algodclient, account, assetid):
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then loop thru the accounts returned and match the account you are looking for
    account_info = algodclient.account_info(account)
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1        
        if (scrutinized_asset['asset-id'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['asset-id']))
            print(json.dumps(scrutinized_asset, indent=4))
            break

print(f"Account 1 Address: {accounts[1]['pk']}")
print(f"Account 2 Address: {accounts[2]['pk']}")
print(f"Account 3 Address: {accounts[3]['pk']}")

########################
## Create Transaction ##
########################

# get the network parameters for transactions
params = algod_client.suggested_params()

# Asset creation transaction:
# Account 1 creates an asset called latinum and sets...
# Account 2 as the manager, reserve, freeze and clawback address.

account1_pk = accounts[1]['pk']
account2_pk = accounts[2]['pk']
asset_name = "latinum"

txn = AssetConfigTxn(
    sender= account1_pk,
    sp= params,
    total=1000,
    default_frozen=False,
    unit_name= asset_name.upper(),
    asset_name= asset_name,
    manager= account2_pk,
    reserve= account2_pk,
    freeze= account2_pk,
    clawback= account2_pk, 
    url= None,
    decimals=0)

##########################
## Sign the transaction ##
##########################

stxn = txn.sign(accounts[1]['sk']) # signing with the secret key

###########################################################################
## Send the create ASA transaction to the blockchain and print the TXNID ##
###########################################################################

# send the transaction to the network and retrieve the transaction id
txid = algod_client.send_transaction(stxn) 
print(f"Transaction ID: {txid}")

# Retrieve the asset ID of the newly created asset by:
# 1. ensuring that the creation transaction was confirmed, and;
# 2. then grabbing the asset id from the transaction.

# wait for the transaction to be confirmed
wait_for_confirmation(algod_client, txid)

try:
    # get asset id from transaction
    # get the new asset's information from the creator account
    ptx = algod_client.pending_transaction_info(txid)
    asset_id = ptx["asset-index"]
    print_created_asset(algod_client, account1_pk, asset_id)
    print_asset_holding(algod_client, account1_pk, asset_id)
except Exception as e:
    print(f"Exception: {e}")

