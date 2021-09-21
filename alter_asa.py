from algosdk.future.transaction import AssetConfigTxn
from utility import Utility

utility = Utility()


# the current manager (Account 2) issues an asset configuration transaction that assigns Account 1 as the new manager.
# the account controlling the reserve, freeze and clawback parameters remain the same as before (Account 2)
params = utility.algod_client.suggested_params()

# The Id. No. of the ASA created in create_asa.py  
ASSET_ID = 5

# get account public keys 
account1_pk = utility.account_credentials[1]['pk']
account2_pk = utility.account_credentials[2]['pk']

# configure the transaction. notice that the "manager" parameter has been changed from account 2 to account 1.
txn = AssetConfigTxn(
    sender = account2_pk,
    sp = params,
    index= ASSET_ID,
    manager= account1_pk,
    reserve= account2_pk,
    freeze= account2_pk,
    clawback= account2_pk,
)
# transaction sender's secret key
account2_sk = utility.account_credentials[2]['sk']

# sign the transaction 
stxn = txn.sign(account2_sk)

# send the transaction
txid = utility.algod_client.send_transaction(stxn)
print(f"Transaction Id: {txid}")

# wait for the transaction to be confirmed 
utility.wait_for_confirmation(txid)

# print asset information to make sure manager is now account 1
utility.print_created_asset(account1_pk, ASSET_ID)

