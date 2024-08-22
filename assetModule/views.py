
from multiprocessing import context
from typing import Type
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render,redirect
from utils import assetsUtil,userUtil,helper
from django.http import JsonResponse
from django.contrib import messages
from django.template.loader import render_to_string
from .view_graph_aux import *
from utils import alchemyUtil
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from utils.chat import getResponseChatGpt

def maintenance(request):  
  return render(request, 'maintenance.html')


def getAssets(request):
  """
    Recupera y muestra una lista de activos y métricas disponibles.

    Esta función obtiene una lista de activos financieros y las métricas disponibles para ellos utilizando utilidades específicas, y luego pasa estos datos al contexto de una plantilla HTML para su visualización. Está diseñada para ser utilizada en una aplicación web que requiere mostrar información sobre diferentes activos financieros junto con las métricas que se pueden aplicar a estos.

    Args:
        request: Objeto HttpRequest que representa la solicitud HTTP entrante.

    Returns:
        HttpResponse: Objeto que contiene la respuesta renderizada, incluyendo una página que muestra los activos y las métricas disponibles.

    Notas:
        - `assetsUtil.get_assets()` se utiliza para obtener una lista de activos financieros disponibles.
        - `assetsUtil.list_variableTable()` obtiene las métricas disponibles que se pueden aplicar a los activos.
        - La información recuperada se pasa a la plantilla `assets/createTable.html` para su visualización, facilitando a los usuarios la visualización de los activos y las métricas correspondientes.
  """
  assets= assetsUtil.get_assets()
  list_metrics=assetsUtil.list_variableTable()
  context={
    'list_metrics':list_metrics,
    'assets':assets
  } 
  return render(request, 'assets/createTable.html',context)


def coin_detail(request,symbol):
  """
    Renderiza una página de detalles para una criptomoneda específica basada en su símbolo.

    Esta función busca los detalles de una criptomoneda específica utilizando su símbolo y los presenta en una página dedicada. Utiliza una utilidad `assetsUtil` para obtener los detalles de la moneda y luego pasa estos detalles al contexto de una plantilla HTML específica para su visualización.

    Args:
        request: Objeto HttpRequest que representa la solicitud HTTP entrante.
        symbol: Cadena que representa el símbolo de la criptomoneda de la cual se desean obtener detalles.

    Returns:
        HttpResponse: Objeto que contiene la respuesta renderizada, incluyendo la página de detalles de la criptomoneda solicitada.

    Notas:
        - La función espera que `assetsUtil.coin_detail` sea un método que acepte un símbolo de criptomoneda y devuelva los detalles de la misma.
        - Los detalles obtenidos se pasan a la plantilla `assets/coin_detail.html` para su visualización, permitiendo a los usuarios ver información detallada sobre la criptomoneda especificada.
  """
  coin_detail= assetsUtil.coin_detail(symbol)
  return render(request, 'assets/coin_detail.html',{'coin_detail': coin_detail})



def showTable(request):
    """
    Renderiza una tabla HTML con métricas de activos basada en los datos enviados mediante una solicitud POST.

    Esta función recibe una solicitud POST, extrae los parámetros enviados (excluyendo el token CSRF), y utiliza estos parámetros para construir una lista de métricas de activos. Cada métrica se procesa para ajustarse a los parámetros solicitados. La función luego compila un contexto con la lista de métricas procesadas, los nombres de las columnas (obtenidos a través de una función de utilidad), y los parámetros de la solicitud original. Este contexto se usa para renderizar una tabla HTML utilizando una plantilla específica. La tabla renderizada se devuelve como respuesta HTTP.

    Args:
        request: Objeto HttpRequest, representa la solicitud HTTP entrante.

    Returns:
        HttpResponse: Objeto que contiene la tabla HTML renderizada como respuesta, listo para ser mostrado en el navegador del usuario.

    Notas:
        - La función asume que existe una utilidad `assetsUtil` que proporciona métodos para obtener las métricas de los activos y los títulos de las columnas basados en los parámetros de la solicitud.
        - Utiliza `helper.process_single_metric` para procesar cada métrica individualmente antes de incluirla en el contexto de la plantilla.
        - `render_to_string` se utiliza para renderizar la plantilla HTML con el contexto proporcionado, generando así el contenido de la respuesta.
    """
    myDict = dict(request.POST)
    myDict.pop('csrfmiddlewaretoken')
    listMetrics = assetsUtil.get_assets()

    list_metrics = [helper.process_single_metric(metrics, myDict) for metrics in listMetrics]
    name_metrics = assetsUtil.titleTable(myDict)
    context = {
        'list_metrics': list_metrics,
        'nameColumns': name_metrics,
        'metrics': myDict
    }
    rendered_table = render_to_string('assets/showTable.html', context)
    return HttpResponse(rendered_table)


@csrf_exempt  # Deshabilita la verificación CSRF para esta vista, útil para APIs que se consumen desde fuera
@require_POST # Asegura que esta vista solo acepte solicitudes POST
def chat_view(request):
    """
    Procesa solicitudes POST para interactuar con un chatbot, recibiendo un mensaje y un activo como datos JSON.

    Esta vista espera recibir una solicitud POST con un cuerpo JSON que contiene un 'message' y un 'asset'. Intenta parsear el cuerpo de la solicitud para extraer estos valores. Si la solicitud no es válida o no contiene un mensaje, devuelve un error en formato JSON. Utiliza los datos recibidos para obtener una respuesta del chatbot mediante la función `getResponseChatGpt`, y devuelve esta respuesta en formato JSON.

    Args:
        request: Objeto HttpRequest, representa la solicitud HTTP entrante.

    Returns:
        JsonResponse: Dependiendo del resultado del procesamiento, esta función devuelve:
          - Una respuesta del chatbot en formato JSON si la solicitud es válida.
          - Un mensaje de error en formato JSON si la solicitud es inválida o faltan datos.

    Notas:
        - La anotación @csrf_exempt permite que esta vista reciba solicitudes de otros dominios eliminando la necesidad de un token CSRF.
        - La anotación @require_POST restringe esta vista a solo aceptar solicitudes POST, haciendo que otras solicitudes (GET, PUT, etc.) sean automáticamente rechazadas.
    """
    try:
        data = json.loads(request.body)
        user_message = data.get('message')
        asset = data.get('asset')
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid request"}, status=400)

    if not user_message:
        return JsonResponse({"error": "No message provided"}, status=400)

    # Obtener la respuesta del chatbot
    bot_response = getResponseChatGpt(user_message,asset)

    # Devolver la respuesta en formato JSON
    return JsonResponse({"reply": bot_response})

def find_fees(request):
  txns_receipt= alchemyUtil.txn_receipt()
  if len(txns_receipt)>0:
    context={
      'txns_reciept':txns_receipt
    }
  else:
     context={
      'msj': "There are no transactions that exceed the amount of 100000"
    }
  # print(txns_receipt)
  return render(request, 'assets/check_fees.html',context=context)
  # return JsonResponse(context) # Return the error message as JSON

def check_fees(request):
  return render(request, 'assets/check_fees.html')