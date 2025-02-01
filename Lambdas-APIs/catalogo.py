import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import io
from io import StringIO
from decimal import Decimal

import pandas as pd
import numpy as np
from numpy.linalg import svd

class DecimalEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return float(obj)
    return json.JSONEncoder.default(self, obj)

dynamodb = boto3.resource('dynamodb')
s3 = boto3.resource('s3')

def lambda_handler(event, context):

    queryType = event['queryStringParameters']['query']

    try:
        cli = event['queryStringParameters']['CLI']
    except:
        cli = False

    if cli:
        http_res = compose_response(queryDynamo(queryType, cliente=cli))
    else: 
        http_res = compose_response(queryDynamo(queryType))

    return http_res


def compose_response(body):
    http_res = {}

    http_res['statusCode'] = 200
    http_res['headers'] = {}
    http_res['headers']['Content-Type'] = "application/json"
    http_res['body'] = json.dumps(body, cls=DecimalEncoder)

    return http_res

def compose_body(queryResults):
    res_body = {}



    return res_body

def queryDynamo(queryType, cliente = "396566981", orden = ""):
    queryResults = list()

    ordenes = dynamodb.Table('Ordenes')
    productos = dynamodb.Table('productos')

    match queryType:
        case "AllItems": # todos los productos

            response = productos.scan()

            queryResults = response['Items']

        case "Rec": # productos recomendados para cliente especifico
            item = list()
            productosRecomm = genRecs(int(cliente))
            for i in range(len(productosRecomm)):
                prod = productosRecomm[i]
                response = productos.query(
                    KeyConditionExpression = Key('ProductID').eq(prod)
                )
                item.append(response['Items'][0])       

            queryResults = item

        case "HistOrd": # historial de compras para cliente especifico
            cliResponse = ordenes.scan(
                ProjectionExpression = 'NameClient',
                FilterExpression = Attr('ClientID').contains(cliente)
            )
            cliNom = cliResponse['Items'][0]
            print(cliNom)

            response = ordenes.scan(
                ProjectionExpression = 'OrderID, ProductID',
                FilterExpression = Attr('ClientID').eq(cliente)
            )

            item = response['Items']

            for i in range(len(item)):
                productID = str(item[i]['ProductID'])

                response = productos.query(
                    #ProjectionExpression = 'Producto, Categoria, Descripcion, imgURL',
                    KeyConditionExpression = Key('ProductID').eq(productID)
                )

                item[i]['ProductoDetalles'] = response['Items'][0]
            
            item.insert(0, cliNom)

            queryResults = item



    return queryResults

def genRecs(cliente=396566981, recCount = 5):

    # loading into dataframe
    R_df = pd.read_csv("https://datos-izzyshop.s3.eu-west-3.amazonaws.com/matrix_ratings.csv") ## Data/matrix_ratings.csv
    Clientes = R_df['ClientID']
    R_df.set_index('ClientID', inplace=True)

    # converting to matrix, demeaning, and performing singular value decomposition
    R = R_df.to_numpy()
    ratingsMean = np.mean(R, axis = 1)
    R_demeaned = R - ratingsMean.reshape(-1, 1)

    U, sigma, Vt = svd(R_demeaned, full_matrices=False)
    sigma = np.diag(sigma)

    # generating list of all products
    allProductIDs = R_df.columns.to_list()
    print(allProductIDs)
    # generating and saving recommendation csv
    allUserRecs = np.dot(np.dot(U, sigma), Vt) + ratingsMean.reshape(-1, 1)
    recsDF = pd.DataFrame(allUserRecs, columns= R_df.columns)
    recsDF.insert(loc=0, column='ClientID', value=Clientes)
    recsDF.set_index('ClientID', inplace=True)

    # making some predictions

    ## ignoring products the user has already bought
    print("opening hist")


    histComp_df = pd.read_csv("https://datos-izzyshop.s3.eu-west-3.amazonaws.com/matrix_histCompras.csv") # Data/matrix_histCompras.csv
    histComp_df.set_index('ClientID', inplace=True)

    for prod in allProductIDs:
        recsDF[prod] = recsDF[prod].mask(histComp_df[prod] == False, -1000)

    ## getting all predictions for a user
    prodScores = recsDF.loc[cliente]

    ## getting top n recs for a user
    topRecs = prodScores.sort_values(ascending=False).head(recCount).index.to_list()

    return topRecs
