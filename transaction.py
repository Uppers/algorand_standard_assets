from utility import Utility
from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn, AssetFreezeTxn

utility = Utility()

ASSET_ID = 5

# transfer asset of 10 from account 1 to account 3
params = utility.algod_client.suggested_params()

sender_account = 1
recipient_account = 3

# account public keys
sender_pk = utility.account_credentials[sender_account]['pk']
recipient_pk = utility.account_credentials[recipient_account]['pk']

# set up the transaction
txn = AssetTransferTxn(
    sender = sender_pk,
    sp=params,
    receiver= recipient_pk,
    amt = 10, 
    index = ASSET_ID
)

# sender account secret key
sender_sk = utility.account_credentials[sender_account]['sk']

# sign the transfer transaction 
stxn = txn.sign(sender_sk)

# send the transaction 
txid = utility.algod_client.send_transaction(stxn)
print(txid)

# wait for the transaction to be confirmed
utility.wait_for_confirmation(txid)

# the balance should have increased by 10
utility.print_asset_holding(recipient_pk, ASSET_ID)
