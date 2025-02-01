from collections import defaultdict
from decimal import Decimal
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


# Escanear la tabla 'Ordenes' y obtener ClientID y Total Sales
response = Ordenes.scan(
    ProjectionExpression="ClientID, NameClient, TotalSales"
)

# Procesar resultados
ventas_por_cliente = defaultdict(Decimal)  # Diccionario para almacenar sumas

for item in response['Items']:
    client_id = item['ClientID']  # ID del cliente
    total_sales = Decimal(item['TotalSales'])  # Convertir a número decimal
    ventas_por_cliente[client_id] += total_sales  # Sumar ventas

# Mostrar total de ventas por cliente
print("Total de ventas por cliente:")
for client, total in ventas_por_cliente.items():
    print(f"Cliente {client}: ${total}")