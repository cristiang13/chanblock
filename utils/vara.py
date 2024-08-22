from utils.db_manager.db_manager_vara import VaraDBManager
from .helper import convert_to_datetime
from assetModule.plot import create_plot_metrics_vara
from chanblockweb.settings.base import env
import requests

def get_vara_price(api_key):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=VARA"
    url2 = "https://min-api.cryptocompare.com/data/price?fsym=VARA&tsyms=USD"
    headers = {'X-CMC_PRO_API_KEY': api_key}
    headers2 = {'Accept': 'application/json'}

    try:
        response = requests.get(url2, headers=headers2)
        # Verificar si la respuesta es exitosa
        response.raise_for_status()

        data = response.json()
        # return data['data']['VARA']['quote']['USD']['price']
        return data['USD']
    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Error de Conexión: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Error de Timeout: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Error en la Solicitud: {req_err}")
    except KeyError as key_err:
        print(f"Error en los datos recibidos: {key_err}")
    except Exception as e:
        print(f"Otro error: {e}")

    return 1



def get_fees_avg(blockDetails):
    """
    Calcula el promedio de tarifas de gas (ajustadas por el precio actual de la moneda) para cada bloque.

    Args:
        blockDetails (list): Una lista de detalles de bloques, donde cada elemento es un diccionario
                             que contiene información detallada de un bloque, incluyendo eventos y
                             extrínsecos.
    
    Returns:
        list: Una lista de diccionarios con el tiempo (datetime) y la tarifa promedio ajustada ('fee_avg')
              para cada bloque.
    """
    db_manager = VaraDBManager()
    values = db_manager.get_last_price_usd()
    precioMoneda = values[0]['priceUSD']
    # precioMoneda = get_vara_price(env('API_KEY_COINMARKETCAP'))
    data = []
    for value in blockDetails:
        timestamp = value['blockDetails']['block']['extrinsics'][0]['method']['args']['now']
        datatime = convert_to_datetime(timestamp)
        
        # Obtener el averageGasLimit y ajustarlo
        averageGasLimit = value['averageGasLimit']
        averageGasLimitAjustado = (averageGasLimit / 1e12) * precioMoneda

        data.append({'time': datatime, 'fee_avg': averageGasLimitAjustado})
       
    return data


def get_count_tnx_events(blockDetails):
    """
    Obtiene el conteo de transacciones y el tiempo de cada bloque en una lista de detalles de bloques.

    Args:
        blockDetails (list): Una lista de detalles de bloques, donde cada elemento es un diccionario
                             que contiene información detallada de un bloque, incluyendo eventos y
                             extrínsecos.
    
    Returns:
        list: Una lista de diccionarios con el tiempo (datetime) y el conteo de transacciones ('count_txn')
              para cada bloque.
    """
    data = []
    for value in blockDetails:
        timestamp = value['blockDetails']['block']['extrinsics'][0]['method']['args']['now']
        datatime = convert_to_datetime(timestamp)
        # count_txn = len(value['events'])
        count_txn = value['cantidadTxns']
        data.append({'time': datatime, 'count_txn': count_txn})
    
    return data

def get_last_three_blocks():
    """
    Obtiene información de los últimos tres bloques, incluyendo el número de bloque,
    el número de transacciones y el promedio del límite de gas por transacción.

    Returns:
        list: Una lista de diccionarios, cada uno con detalles de un bloque.
    """
    db_manager = VaraDBManager()
    values = db_manager.get_last_three_documents()
    values_blocks=[]
    for value in values:
        data_fee = []
        number_block = value['blockNumber']
        number_txns = len(value['events'])
        # print("value", value['blockDetails']['block']['extrinsics'])
        for block in value['blockDetails']['block']['extrinsics'][1:]:
            # # Usando el método get para evitar KeyError
            gas_limit = block['method']['args'].get('gas_limit')
            if gas_limit:
                # Eliminar las comas y convertir a entero
                gas_limit = int(gas_limit.replace(',', ''))
                data_fee.append(gas_limit)
        # Calcular el promedio si hay datos disponibles
        if data_fee:
            avg_gas_limit = sum(data_fee) / len(data_fee)
        else:
            avg_gas_limit = 0

        values_blocks.append({ 'number_block': number_block,'number_txns': number_txns, 'fees_avg': avg_gas_limit})
    return values_blocks
    

def plots_vara():
    """
    Genera dos gráficos a partir de los eventos de bloques de las últimas 24 horas, cada 10 minutos.

    El primer gráfico representa la cantidad de transacciones, y el segundo, el promedio de tarifas.

    Returns:
        dict: Un diccionario con dos claves, 'plot' y 'plot2', que contienen los gráficos generados.
    """
    db_manager = VaraDBManager()
    getvalues = db_manager.get_blockDetails_events_24h_every_10min()
    get_fees_prom = get_fees_avg(getvalues)
    get_count_tnx = get_count_tnx_events(getvalues)

    get_fees_prom.sort(key=lambda x: x['time'])
    get_count_tnx.sort(key=lambda x: x['time'])

    plot = create_plot_metrics_vara(get_count_tnx)
    plot2 = create_plot_metrics_vara(get_fees_prom)

    context={
        'plot': plot,
        'plot2': plot2
    }


    return context

