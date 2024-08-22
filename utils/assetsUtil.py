
import csv
import os
from django.utils.html import strip_tags
from datetime import datetime
import json
from utils.db_manager.db_manager import AssetDBManager,ProfileManager,TickersManager

from pymongo import MongoClient

from chanblockweb.settings import base

def get_assets() -> list:
    """
    Retrieves assets for the current date or for the last available date if no assets are found for the current date.
    :param manager: Instance of AssetDBManager
    :return: List of assets
    """
    manager= AssetDBManager()
    timestamp = str(datetime.now().date())
    list_assets = manager.find_by_date(timestamp)

    if len(list_assets) == 0:
        last_record_date = manager.find_last_record_date()
        if len(last_record_date) > 0:
            last_date = last_record_date[0]['date']
            list_assets = manager.find_by_date(last_date)

    for assets in list_assets:
        assets['metrics']['marketcap']['current_marketcap_usd'] = assets['metrics']['marketcap']['current_marketcap_usd'] / pow(10, 6)

    return list_assets
   
    

def list_variable():
    """
    Lee y retorna una lista de variables desde un archivo CSV.

    Returns:
        list: Una lista de listas, donde cada sublista contiene variables leídas de una línea del archivo CSV.
    """
    list_variable=[]
    dir_file=os.path.join(base.BASE_DIR,'..', 'static','file','DataMessariSplitMetrics.csv')
    dir_file1="/home/wtfinance/chanblock/chanblockEnv/chanblock_2022_10_21/static/file/metrics_name.csv"
                       
    with open(dir_file) as File:
        reader = csv.reader(File, delimiter=',', quotechar=',',
                        quoting=csv.QUOTE_MINIMAL)
        for variable in reader:            
            list_variable.append(variable[0].split(';'))

    return list_variable   


def list_variableTable():
    list_variableTable=[]
    dir_file1=os.path.join(base.BASE_DIR,'..', 'static','file','DataMessariSplitMetrics.csv')
         
    with open(dir_file1) as File:
        reader = csv.reader(File, delimiter=',', quotechar=',',
                        quoting=csv.QUOTE_MINIMAL)
        for variable in reader:
            # print(variable[0])            
            list_variableTable.append(variable[0].split(';'))

    return list_variableTable


def titleTable(dict):
  name_metrics=[]
  name_metrics.append('rank')
  name_metrics.append('crypto')
  list_metrics=list_variableTable()

  for row in dict:
    if len(dict[row])== 0:
      dict.pop(row)
    else:
      for variable in dict[row]:
        aux= row+variable
        # name from file csv
        for metrics in list_metrics:
          if metrics[0]+metrics[1] == aux:
              name_metrics.append(metrics[4])
              
  return name_metrics


def coin_detail(symbol):
    """
    Recupera y organiza detalles y perfiles de una moneda por su símbolo.

    Args:
        symbol (str): Símbolo de la moneda a buscar.

    Returns:
        dict: Contiene los detalles del activo y su perfil, incluyendo métricas clave,
              información del perfil (categoría, sector, tecnología, etc.), y el símbolo de TradingView.
    """
    #connection to collection assets
    asset_manager = AssetDBManager()
    profile_manager= ProfileManager()
    tickers_manager = TickersManager()
    listMetric = asset_manager.find_asset_by_symbol(symbol)
    profile = profile_manager.find_latest_profile()

    roi_detail1=[]
    for key , value in zip(listMetric['metrics']['roi_by_year'].keys(),listMetric['metrics']['roi_by_year'].values()):       
        
        if value != 0:
            roi_detail1.append([key[:4] , value])
    listMetric['metrics']['roi_by_year']=roi_detail1

    #generacion de un list()para el tratamiento de los datos del profile
    profile_detail=list()
    for doc in profile:  
     for ind in doc:
        if doc[ind]['name']==listMetric['name']:
         profile_detail={'category':doc[ind]['profile']['general']['overview']['category']}
         profile_detail['tagline']=doc[ind]['profile']['general']['overview']['tagline']
         profile_detail['sector']=doc[ind]['profile']['general']['overview']['sector']         
         profile_detail['roadmap']=format_date(doc[ind]['profile']['general']['roadmap'])
         profile_detail['economics']=doc[ind]['profile']['economics']
        #eliminacion de tag con strip_tags 
         profile_detail['project_details']=strip_tags(doc[ind]['profile']['general']['overview']['project_details'])        
         profile_detail['technology']=strip_tags(doc[ind]['profile']['technology']['overview']['technology_details'])
         profile_detail['regulatory_details']=strip_tags(doc[ind]['profile']['general']['regulation']['regulatory_details'])
         profile_detail['governance']=strip_tags(doc[ind]['profile']['governance']['governance_details'])
         profile_detail['economics_launchDetails']=strip_tags(doc[ind]['profile']['economics']['launch']['general']['launch_details'])


    #find symbol_tradingview para el requeste del widget 
    symbol_coins = tickers_manager.find_latest_symbols() 
    for symbol_coin in symbol_coins:
        for aux in symbol_coin:
         if aux == symbol:   
         # print(aux,':',symbol_coin[aux])
          profile_detail['symbol_tradingview']=symbol_coin[aux]
    
    coin_detail={'asset': listMetric,'profile': profile_detail}  
   
    return coin_detail

def format_date(roadmap):
    for iterator in roadmap:
        aux = iterator['date'] 
        if iterator['date']:              
         dto = datetime.strptime(aux, "%Y-%m-%dT%H:%M:%SZ").date()                                         
         iterator['date']= dto
    
    return roadmap
