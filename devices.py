#!/usr/bin/env python
# device demons of epic legandary counterparty blockchain streaming proportions... chris b peter j  devices.py

from flask import Flask, jsonify, request
import json
import requests
from requests.auth import HTTPBasicAuth
import time
#######################################
#Counterparty endpoint (default: coindaddy)
#
#Currently HTTP -- adjustable with: @app.route("/add-fednode", methods=['POST'])
#                                   def add_fednode():
url = "http://206.189.192.166:14000/"
headers = {'content-type': 'application/json'}
auth = HTTPBasicAuth('rpc', 'rpc')
#Bitcoin endpoint (default: coindaddy)
#
#Currently HTTP -- adjustable with: @app.route("/add-fednode", methods=['POST'])
#                                   def add_fednode():
urlB = "http://206.189.192.166:18332/"
headersB = {'content-type': 'application/json'}
authB = HTTPBasicAuth('rpc', 'rpc')
urlC = "http://public.coindaddy.io:14100/api/"
headersC = {'content-type': 'application/json'}
authC = HTTPBasicAuth('rpc', '1234')
#Block explorer api
urlX = "https://testnet.xchain.io/api/"
#nothing to see here#
PHONE_PUB = 'msrt1G7TL2PwVNU7Qo8z7tmbLBDMfDBjXJ'
PHONE_PRV = 'cRT1HVbuPr9e2LjpLBUvVpmog7NWhMDjP7wQrgieMT1DJAtLkS3f'
GUN_PUB = 'n2RqFDvTFVYwxnMf3ZKytV3cGzP44vDATb'
GUN_PRV = 'cRNkCJh1dQ5sbM2PuymN8M1NixXa4VjSXGGaHAp8RL6byWe1hxxy'
DRONE_PUB = 'mkbzBXagaWpKZemjYWsTwjPiqTZXt2b7xi'
DRONE_PRV = 'cTFERWg7GLkvmJYi5AUowEYJtoNAmdj3FZigUdWjqJ7L2ZFHPBPz'
OTHER_PUB = 'mqH3jBrp3b5yWQAJ3wQCJyXkvp4nvq6J2U'
OTHER_PRV = 'cQxnzLmUQPPuocLKHuk9JgTgAnWdg61qXD518TxjFu14CuDCKxVa'

try:
    # The typical way to import flask-cors
    from flask.ext.cors import CORS, cross_origin
except ImportError:
    # Path hack allows examples to be run without installation.
    import os
    parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(0, parentdir)

    from flask.ext.cors import CORS, cross_origin

app = Flask(__name__)

# Set CORS options on app configuration
app.config['CORS_HEADERS'] = "Content-Type"
app.config['CORS_RESOURCES'] = {r"/api/*": {"origins": "*"}}

cors = CORS(app)

## Equivalent to (but using both is not advised)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}},
            headers="Content-Type")

#Input: formated issuance paramaters
#returns response from counterparty server
def counterparty_api_issuance(params):
    payload = {
        "method": 'create_issuance',
        "params": params,
        "jsonrpc": "2.0",
        "id": 0
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)
    pres = json.loads(response.text)
    hexString = pres['result']
    return hexString
#Input: formated send paramaters
#returns response from counterparty server
def counterparty_api_send(params):
    payload = {
        "method": 'create_send',
        "params": params,
        "jsonrpc": "2.0",
        "id": 0
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)
    pres = json.loads(response.text)
    hexString = pres['result']
    return hexString
