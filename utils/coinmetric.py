

from utils.db_manager.db_manager_coinmetric import CoinmetricDBManager




def create_graph(symbol):
    
    db_manager = CoinmetricDBManager()
    listXY = []
    unmetric = []
    modelSymbol = []
    # condicional para saber si la variable symbol es un array o str
    if type(symbol) == str:
        isArray = False
        getvalues = db_manager.get_price(symbol, 'PriceUSD')
        listXY.append(getvalues)
        modelSymbol.append(symbol)
    else: 
        isArray = True
        if len(symbol['metric']) == 1:            
            for i in symbol['assets']:
                metric = symbol['metric'][0]
                getvalues = db_manager.get_price(i, metric)
                if len(getvalues)==0:
                    unmetric.append(i)
                else:    
                    listXY.append(getvalues)
                    modelSymbol.append(i)
    return {'listXY': listXY, 'modelSymbol': modelSymbol}

def create_graph_metrics(symbol,metric):
    db_manager = CoinmetricDBManager()
    listXY = []
    unmetric = []
    modelSymbol = []
    # condicional para saber si la variable symbol es un array o str
    if type(symbol) == str:
        isArray = False
        getvalues = db_manager.get_values(symbol, metric)
        listXY.append(getvalues)
        modelSymbol.append(symbol)
    else: 
        isArray = True
        if len(symbol['metric']) == 1:            
            for i in symbol['assets']:
                metric = symbol['metric'][0]
                getvalues = db_manager.get_price(i, metric)
                if len(getvalues)==0:
                    unmetric.append(i)
                else:    
                    listXY.append(getvalues)
                    modelSymbol.append(i)
    return {'listXY': listXY, 'modelSymbol': modelSymbol}   

