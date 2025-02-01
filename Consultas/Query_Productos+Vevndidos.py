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


# Escanear la tabla para obtener Product ID y Quantity
response = Ordenes.scan(
    ProjectionExpression="ProductID, Quantity"
)

# Diccionario para almacenar el total vendido por producto
ventas_por_producto = defaultdict(Decimal)

# Sumar la cantidad vendida de cada producto
for item in response['Items']:
    product_id = item['ProductID']  # ID del producto
    quantity = Decimal(item['Quantity'])  # Convertir a número decimal
    ventas_por_producto[product_id] += quantity  # Sumar la cantidad vendida

# Ordenar los productos por cantidad vendida (de mayor a menor)
productos_ordenados = sorted(ventas_por_producto.items(), key=lambda x: x[1], reverse=True)

# Mostrar los productos más vendidos
print("Productos más vendidos:")
for product, total in productos_ordenados[:10]:  # Mostrar solo los 10 primeros
    print(f"Producto {product}: {total} unidades vendidas")