#Input: unsigned hash and privatekey
#decode and signs tx using bitcoin server
#returns signed transaction
def decodeAndSign(hash_tx,prv):
    payloadB = {
        "method": "decoderawtransaction",
        "params": [hash_tx],
        "jsonrpc": "2.0",
        "id": 0
    }
    responseB = requests.post(urlB, data=json.dumps(payloadB), headers=headersB, auth=authB)
    rawTX = json.loads(responseB.text)
    tx_id = rawTX['result']['txid']
    scriptPubKey = rawTX['result']['vout'][0]['scriptPubKey']['asm']
    scriptPubKey = scriptPubKey.split(' ')[1]
    payloadB = {
        "method": "signrawtransaction",
        "params": [
            hash_tx,
            [{"txid":tx_id,
              "vout":0,
              "scriptPubKey": scriptPubKey,
              "redeemScript": None,
              "amount": 0.0001}],
            [prv]
        ],
        "jsonrpc": "2.0",
        "id": 0
    }
    responseB = requests.post(urlB, data=json.dumps(payloadB), headers=headersB, auth=authB)
    rawSigned = json.loads(responseB.text)
    signed_tx = rawSigned['result']['hex']
    return signed_tx
#############################################################
#Input: params for issuance
#broadcasts the transaction to bitcoin server
#returns tx_hash
def do_issuance(source, sourcePrv, asset, quantity, desc, div):
    unsigned_tx = counterparty_api_issuance({"source": source,"asset": asset,"quantity": quantity,"description": desc,"divisible": div})
    signed_tx = decodeAndSign(unsigned_tx,sourcePrv)
    new_tx_hash_issuance = signed_tx
    payloadB = {
        "method": "sendrawtransaction",
        "params": [signed_tx],
        "jsonrpc": "2.0",
        "id": 0
    }
    responseB = requests.post(urlB, data=json.dumps(payloadB), headers=headersB, auth=authB)
    tx_confirm_raw = json.loads(responseB.text)
    tx_confirm = tx_confirm_raw['result']
    return tx_confirm
#Input: params for ownership transfer
#broadcasts the transaction to bitcoin server
#returns tx_hash
##Untested
def do_transfer(source, sourcePrv, asset, quantity, desc, div):
    unsigned_tx = counterparty_api_issuance({"source": source, "asset": asset, "quantity": quantity, "description": desc, "divisible": div})
    signed_tx = decodeAndSignDev(unsigned_tx, sourcePrv)
    new_tx_hash_issuance = signed_tx
    payloadB = {
        "method": "sendrawtransaction",
        "params": [signed_tx],
        "jsonrpc": "2.0",
        "id": 0
    }
    responseB = requests.post(urlB, data=json.dumps(payloadB), headers=headersB, auth=authB)
    tx_confirm_raw = json.loads(responseB.text)
    tx_confirm = tx_confirm_raw['result']
    return tx_confirm
#Input: params for asset send
#broadcasts transaction to bitcoin server
#returns tx_hash
def do_send(source, sourcePrv, destination, asset, quantity, memo):
    unsigned_tx = counterparty_api_send({'source': source, 'destination': destination, 'asset': asset, 'quantity': quantity, 'memo': memo})
    signed_tx = decodeAndSign(unsigned_tx,sourcePrv)
    new_tx_hash_send = signed_tx
    payloadB = {
        "method": "sendrawtransaction",
        "params": [signed_tx],
        "jsonrpc": "2.0",
        "id": 0
    }
    responseB = requests.post(urlB, data=json.dumps(payloadB), headers=headersB, auth=authB)
    tx_confirm_raw = json.loads(responseB.text)
    tx_confirm = tx_confirm_raw['result']
    return tx_confirm
#Input: params for asset send device
#broadcasts the transaction to bitcoin server
#returns tx_hash
##Dev for devices
def do_send_device(source,sourcePrv, destination, asset, quantity, memo):
    unsigned_tx = counterparty_api_send({'source': source, 'destination': destination, 'asset': asset, 'quantity': quantity, 'memo': memo})
    signed_tx = decodeAndSignDev(unsigned_tx,sourcePrv)
    new_tx_hash_send = signed_tx
    payloadB = {
        "method": "sendrawtransaction",
        "params": [signed_tx],
        "jsonrpc": "2.0",
        "id": 0
    }
    responseB = requests.post(urlB, data=json.dumps(payloadB), headers=headersB, auth=authB)
    tx_confirm_raw = json.loads(responseB.text)
    tx_confirm = tx_confirm_raw['result']
    return tx_confirm
