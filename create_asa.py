from algosdk.future.transaction import AssetConfigTxn
from utility import Utility

###########
## SETUP ##
###########

utility = Utility()

########################
## Create Transaction ##
########################

# get the network parameters for transactions
params = utility.algod_client.suggested_params()

# Asset creation transaction:
# Account 1 creates an asset called latinum and sets...
# Account 2 as the manager, reserve, freeze and clawback address.

account1_pk = utility.account_credentials[1]['pk']
account2_pk = utility.account_credentials[2]['pk']
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

stxn = txn.sign(utility.account_credentials[1]['sk']) # signing with the secret key

###########################################################################
## Send the create ASA transaction to the blockchain and print the TXNID ##
###########################################################################

# send the transaction to the network and retrieve the transaction id
txid = utility.algod_client.send_transaction(stxn) 
print(f"Transaction ID: {txid}")

# Retrieve the asset ID of the newly created asset by:
# 1. ensuring that the creation transaction was confirmed, and;
# 2. then grabbing the asset id from the transaction.

# wait for the transaction to be confirmed
utility.wait_for_confirmation(txid)

try:
    # get asset id from transaction
    # get the new asset's information from the creator account
    ptx = utility.algod_client.pending_transaction_info(txid)
    asset_id = ptx["asset-index"]
    utility.print_created_asset(account1_pk, asset_id)
    utility.print_asset_holding(account1_pk, asset_id)
except Exception as e:
    print(f"Exception: {e}")

