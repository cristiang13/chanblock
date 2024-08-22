import plotly.graph_objs as go
import plotly.offline as pyo
from datetime import datetime
from utils.coinmetric import create_graph,create_graph_metrics

def create_plot_metrics(metrics):
    """
    Genera un gráfico interactivo para visualizar diversas métricas de Bitcoin (BTC) a lo largo del tiempo.

    Esta función recupera datos específicos de Bitcoin según las métricas seleccionadas utilizando la función 'create_graph_metrics' y procesa estos datos para generar un gráfico lineal. Cada métrica seleccionada se representa como una serie de datos en el gráfico, permitiendo comparar diferentes aspectos del comportamiento de Bitcoin a lo largo del tiempo.

    Parameters:
        metrics (list): Una lista de cadenas que representa las métricas a visualizar en el gráfico.

    Returns:
        Un diccionario que contiene el gráfico (como un objeto HTML div) y la métrica seleccionada, listo para ser incrustado en una página web o utilizado según sea necesario.

    Notas:
        - La función asume que 'create_graph_metrics' devuelve una lista de diccionarios con las claves correspondientes a las métricas seleccionadas y la clave 'time', donde 'time' es una cadena que representa la fecha.
        - El gráfico es interactivo y permite a los usuarios explorar las métricas a través de diferentes rangos de tiempo con controles interactivos.
        - Se aplican configuraciones adicionales para mejorar la interactividad y la presentación visual del gráfico, como la personalización de tooltips y la ocultación del logo de Plotly.
    """
    getvalues= create_graph_metrics('btc',metrics)
    # print('getvalues',getvalues)
    fechas = [dato['time'].strftime("%Y-%m-%d") for dato in getvalues['listXY'][0]]
    # Convertir las fechas a objetos datetime
    dates = [datetime.strptime(fecha, '%Y-%m-%d') for fecha in fechas] 
     # Crear una lista vacía para almacenar las trazas (series de datos)
    data = []

    # Añadir una traza por cada serie de datos
    for field in metrics:
        if field in getvalues['listXY'][0][0]:  # Comprobar si el campo existe en los datos
            values = [float(dato[field]) for dato in getvalues['listXY'][0]]
            # trace = go.Scatter(x=dates, y=values, mode='lines', name=field)
            trace = go.Scatter(
                x=dates, 
                y=values, 
                mode='lines', 
                name=field,
                hoverinfo='text',
                text=[f'{date}<br>{value}<br>{field}' for date, value in zip(dates, values)]  # Personalizar el contenido del tooltip
            )

            data.append(trace)
    
   
    # Configurar el layout con la altura deseada
    layout = go.Layout(
        height=660,  # Altura de la gráfica en píxeles
        yaxis=dict(side='right'),  # Coloca el eje Y en el lado derecho
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date"
        )
    )

    
    # Crear la gráfica con el layout configurado
    fig = go.Figure(data=data, layout=layout)
    # Aquí añades el resto de la configuración como el rangeslider, etc.

    # Configuración para ocultar el logo de Plotly y otros elementos
    config = {
        'displayModeBar': True,
        'modeBarButtonsToRemove': ['sendDataToCloud'],
        'showLink': False,
        'displaylogo': False
    }
    plot = pyo.plot(fig, output_type='div', config=config)

    context = {
        'plot': plot,
        'metrics': 'btc'
    }

    return context
    
    
