import json
from web3 import Web3
from hexbytes import HexBytes
from decimal import Decimal
import os
from pathlib import Path
from pymongo import MongoClient
from chanblockweb.settings.base import env

BASE_DIR = Path(__file__).resolve().parent.parent
token_metadata="static/json/tokenMetadata.json"
dir_token_metadata = os.path.join(BASE_DIR,token_metadata)

client = MongoClient(env('MONGOATLAS_USER'))
db = client.metaData

provider ="https://eth-mainnet.g.alchemy.com/v2/LlNcOonosHij2PiE8TdwutxYZtKvVfGV" 
w3 = Web3(Web3.HTTPProvider(provider))


def check_fees_alchemy():
    block_pending= w3.eth.get_block('pending', True)
    txns_receipt=[]
    for value in block_pending['transactions']:

        if value['gas'] > 1000:
            txn={}
            hb= value['hash']
            txn['hash']= hb.hex()
            txn['from']=value['from']
            txn['to']=value['to']
            txn['gas']=value['gas']
            txn['value']= value['value']
            txn['type']=value['type']
            txns_receipt.append(txn)
    return txns_receipt

# Función para obtener los recibos de transacción del bloque pendiente
def txn_receipt():
    # Obtener el bloque pendiente y sus transacciones
    block_pending= w3.eth.get_block('pending', True)
    txns_receipt=[]
    
    # Iterar a través de cada transacción en el bloque pendiente
    for value in block_pending['transactions']:
        txn_hash = value['hash'].hex()
        try:
            # Obtener el recibo de transacción
            receipt = w3.eth.get_transaction_receipt(txn_hash)
            receipt['gasUsed']
           # Verificar si el gas utilizado es mayor que 100,000
            if receipt['gasUsed'] > 100000:
                txn={}

                
                # Agregar información de la transacción al diccionario
                txn['hash']=receipt['transactionHash'].hex()
                txn['blockNumber']= receipt['blockNumber']
                
                # Verificar si hay registros en el recibo de transacción
                if len(receipt['logs']) > 0:
                    txn['topics']= topics_txn(receipt['logs'])
                # else:
                #     txn['topics']=[]
                    if len(txn['topics']) > 0:
                        txn['type']=receipt['type']
                        txn['from']=receipt['from']
                        
                        # Verificar si el destino de la transacción existe
                        if receipt['to']:
                            txn['to']=receipt['to']
                        else:
                            txn['to']=""
                        txn['gasUsed']=receipt['gasUsed']  # und Gwei
                        txn['gasUsed_eth']=receipt['gasUsed']/10**9 #conversion a eht 10**9 Gwei => 1eth
                        txn['effectiveGasPrice']=receipt['effectiveGasPrice']/10**9 #effectiveGasPrice viene en unidades wei 10**9 wei => Gwei 
                        txn['effectiveGasPrice_eth']=receipt['effectiveGasPrice']/10**18 # 10**18 wei => 1eth
                        txn['txn_fee_eth']= (txn['gasUsed']*txn['effectiveGasPrice'])/10**9  #transaction fee es la multiplicacion del gas usado por el gas price
                        
                        # Agregar el diccionario de transacción a la lista de recibos de transacción
                        txns_receipt.append(txn)
               
        except Exception as e:
          print('-Transaction with hash not found')
    # Retornar la lista de recibos de transacción      
    return txns_receipt

def array_to_hex(arr):
    hex_arr = []
    if len(arr)> 0:
        if arr[0].hex()[:10] == '0xddf252ad':
            for item in arr:
                hex_arr.append(item.hex())
    return hex_arr

def is_transfer(arr):
    is_transfer= False
    if len(arr)> 0:
        
        if arr[0].hex()[:10] == '0xddf252ad':
            is_transfer=True
    return is_transfer

def topics_txn(logs):
    """
    Argumentos:
    logs -- una lista de logs obtenidos de una transacción

    Retorna:
    tokens -- una lista de diccionarios que representan los tokens transferidos en las transacciones
    """
    tokens = []
    decimal=0
    
    for log in logs:
        # Verificar si hay topics en el log

        if len(log['topics'])> 0:
            # Verificar si la transacción es una transferencia de tokens
            if is_transfer(log['topics']):
                token={}
                address= log['address']
                token['address']= log['address']
                
                # Obtener el nombre y el símbolo del token usando su dirección
                values  = get_token_name_by_address(address)
                
                if values:
                    token['name'] = values['name'] if values and values['name'] else ""
                    token['symbol']= values['symbol']
                    if values['decimal']:
                        decimal = values['decimal']
                else:
                    token['name']=""
                    token['symbol']= ""
                
                if log['data'] == "0x":
                    data_int= 0
                else:
                    data_int = int.from_bytes(log['data'], 'big') 
                    
                    # data=int(log['data'], 16)
                # token['data'] = data/10**decimal
                token['data']=data_int  
                tokens.append(token)
    return tokens

def read_json_metadata():
    with open(dir_token_metadata) as f:
        data = json.load(f)
    token_names = [{'address': item['address'], 'name': item['name']} for item in data]
    return token_names

def get_token_name_by_address(address):
    """
    Obtiene la información de metadatos de un token a partir de su dirección
    Args:
    - address (str): Dirección en formato hexadecimal de un token.

    Returns:
    - dict: Diccionario con los valores de los metadatos del token (nombre, símbolo y cantidad de decimales).
            Si no se encuentra información para la dirección proporcionada, se retorna None.
    """
    try:
        address = address.lower()
        #connection to collection tokens metadata
        tokens_metadata = db.tokens_metadata
        # Se realiza una consulta a la base de datos para obtener los metadatos del token
        dbmetadata= tokens_metadata.find_one({'address':address},{"_id":0})
        # print(dbmetadata)
        if dbmetadata != None :
            
            # Se crea un diccionario con los valores de los metadatos del token
            list={}
            list['name']=dbmetadata['name']
            if dbmetadata['symbol']:
                list['symbol']= dbmetadata['symbol']
            else:
                list['symbol']= ""
            if dbmetadata['decimal']:
                list['decimal']=dbmetadata['decimal']
            else:
                list['decimal']=0
            return list
        else:
            return None
           
    except StopIteration:
        return None      

