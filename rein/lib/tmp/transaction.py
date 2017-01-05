from bitcoin import SelectParams
from bitcoin.core import b2x, lx, COIN, COutPoint, CMutableTxOut, CMutableTxIn, CMutableTransaction, Hash160, x
from bitcoin.core.script import CScript, OP_DUP, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG, SignatureHash, SIGHASH_ALL, OP_2, OP_3, OP_CHECKMULTISIG, OP_0
from bitcoin.core.scripteval import VerifyScript, SCRIPT_VERIFY_P2SH
from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret, P2PKHBitcoinAddress
import urllib2, urllib
import json
from hashlib import sha256
api = "blocktrail" #handle this
from rein.lib.bucket import Bucket
from rein.lib.io import safe_get
import click
SelectParams("testnet")

def unspent_txins(address,testnet):
    if (api == "blockr"):
        if testnet:
            url = "https://tbtc.blockr.io/api/v1/address/unspent/"+str(address)
        else:
            url = "https://btc.blockr.io/api/v1/address/unspent/"+str(address)
        hdr = {'User-Agent': 'Mozilla/5.0'}
        request = urllib2.Request(url,headers=hdr)
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        total_value = 0;
        txins = [];
        for tx in json_object['data']['unspent']:
            txid = tx['tx'];
            vout = tx['n'];
            value = float(tx['amount']);
            total_value += value;
            txins.append((txid, vout))
    else:
        if testnet:
            url = "https://api.blocktrail.com/v1/tbtc/address/"+str(address)+"/unspent-outputs?api_key=1e1ebd7ae629e031310ae9d61fe8549c82d0c589"
        else:
            url = "https://api.blocktrail.com/v1/btc/address/"+str(address)+"/unspent-outputs?api_key=1e1ebd7ae629e031310ae9d61fe8549c82d0c589"
        hdr = {'User-Agent': 'Mozilla/5.0'}
        request = urllib2.Request(url,headers=hdr)
        print("open url "+url)
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        total_value = 0;
        txins = [];
        for tx in json_object['data']:
            txid = tx['hash'];
            vout = tx['index'];
            value = tx['value']/100000000.;
            total_value += value;
            txins.append((txid, vout))
            
    return (txins,total_value)

def broadcast_tx (tx_hex,rein):

    urls = Bucket.get_urls(rein)
    sel_url = "{0}bitcoin?owner={1}&query=sendrawtransaction&tx={2}&testnet={3}"
    
    for url in urls:
        data = safe_get(rein.log, sel_url.format(url,rein.user.maddr,tx_hex,rein.testnet))
        if data and 'txid' in data:
            return data['txid']
    
def partial_spend_p2sh (redeemScript,rein,daddr=None,alt_amount=None,alt_daddr=None):
    if daddr is None:
        daddr = rein.user.daddr
    txin_redeemScript = CScript(x(redeemScript))
    txin_scriptPubKey = txin_redeemScript.to_p2sh_scriptPubKey()
    txin_p2sh_address = CBitcoinAddress.from_scriptPubKey(txin_scriptPubKey)
    (txins,total_value) = unspent_txins(txin_p2sh_address,rein.testnet)
    if len(txins)==0:
        raise ValueError('No unspent txins found')
    txins_str = ""
    txins_obj = []
    for txid,vout in txins:
        txins_str += " "+txid+"-"+str(vout)
        txins_obj.append(CMutableTxIn(COutPoint(lx(txid),vout)))                
    fee = 0.0005
    amount = total_value-fee
    if alt_amount is not None:
        amount = amount-alt_amount
    if amount<=0. or alt_amount>total_value-fee:
        click.echo("amount: "+str(amount)+" alt_amount: "+str(alt_amount)+" total_value: "+str(total_value))
        raise ValueError('Not enough value in the inputs')
    txouts = []
    txout = CMutableTxOut(amount*COIN, CBitcoinAddress(daddr).to_scriptPubKey())
    txouts.append(txout)
    if alt_amount is not None:
        txout_alt = CMutableTxOut(alt_amount*COIN, CBitcoinAddress(alt_daddr).to_scriptPubKey())
        txouts.append(txout_alt)
    tx = CMutableTransaction(txins_obj, txouts)
    ntxins = len(txins_obj)
    seckey = CBitcoinSecret(rein.user.dkey)
    sig = "";
    for i in range(0,ntxins):
        sighash = SignatureHash(txin_redeemScript, tx, i, SIGHASH_ALL)
        sig += " "+b2x(seckey.sign(sighash))+"01"
    if alt_amount is not None:
        return (txins_str[1:],str(amount),daddr,str(alt_amount),alt_daddr,sig[1:])
    return (txins_str[1:],str(amount),daddr,sig[1:])