#########################################################################
#Input: pubAddress
#returns all assets under that address
def get_assets(addr):
    payload = {
        "method": "get_balances",
        "params": {
            "filters": [{"field": "address", "op": "==", "value": addr}],
        },
        "jsonrpc": "2.0",
        "id": 0
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)
    raw_assets = json.loads(response.text)
    assets = raw_assets['result']
    return assets
#Input: asset name
#returns asset info
def get_asset_info(asset):
    payload = {
        "method": "get_asset_info",
        "params": {'assets':[asset]},
        "jsonrpc": "2.0",
        "id": 0
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)
    raw_assets_info = json.loads(response.text)
    assets_info = raw_assets_info['result']
    return assets_info
#Input: address
#pulls assets from counterparty server
#formats response
#returns [{'DeviceID': '', 'DeviceName': '', 'DeviceKey': '', 'DeviceType': ''}]
def format_assets(address):
    all_assets = get_assets(address)
    build_list = []
    for x in all_assets:
        build_json = get_asset_info(x['asset'])[0]
        final_json = {'DeviceID': '', 'DeviceName': '', 'DeviceKey': '', 'DeviceType': ''}
        
        if x['asset'] != 'XCP':
            final_json['DeviceID'] = x['asset']
            if build_json['asset_longname'] == None:
                final_json['DeviceName'] = 'No name'
                final_json['DeviceType'] = x['asset']
            else:
                name = build_json['asset_longname']
                nameL = name.split('.')
                final_json['DeviceName'] = nameL[1]
                final_json['DeviceType'] = nameL[0]
            final_json['DeviceKey'] = build_json['description']
        build_list.append(final_json)
        
    return build_list
def get_asset_history(asset):
    payload = {
           "method": "get_asset_history",
           "params": {'asset':asset},
           "jsonrpc": "2.0",
           "id": 0
          }
    response = requests.post(urlC, data=json.dumps(payload), headers=headers, auth=authC)
    raw_assets_info = json.loads(response.text)
    print(raw_assets_info)
    assets_info = raw_assets_info['result']
    return assets_info
def get_asset_issuances(asset):
    response = requests.get(urlX+'issuances/'+asset)
    outJson = response.json()['data'][0]
    return outJson
#Input: asset/DeviceName
#pulls asset info from counterparty server
#formats response
#returns [{'DeviceID': '', 'DeviceName': '', 'DeviceKey': '', 'DeviceType': '', 'DeviceIssuer':'', 'IssuanceTimestamp':''}]
def format_asset_details(asset):
    asset_info = get_asset_issuances(asset)
    final_json = {'DeviceID': '', 'DeviceName': '', 'DeviceKey': '', 'DeviceType': '', 'DeviceIssuer':'', 'IssuanceTimestamp':''}
    
    final_json['DeviceID'] = asset_info['asset']
    if asset_info['asset_longname'] == None:
        final_json['DeviceName'] = 'No name'
        final_json['DeviceType'] = asset_info['asset']
    else:
        name = asset_info['asset_longname']
        nameL = name.split('.')
        final_json['DeviceName'] = nameL[1]
        final_json['DeviceType'] = nameL[0]
        final_json['DeviceKey'] = asset_info['description']
        final_json['DeviceIssuer'] = asset_info['issuer']
        final_json['IssuanceTimestamp'] = time.ctime(int(asset_info['timestamp']))
        
    return final_json
#Input: DeviceType-phone/gun/drone
#returns address and asset info
def handle_device_type(devType):
    if devType == 'phone':
        return ['SIOTPHONE',PHONE_PUB,PHONE_PRV]
    if devType == 'gun':
        return ['SIOTGUN',GUN_PUB,GUN_PRV]
    if devType == 'drone':
        return ['SIOTDRONE',DRONE_PUB,DRONE_PRV]
    return ['SIOTOTHER',OTHER_PUB,OTHER_PRV]
@app.route("/", methods=['GET', 'POST'])
def index():
    return jsonify({"about":"Hello World!"})
