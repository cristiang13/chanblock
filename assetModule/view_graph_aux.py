import json
from django.http import JsonResponse
from django.shortcuts import render
from utils.coinmetric import create_graph
from utils.assetsUtil import list_variable
from utils.vara import plots_vara, get_last_three_blocks
from .plot import create_plot_default,create_plot_metrics # Asegúrate de importar la función correctamente

from django.http import StreamingHttpResponse
from django.core.cache import cache
import time

# Create your views here.
def graphics(request):
  """
  Renderiza una página con gráficos del precio de Bitcoin (BTC) a lo largo del tiempo.     
  Esta función llama a `create_graph` con 'btc' como argumento para obtener datos históricos de precios de Bitcoin. Luego, procesa estos datos extrayendo las fechas y los precios para generar un gráfico. Los datos procesados se pasan al contexto de una plantilla HTML específica, que luego se usa para renderizar la página web con el gráfico de precios de Bitcoin.   
  Args:
      request: Objeto HttpRequest, representa la solicitud HTTP entrante.  
  Returns:
      HttpResponse: Objeto que representa la respuesta HTTP, incluyendo el contenido HTML de la página con el gráfico de precios de Bitcoin incrustado.    
  Nota:
      La función asume que `create_graph` devuelve un diccionario con una lista de diccionarios bajo la clave 'listXY', donde cada diccionario contiene las claves 'time' y 'PriceUSD', representando la fecha y el precio de Bitcoin respectivamente.
  """
  getvalues= create_graph('btc')
 
  # Extraer los datos para el gráfico
  fechas = [dato['time'].strftime("%Y-%m-%d") for dato in getvalues['listXY'][0]]
  precios = [float(dato['PriceUSD']) for dato in getvalues['listXY'][0]]  
  context = {
      'fechas': fechas,
      'precios': precios
  } 
  return render(request, 'assets/graphic/graphics.html', context)


def plot_view(request):
    """
    Renderiza una página que muestra un gráfico predeterminado y una lista de variables de Coinmetrics.

    Esta función genera un gráfico utilizando la función `create_plot_default` y obtiene una lista de variables disponibles para gráficos a través de `list_variable`. Ambos, el gráfico y la lista de variables, se pasan al contexto de la plantilla HTML especificada para ser renderizados en la página web.

    Args:
        request: Objeto HttpRequest, representa la solicitud HTTP entrante.

    Returns:
        HttpResponse: Objeto que representa la respuesta HTTP, incluyendo el contenido HTML de la página con el gráfico y la lista de variables incrustados.

    Nota:
        Esta vista está diseñada para ser accesible mediante cualquier método HTTP, pero principalmente se espera que sea utilizada con solicitudes GET para visualizar la página con los datos ya preparados.
    """
    plot = create_plot_default()
    variable_coinmetrics= list_variable()
    return render(request, 'assets/graphic/graphics.html', context={'plot': plot, 'variable_coinmetrics':variable_coinmetrics})


def plot_metrics_view(request):
    """
    Procesa solicitudes POST para generar gráficos basados en métricas especificadas en el cuerpo de la solicitud.

    Cuando recibe una solicitud POST, esta función parsea el cuerpo de la solicitud como JSON para extraer las métricas solicitadas. Utiliza estas métricas para generar los gráficos correspondientes mediante la función `create_plot_metrics`, que devuelve un contexto conteniendo los gráficos y las métricas procesadas. Finalmente, retorna este contexto como un objeto JsonResponse, facilitando la integración con clientes que consuman esta API de forma asincrónica.

    Args:
        request: Objeto HttpRequest, representa la solicitud HTTP entrante.

    Returns:
        JsonResponse: Solo para solicitudes POST, devuelve un objeto JsonResponse con el gráfico generado y las métricas procesadas.
        Para otros métodos HTTP, actualmente no retorna nada, pero se puede ampliar para manejar diferentes tipos de solicitudes.

    Nota:
        Esta función está diseñada para ser utilizada con solicitudes POST. Las solicitudes que no sean POST se pasan sin acción, pero se podría extender para manejar otros métodos HTTP si fuera necesario.
    """
    if request.method == 'POST':
        # Parsear el cuerpo de la solicitud como JSON
        data = json.loads(request.body)
        metrics = data['metrics']
        context = create_plot_metrics(metrics)
        # Retorna un objeto JsonResponse
        return JsonResponse({'plot': context['plot'], 'metrics': context['metrics']})
    else:
        # Manejar otros métodos HTTP, si es necesario
        pass
   
def plot_metrics_vara_view(request):
    """
    Renderiza la página de métricas con gráficos generados por la función `plots_vara`.

    Esta vista obtiene los gráficos generados por `plots_vara`, que devuelve un diccionario con los gráficos 'plot' y 'plot2'. Luego, pasa estos gráficos al contexto de la plantilla 'vara/metrics.html' para su visualización en la página web.

    Args:
        request: Objeto HttpRequest, representa la solicitud HTTP entrante.

    Returns:
        HttpResponse: Objeto que representa la respuesta HTTP, incluyendo el contenido HTML de la página de métricas con los gráficos incrustados.
    """
    plot = plots_vara()
    
    return render(request, 'vara/metrics.html', context={'plot': plot['plot'], 'plot2': plot['plot2']})

def stream_last_three_blocks(request):
    """
    Transmite los últimos tres bloques de datos en tiempo real usando Server-Sent Events (SSE).

    Utiliza un bucle infinito para enviar continuamente los últimos tres bloques almacenados en caché al cliente, con una pausa de 3 segundos entre cada transmisión. Esta función es ideal para aplicaciones que necesitan mostrar datos actualizados dinámicamente sin recargar la página.

    Args:
        request: Objeto HttpRequest, no utilizado directamente pero requerido por la interfaz de la vista.

    Returns:
        StreamingHttpResponse: Permite la transmisión continua de datos en formato SSE al cliente.
    """
    def event_stream():
        while True:
            last_three_blocks = cache.get('last_three_blocks', [])
            yield f"data: {json.dumps(last_three_blocks)}\n\n"
            time.sleep(3)  # Controla la frecuencia de transmisión
    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')