def partial_spend_p2sh_mediator (redeemScript,rein,mediator_address,mediator_sig=False):
    txin_redeemScript = CScript(x(redeemScript))
    txin_scriptPubKey = txin_redeemScript.to_p2sh_scriptPubKey()
    txin_p2sh_address = CBitcoinAddress.from_scriptPubKey(txin_scriptPubKey)
    (txins,total_value) = unspent_txins(txin_p2sh_address,rein.testnet)
    if len(txins)==0:
        raise ValueError('No unspent txins found')
    txins_str = ""
    txins_obj = []
    for txid,vout in txins:
        txins_str += " "+txid+"-"+str(vout)
        txins_obj.append(CMutableTxIn(COutPoint(lx(txid),vout)))
    fee = 0.0005
    amount = total_value-fee
    if amount<=0:
        raise ValueError('Not enough value in the inputs')
    if mediator_sig:
        txout = CMutableTxOut(amount*COIN,CBitcoinAddress(mediator_address).to_scriptPubKey())
        tx = CMutableTransaction(txins_obj,[txout])
        seckey = CBitcoinSecret(rein.user.dkey)
        ntxins = len(txins_obj)
        sig = ""
        for i in range(0,ntxins):
            sighash = SignatureHash(txin_redeemScript,tx,i,SIGHASH_ALL)
            sig += " "+b2x(seckey.sign(sighash)+x("01"))
        return (txins_str[1:],str(amount),str(mediator_address),sig[1:])
    return (txins_str[1:],str(amount),str(mediator_address))

def partial_spend_p2sh_mediator_2 (redeemScript,txins_str,amount,daddr,rein):
    txin_redeemScript = CScript(x(redeemScript))
    txin_scriptPubKey = txin_redeemScript.to_p2sh_scriptPubKey()
    txins_obj = []
    for txin_str in txins_str.split():
        txin_list = txin_str.split("-")
        txins_obj.append(CMutableTxIn(COutPoint(lx(txin_list[0]),int(txin_list[1]))))
    txout = CMutableTxOut(amount*COIN,CBitcoinAddress(daddr).to_scriptPubKey())
    tx = CMutableTransaction(txins_obj,[txout])
    seckey = CBitcoinSecret(rein.user.dkey)
    ntxins = len(txins_obj)
    sig = ""
    for i in range(0,ntxins):
        sighash = SignatureHash(txin_redeemScript,tx,i,SIGHASH_ALL)
        sig += " "+b2x(seckey.sign(sighash)+x("01"))
    return sig[1:]

def spend_p2sh (redeemScript,txins_str,amounts,daddrs,sig,rein):
    txin_redeemScript = CScript(x(redeemScript))
    txin_scriptPubKey = txin_redeemScript.to_p2sh_scriptPubKey()
    txins_obj = []
    for txin_str in txins_str.split():
        txin_list = txin_str.split("-")
        txins_obj.append(CMutableTxIn(COutPoint(lx(txin_list[0]),int(txin_list[1]))))
    txouts = []
    len_amounts = len(amounts)
    for i in range(0,len_amounts):
        txouts.append(CMutableTxOut(amounts[i]*COIN,CBitcoinAddress(daddrs[i]).to_scriptPubKey()))
    tx = CMutableTransaction(txins_obj,txouts)
    seckey = CBitcoinSecret(rein.user.dkey)
    ntxins = len(txins_obj)
    sig_list = []
    for s in sig.split():
        sig_list.append(x(s))
    sig2_str = ""
    for i in range(0,ntxins):
        sighash = SignatureHash(txin_redeemScript,tx,i,SIGHASH_ALL)
        sig2 = seckey.sign(sighash)+x("01")
        sig2_str += " "+b2x(sig2)
        txins_obj[i].scriptSig = CScript([OP_0, sig2, sig_list[i], txin_redeemScript])
        VerifyScript(txins_obj[i].scriptSig, txin_scriptPubKey, tx, i, (SCRIPT_VERIFY_P2SH,))
    tx_bytes = tx.serialize()
    hash = sha256(sha256(tx_bytes).digest()).digest()
    txid = b2x(hash[::-1])
    #txid_causeway = broadcast_tx(b2x(tx_bytes),rein)
    return (txid,sig2_str[1:])