#Change sever info for counterparty
#'{"counterparty":"http://206.189.192.166:14000","user":"rpc", "pass":"rpc",}'
##dev
@app.route("/add-counterparty-server", methods=['POST'])
def add_counterparty():
    inj = request.get_json()
    url = inj['counterparty']
    auth = HTTPBasicAuth(inj['user'],inj['pass'])
    return url
#Change sever info for bitcoin
#'{"bitcoin":"http://206.189.192.166:18332","user":"rpc", "pass":"rpc",}'
##dev
@app.route("/add-bitcoin-server", methods=['POST'])
def add_bitcoin():
    inj = request.get_json()
    urlB = inj['bitcoin']
    authB = HTTPBasicAuth(inj['user'],inj['pass'])
    return urlB
#Input: '{"DeviceKey":"", "DeviceName":"", "DeviceType":"phone/gun/drone/other"}'
#Creates subasset from respective providers asset
#returns tx
@app.route("/add-device", methods=['POST'])
def add_device():
    inj = request.get_json()
    dataBuild = '{K:'+inj['DeviceKey']+'}'
    assetBuild = handle_device_type(inj['DeviceType'])
    tx_hash = do_issuance(assetBuild[1],assetBuild[2],assetBuild[0]+'.'+inj['DeviceName'], 1, dataBuild, False)
    return jsonify({'tx_hash': tx_hash}), 201
#####################################################################################
# confirm tx is valid with /Check-tx/tx_hash before sending asset with /send-device #
#####################################################################################
#Input: '{"DeviceType":"phone/gun/drone","Address":"", "DeviceName":"", "data":"{key:value}"}'
#sends device asset token to address
#returns tx
@app.route("/send-device", methods=['POST'])
def send_device():
    inj = request.get_json()
    assetBuild = handle_device_type(inj['DeviceType'])
    
    tx_hash = do_send(assetBuild[1],assetBuild[2], inj['Address'], assetBuild[0]+'.'+inj['DeviceName'], 1 ,inj['data'])
    return jsonify({'tx_hash': tx_hash}), 201
#Input: hash_tx
#returns True or False for valid status
@app.route("/check-tx/<string:tx>", methods=['GET'])
def check_tx(tx):
    response = requests.get(urlX+'tx/'+tx)
    return str(response.json()['status'] == 'valid')
#retuns list of assets for address
#[{"DeviceType":"phone/gun/drone", "DeviceName":"", "DeviceKey":"", "DeviceID":""}]
@app.route('/get-devices/<string:pubname>', methods=['GET'])
def get_devices(pubname):
    out_assets = format_assets(pubname)
    return jsonify({'result':out_assets})
#retuns details of asset
#[{"DeviceType":"phone/gun/drone", "DeviceName":"", "DeviceKey":"", "DeviceID":""}]
@app.route('/get-device-details/<string:DeviceID>', methods=['GET'])
def get_device_details(DeviceID):
    asset_details = format_asset_details(DeviceID)
    return jsonify({'result':asset_details})
#Input: '{"addFrom":"","prvKey":"", "addTo":"", "name":"", "data":"{key:value}"}'
#sends asset "name" from "addFrom" to "addTo"
#returns tx
@app.route("/send", methods=['POST'])
def send():
    inj = request.get_json()
    tx_hash = do_send(inj['addFrom'], inj['prvKey'], inj['addTo'], inj['name'], 1 ,inj['data'])
    return jsonify({'tx_hash': tx_hash}), 201
##############
@app.route("/add-device-dev", methods=['POST'])
def add_device_dev():
    inj = request.get_json()
    dataBuild = '{K:'+inj['DeviceKey']+'}'
    assetBuild = handle_device_type(inj['DeviceType'])
    tx_hash = do_issuance(assetBuild[1],assetBuild[2],assetBuild[0]+'.'+inj['DeviceName'], 1, dataBuild, False)
    return jsonify({'tx_hash': tx_hash}), 201
if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
