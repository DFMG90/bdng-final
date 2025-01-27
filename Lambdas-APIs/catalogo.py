import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import io
from io import StringIO

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):

    http_res = compose_response(queryDynamo("HistOrd"))
    return http_res


def compose_response(body):
    http_res = {}

    http_res['statusCode'] = 200
    http_res['headers'] = {}
    http_res['headers']['Content-Type'] = "application/json"
    http_res['body'] = json.dumps(body)

    return http_res

def compose_body(queryResults):
    res_body = {}



    return res_body

def queryDynamo(queryType, cliente = "", orden = ""):
    queryResults = list()

    ordenes = dynamodb.Table('Ordenes')
    productos = dynamodb.Table('Productos')

    match queryType:
        case "AllItems":

            response = productos.scan(
                FilterExpression = Attr('Categoria').eq('Prenda')
            )

            queryResults = response['Items']

        case "TopItems": 
            responses = {}

        case "HistOrd":

            clienteID = 396566981

            cliResponse = ordenes.scan(
                ProjectionExpression = 'Cliente[1]',
                FilterExpression = Attr('Cliente').contains(clienteID)
            )
            cliNom = cliResponse['Items'][0]
            cliNom['Cliente'] = cliNom['Cliente'][0]

            response = ordenes.scan(
                ProjectionExpression = 'OrdenID, Producto[0]',
                FilterExpression = Attr('Cliente').contains(clienteID)
            )

            item = response['Items']

            for i in range(len(item)):
                productID = str(item[i]['Producto'][0])

                response = productos.query(
                    #ProjectionExpression = 'Producto, Categoria, Descripcion, imgURL',
                    KeyConditionExpression = Key('ProductID').eq(productID)
                )

                item[i]['ProductoDetalles'] = response['Items'][0]
            
            item.insert(0, cliNom)

            queryResults = item



    return queryResults
