import boto3

# Especificar la región y las claves de acceso AWS
aws_region = 'eu-west-3'
aws_access_key_id = ''
aws_secret_access_key = ''
 
# Crear un cliente de DynamoDB con la región y claves especificadas
client = boto3.client(
    'dynamodb',
    region_name=aws_region,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)
 
# Crear un recurso de DynamoDB con la región y claves especificadas
dynamodb = boto3.resource(
    'dynamodb',
    region_name=aws_region,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

Ordenes = dynamodb.Table('Ordenes') 

from boto3.dynamodb.conditions import Key

# Definir rango de fechas
fecha_inicio = "01-01-2024"  #  Fecha de inicio (YYYY-MM-DD)
fecha_fin = "31-01-2024"     #  Fecha de fin (YYYY-MM-DD)

# Consulta para obtener órdenes en el rango de fechas
response = Ordenes.scan(
    FilterExpression=Key('OrderDate').between(fecha_inicio, fecha_fin)  # Filtra por fecha
)

# Contar la cantidad de órdenes en el rango
cantidad_ordenes = len(response['Items'])

# Mostrar resultado
print(f"Total de órdenes entre {fecha_inicio} y {fecha_fin}: {cantidad_ordenes}")
