## Produces a list with the set amount of recommendations for the user!!

import pandas as pd
import numpy as np
from numpy.linalg import svd
import os
#from scipy.sparse.linalg import svds

R_df = pd.read_csv("..\..\Data Sets\matrix_ratings.csv")
Clientes = R_df['ClientID']
R_df.set_index('ClientID', inplace=True)

R = R_df.to_numpy()
ratingsMean = np.mean(R, axis=1)
R_demeaned = R - ratingsMean.reshape(-1, 1)


U, sigma, Vt = svd(R_demeaned, full_matrices=False)
sigma = np.diag(sigma)

allUserRecs = np.dot(np.dot(U, sigma), Vt) + ratingsMean.reshape(-1, 1)
recsDF = pd.DataFrame(allUserRecs, columns= R_df.columns)
recsDF.insert(loc=0, column='ClientID', value = Clientes)
recsDF.set_index('ClientID', inplace=True)

recsDF.to_csv('..\..\Data Sets\matrix_rec.csv')

#### printing some predicitons!!!

histComp_df = pd.read_csv("..\..\Data Sets\matrix_histCompras.csv")
histComp_df.set_index('ClientID', inplace=True)

allProductIDs = recsDF.columns.to_list()

for prod in allProductIDs:
    recsDF[prod] = recsDF[prod].mask(histComp_df[prod] == False, -1000)

valInput = False
os.system('cls')
while valInput == False:
    userInput = input("Insertar numero de cliente: ")
    try:
        target = int(userInput)
        valInput = True
    except:
        print("Numero de cliente debe contener solo numeros.")


recCount = int(input("Cuantas recomendaciones desea? "))
prodScores = recsDF.loc[target]

topRecs = prodScores.sort_values(ascending=False).head(recCount).index.to_list()
print(f"Para cliente: {target} las recomendaciones son: ", topRecs)