def create_plot_default():
    """
    Genera un gráfico interactivo por defecto para visualizar los precios de Bitcoin (BTC) a lo largo del tiempo.

    Esta función recupera datos específicos de precios de Bitcoin utilizando la función 'create_graph' y luego procesa estos datos para generar un gráfico lineal que muestra la evolución del precio de Bitcoin a lo largo del tiempo. Utiliza Plotly para crear un gráfico interactivo que permite al usuario explorar diferentes rangos de fechas con facilidad.

    Returns:
        Un objeto gráfico (div) de Plotly como una cadena de texto HTML, listo para ser incrustado en una página web.

    Notas:
        - La función asume que 'create_graph' devuelve una lista de diccionarios con las claves 'time' y 'PriceUSD', donde 'time' es una cadena que representa la fecha y 'PriceUSD' el precio de Bitcoin en USD.
        - El gráfico incluye un selector de rango y botones para facilitar la visualización de períodos específicos.
        - Se aplican configuraciones adicionales para ajustar la interactividad y apariencia del gráfico, como ocultar el logo de Plotly y desactivar ciertos botones de la barra de herramientas.
    """
    getvalues= create_graph('btc')
 
    # Extraer los datos para el gráfico
    fechas = [dato['time'].strftime("%Y-%m-%d") for dato in getvalues['listXY'][0]]
    precios = [float(dato['PriceUSD']) for dato in getvalues['listXY'][0]]
    # Convertir las fechas a objetos datetime
    dates = [datetime.strptime(fecha, '%Y-%m-%d') for fecha in fechas] 

    # Configurar el layout con la altura deseada
    layout = go.Layout(
        height=600,  # Altura de la gráfica en píxeles
        yaxis=dict(
            side='right'  # Coloca el eje Y en el lado derecho
        )
    )

    # Crear la gráfica con el layout configurado
    data = [go.Scatter(x=dates, y=precios, mode='lines',line=dict(width=1) )]
    fig = go.Figure(data=data, layout=layout)
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    # Configuración para eliminar el logo de Plotly
    # Configuración para ocultar el mensaje "Produced with Plotly"
    config = {
        'displayModeBar': True,  # Muestra la barra de herramientas
        'modeBarButtonsToRemove': ['sendDataToCloud'],  # Elimina botones específicos
        'showLink': False,  # Desactiva el enlace a Plotly
        'displaylogo': False  # Oculta el logo de Plotly
    }
    plot = pyo.plot(fig, output_type='div',config=config)

    return plot



def create_plot_metrics_vara(values):
    """
    Genera un gráfico interactivo basado en los valores de métricas específicas como transacciones o tarifas promedio.

    Esta función analiza un conjunto de datos para determinar si contienen métricas relacionadas con el número de transacciones ('count_txn') o el promedio de tarifas ('fee_avg'). Basándose en esto, extrae las fechas y los valores correspondientes para crear un gráfico lineal interactivo utilizando Plotly.

    Args:
        values: Lista de diccionarios, cada uno representando una observación con claves como 'time', 'count_txn' o 'fee_avg'.

    Returns:
        Un objeto gráfico (div) de Plotly como una cadena de texto HTML, listo para ser incrustado en una página web.

    Notas:
        - Dependiendo de la métrica presente en los datos de entrada, el gráfico se etiqueta y configura adecuadamente para mostrar el número de transacciones o el promedio de tarifas en USD.
        - El gráfico incluye un selector de rango y botones para facilitar la visualización de períodos específicos.
        - Se aplican configuraciones adicionales para ajustar la interactividad y apariencia del gráfico.
    """
    # Verificar si estamos trabajando con 'count_txn' o 'fee_avg'
    if 'count_txn' in values[0]:
        # Extraer fechas y cantidad de transacciones
        fechas = [dato['time'] for dato in values]
        y_values = [dato['count_txn'] for dato in values]
        y_label = 'Number of transactions'
    elif 'fee_avg' in values[0]:
        # Extraer fechas y promedio de tarifas
        fechas = [dato['time'] for dato in values]
        y_values = [dato['fee_avg'] for dato in values]
        y_label = 'Average fee (USD)'

    # Crear el gráfico
    layout = go.Layout(
        title=y_label,
        height=600,
        yaxis=dict(title=y_label, side='right')
    )

    data = [go.Scatter(x=fechas, y=y_values, mode='lines', line=dict(width=1))]
    fig = go.Figure(data=data, layout=layout)

    # Configuraciones adicionales del gráfico
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    config = {
        'displayModeBar': True,
        'modeBarButtonsToRemove': ['sendDataToCloud'],
        'showLink': False,
        'displaylogo': False
    }

    plot = pyo.plot(fig, output_type='div', config=config)

    # Retornar el plot
    return plot