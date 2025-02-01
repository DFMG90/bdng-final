import pandas as pd
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

# Ruta del archivo
file_path = r"C:/Users/DAVID MARTINEZ/OneDrive/Desktop/maestria/00 Bases de datos de nueva generacion/Trabajos/Tarea Final Grupal/productos.csv"

# Leer el archivo CSV con el delimitador adecuado
productos_df = pd.read_csv(file_path, encoding='latin1', delimiter=';')

# Seleccionar la tabla productos
productos_table = dynamodb.Table('productos')

# Usar batch_writer para agregar ítems desde el DataFrame
with productos_table.batch_writer() as batch:
    for _, row in productos_df.iterrows():
        batch.put_item(
            Item={
                'ProductID': row['ProductID'],
                'Producto': row['Producto'],
                'urls3': row['urls3'],  
                'descripcion': row['descripcion']
            }
        )

print("Productos agregados exitosamente.")
