import pandas as pd
import boto3
from decimal import Decimal
import os
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


# Ruta del archivo CSV
file_path = r"C:/Users/DAVID MARTINEZ/OneDrive/Desktop/maestria/00 Bases de datos de nueva generacion/Trabajos/Tarea Final Grupal/OrdenesConClientes.csv"

# Leer archivo CSV
ordenes_df = pd.read_csv(file_path, encoding='latin1', delimiter=';').fillna(0)

# Tabla DynamoDB
ordenes_table = dynamodb.Table('Ordenes')

# Convertir valores a Decimal
def convert_to_decimal(value):
    try:
        return Decimal(str(value))
    except Exception:
        return Decimal('0')

# Insertar datos en DynamoDB
with ordenes_table.batch_writer() as batch:
    for index, row in ordenes_df.iterrows():
        try:
           batch.put_item(
    Item={
        'OrderID': str(row['Order ID']),
        'OrderDate': str(row['Order Date']),
        'ProductID': str(row['Product ID']),
        'BuyerGender': str(row['Buyer Gender']),
        'BuyerAge': convert_to_decimal(row['Buyer Age']),
        'OrderLocation': str(row['Order Location']),
        'InternationalShipping': str(row['International Shipping']),
        'SalesPrice': convert_to_decimal(row['Sales Price']),
        'ShippingCharges': convert_to_decimal(row['Shipping Charges']),
        'SalesPerUnit': convert_to_decimal(row['Sales per Unit']),
        'Quantity': convert_to_decimal(row['Quantity']),
        'TotalSales': convert_to_decimal(row['Total Sales']),
        'Rating': convert_to_decimal(row['Rating']),
        'Review': str(row['Review']),
        'ClientID': str(row['ClientID']),
        'NameClient': str(row['NameClient']),
        'Email': str(row['Email'])

    }
)


            
        except Exception as e:
            print(f"Error en fila {index}: {e}")

print("Órdenes agregadas exitosamente.")
