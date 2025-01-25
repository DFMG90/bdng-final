import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import io
from io import StringIO

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    productos = dynamodb.Table('Productos')

    http_res = compose_response(queryDynamo(productos, "AllItems"))
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
    for i in range(len(queryResults) -1):
        item = queryResults[i]
        ID = item['ProductID']
        res_body[ID] = {}
        
        preDump = {}

        preDump['ID'] = item['ProductID']
        preDump['producto'] = item['Producto']
        preDump['Categoria'] = item['Categoria']
        preDump['Descripcion'] = item['Descripcion']
        preDump['imgURL'] = item['imgURL']

        res_body[ID] = json.dumps(preDump)

    return res_body

def queryDynamo(tabla, queryType):
    queryResults = list()

    match queryType:
        case "AllItems":
            response = tabla.scan(
                FilterExpression = Attr('Categoria').eq('Prenda')
            )

            queryResults = response['Items']

        case "TopItems": 
            responses = {}

    return queryResults