def spend_p2sh_mediator (redeemScript,txins_str,amounts,daddrs,sig,rein):
    txin_redeemScript = CScript(x(redeemScript))
    txin_scriptPubKey = txin_redeemScript.to_p2sh_scriptPubKey()
    txins_obj = []
    for txin_str in txins_str.split():
        txin_list = txin_str.split("-")
        txins_obj.append(CMutableTxIn(COutPoint(lx(txin_list[0]),int(txin_list[1]))))
    txouts = []
    len_amounts = len(amounts)
    for i in range(0,len_amounts):
        txouts.append(CMutableTxOut(amounts[i]*COIN,CBitcoinAddress(daddrs[i]).to_scriptPubKey()))
    tx = CMutableTransaction(txins_obj,txouts)
    seckey = CBitcoinSecret(rein.user.dkey)
    ntxins = len(txins_obj)
    sig_list = []
    for s in sig.split():
        sig_list.append(x(s))
    sig2_str = ""
    for i in range(0,ntxins):
        sighash = SignatureHash(txin_redeemScript,tx,i,SIGHASH_ALL)
        sig2 = seckey.sign(sighash)+x("01")
        sig2_str += " "+b2x(sig2)
        txins_obj[i].scriptSig = CScript([OP_0, sig_list[i], sig2, txin_redeemScript])
        VerifyScript(txins_obj[i].scriptSig, txin_scriptPubKey, tx, i, (SCRIPT_VERIFY_P2SH,))
    tx_bytes = tx.serialize()
    hash = sha256(sha256(tx_bytes).digest()).digest()
    txid = b2x(hash[::-1])
    txid_causeway = broadcast_tx(b2x(tx_bytes),rein)
    return (txid,sig2_str[1:])

redeemScript = "522103220d8573c2d9bdea5d60d3ad8a892c94da4a1850445fe3b83b17307a8d655fb1210342b976a71a5aa2daa65512da45f1d44579c1d3fc364d085e398fc771c23fe2622102ba974cf1e3853814e0e05e7e36266e3d5d324eb48a31694d4969bed390535a6053ae"

class Config():
        def __init__(self):
            self.user = {}
            self.testnet = True
            self.daddr = ""
            self.dkey = ""

mediator = Config()
mediator.daddr = "mzwCJVcQZampofzP8eYDgfNYDauggC5TSy"
mediator.dkey = "cUsMq5ziSVvSFWKG1rwbu7YDZdKjpCzzE9jJabmeUQ6XjUGDxQQg"
client = Config()
client.daddr = "mzcrNKvmKJZKhzy1kV9uht9uJfJBQaPJMF"
client.dkey = "cUtVwDQqPn75KjnF5Qa3kyVUQmE4gprami3QW1QughTACnkHQHpa"
reinmediator = Config()
reinmediator.user = mediator
reinclient = Config()
reinclient.user = client

daddr = "mgomM45aKPNbjNgq9bs8CnZnMyzNdrv6EB"
alt_amount = 0.0081
alt_daddr = "mzcrNKvmKJZKhzy1kV9uht9uJfJBQaPJMF"

(txins_str,amount_str,daddr,alt_amount_str,alt_daddr,sig_str) = partial_spend_p2sh(redeemScript,reinmediator,daddr,alt_amount,alt_daddr)

print (txins_str,amount_str,daddr,alt_amount_str,alt_daddr,sig_str)

#print(spend_p2sh(redeemScript,txins_str,float(amount),daddr,sig,"cUtVwDQqPn75KjnF5Qa3kyVUQmE4gprami3QW1QughTACnkHQHpa"))
amounts = [float(amount_str),float(alt_amount_str)]
daddrs = [daddr,alt_daddr]
print spend_p2sh(redeemScript,txins_str,amounts,daddrs,sig_str,reinclient)
