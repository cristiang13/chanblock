
from datetime import datetime
from pymongo import MongoClient
from datetime import datetime, timedelta
import pymongo.errors
from chanblockweb.settings.base import env
import os

class VaraDBManager:
    def __init__(self):
        """
        Initializes the VaraDBManager with a MongoDB database instance.
        """
        # Connection to the MongoDB instance
        # client = MongoClient(os.getenv('MONGOATLAS_VARA'))
        client = MongoClient(env('MONGOATLAS_VARA'))

        self.db = client.VaraNetwork  # Connection to the 'coinmetrics' database
    
    def get_blockDetails_events(self):
        """
        Recupera todos los eventos relacionados con los detalles de los bloques de la colección 'vara'.

        Esta función consulta la base de datos para obtener todos los documentos en la colección 'vara', 
        seleccionando específicamente los campos 'blockDetails' y 'events' de cada documento. Estos campos 
        incluyen información detallada sobre los bloques y los eventos asociados, respectivamente.

        Returns:
            Una lista de diccionarios, donde cada diccionario representa un documento de la colección 'vara',
            conteniendo únicamente la información de 'blockDetails' y 'events'. La información de identificación
            del documento ('_id') es excluida de los resultados para limpieza y simplicidad de los datos retornados.

        Nota:
            - Esta función es útil para obtener una visión general de los eventos de bloque sin cargar con información
            adicional no solicitada.
        """
        # Actualiza esta línea para incluir la lógica adecuada
        return list(self.db.vara.find({}, {'_id': 0, 'blockDetails': 1, 'events': 1}))
    
    def get_last_three_documents(self):
        """
        Obtiene los últimos tres documentos de la colección 'vara', basándose en su orden de inserción.

        Esta función realiza una consulta a la base de datos para encontrar los tres documentos más recientes
        en la colección 'vara'. Los documentos se ordenan de manera descendente utilizando el campo '_id',
        que en MongoDB típicamente refleja el orden de inserción debido a su componente de timestamp.

        Returns:
            Una lista de los tres documentos más recientes de la colección, excluyendo su campo '_id' para 
            simplificar los datos retornados. Si la colección contiene menos de tres documentos, la función
            retornará todos los documentos disponibles.

        Nota:
            - La suposición de ordenación por '_id' para determinar los documentos "más recientes" se basa en
            la convención de MongoDB de incluir un timestamp en este campo. Si la colección utiliza una
            estrategia de ordenación diferente para determinar la "recencia", esta función necesitará ajustes.
        """
        # Suponiendo que quieres ordenar por un campo de marca de tiempo. Si no existe, puedes usar '_id'.
        # -1 en sort() indica orden descendente
        return list(self.db.vara.find({}, {'_id': 0}).sort('_id', -1).limit(3))
    
    def get_blockDetails_events_24h1(self):
        try:
            # Obtén la fecha y hora actuales
            now = datetime.now()

            # Calcula la marca de tiempo para 24 horas atrás
            timestamp_24h_ago = f"{(now - timedelta(days=1)).timestamp() * 1000:,.0f}"

            
            # Filtra los documentos que tienen un campo 'now' mayor que el timestamp calculado
            query = {"blockDetails.block.extrinsics.0.method.args.now": {"$gte": str(timestamp_24h_ago)}, "averageGasLimit": {"$exists": True}}
            # projection = {'_id': 0, 'blockDetails': 1, 'events': 1}
            projection = {'_id': 0, 'blockDetails': 1, 'averageGasLimit': 1, 'events':1}
            

            return list(self.db.vara.find(query, projection))
        except pymongo.errors.PyMongoError as e:
            print(f"Error al obtener datos de la base de datos: {e}")
            return []
    
    def get_blockDetails_events_24h_every_10min(self):
        """
        Recupera eventos de detalles de bloques de las últimas 24 horas, filtrando para mantener un registro cada 10 minutos.

        Esta función consulta la base de datos para eventos de detalles de bloques ocurridos en las últimas 24 horas,
        asegurándose de que solo se incluyan aquellos documentos que contengan un 'averageGasLimit' y una 'cantidadTxns'
        definidos. Luego, filtra estos documentos para mantener solamente uno cada 10 minutos, basándose en el timestamp
        especificado dentro de los argumentos del método del primer extrínseco de cada bloque.

        Returns:
            Una lista de documentos filtrados, cada uno representando los detalles de un bloque específico junto con
            información adicional como el límite promedio de gas y la cantidad de transacciones. Si se produce un error
            al consultar la base de datos, se devuelve una lista vacía.

        Raises:
            PyMongoError: Si ocurre un error al realizar la consulta en la base de datos.

        Notas:
            - La función calcula el timestamp de 24 horas atrás desde el momento actual y lo utiliza para filtrar los documentos.
            - Se utiliza un formato de timestamp en milisegundos para la comparación.
            - La selección de documentos cada 10 minutos ayuda a reducir la cantidad de datos a procesar y enviar,
            optimizando el rendimiento y la relevancia de la información presentada.
        """
        try:
            now = datetime.now()
            timestamp_24h_ago = f"{(now - timedelta(days=1)).timestamp() * 1000:,.0f}"
            
            query = {"blockDetails.block.extrinsics.0.method.args.now": {"$gte": str(timestamp_24h_ago)}, "averageGasLimit": {"$exists": True},"cantidadTxns": {"$exists": True}}
            projection = {'_id': 0, 'blockDetails': 1, 'averageGasLimit': 1, 'cantidadTxns': 1}
            
            all_documents = list(self.db.vara.find(query, projection))

            # Filtrar los documentos para mantener uno cada 10 minutos
            filtered_documents = []
            last_selected_timestamp = 0
            for doc in all_documents:
                doc_timestamp = int(doc["blockDetails"]["block"]["extrinsics"][0]["method"]["args"]["now"].replace(',', ''))
                if doc_timestamp >= last_selected_timestamp + 600000:  # 10 minutos en milisegundos
                    filtered_documents.append(doc)
                    last_selected_timestamp = doc_timestamp

            return filtered_documents
        except pymongo.errors.PyMongoError as e:
            print(f"Error al obtener datos de la base de datos: {e}")
            return []
    
    def get_last_price_usd(self):
        """
        Retorna el último documento de la colección con respecto al campo 'priceUSD'.
        """
        # Suponiendo que cada documento tiene un campo de marca de tiempo o un identificador único que 
        # se puede usar para ordenar los documentos de manera descendente.
        # Si no hay un campo de marca de tiempo específico, se puede usar '_id'.
        # -1 en sort() indica orden descendente.
        # Se usa limit(1) para obtener solo el último documento.
        last_document = self.db.priceVaraUSD.find({}, {'_id': 0, 'priceUSD': 1}).sort('_id', -1).limit(1)

        return list(last_document)


        