from datetime import datetime

# funciones auxiliares o generales 


def format_value_based_on_variable(variable, value):
    # Formateo de fechas
    if isinstance(value, str) and value.endswith('Z'):
        return value.split('T')[0]
    
    # Formateo numérico
    if isinstance(value, (int, float)):
        thresholds = [(1_000_000_000_000, 'T'), 
                      (1_000_000_000, 'B'), 
                      (1_000_000, 'M')]
        
        for threshold, suffix in thresholds:
            if value >= threshold:
                return f"{value / threshold:.2f}{suffix}"
        return f"{value:.3f}"
    
    # Formateo basado en el nombre de la variable
    if 'usd' in variable[-3:]:
        return f"${value}"
    
    if 'percent' in variable[-7:] or 'percent' in variable[:7]:
        return f"{float(value):.2f}%"
    
    return value

def process_single_metric(metrics, myDict):
    value_metric = []
    value_metric.append(metrics['metrics']['marketcap']['rank'])
    value_metric.append(metrics['name'])

    for metric, variables in myDict.items():
        for variable in variables:
            # Inicializamos con un valor por defecto
            current_value = None 
            if variable.find('.') != -1:  # found point in variable(str)
                splitVariable = variable.split('.')
                current_value = metrics['metrics'][metric][splitVariable[0]].get(splitVariable[1], None)
            else:
                current_value = metrics['metrics'][metric].get(variable, None)
            
            if current_value is not None:
                current_value = format_value_based_on_variable(variable, current_value)
            
            value_metric.append(current_value)
    
    return value_metric

def convert_to_datetime(timestamp):
    """
    Convert a timestamp in milliseconds to a datetime object.

    :param timestamp: The timestamp in milliseconds (as a string or integer)
    :return: A datetime object
    """
    # Remove commas and convert the timestamp to integer
    timestamp = int(timestamp.replace(',', ''))

    # Convert from milliseconds to seconds
    timestamp_seconds = timestamp / 1000.0

    # Convert to datetime
    return datetime.fromtimestamp(timestamp_seconds)

