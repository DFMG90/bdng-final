# bdng-final
[David M.](https://github.com/DFMG90), [Elizabeth E.](https://github.com/EliJohana7), Izzy D.

---

Presentamos un proyect de ETL utilizando DynamoDB como base de datos y AWS como plataforma de hosting elaborado para la clase Bases de Datos de Nueva Generación del Master en Big Data de la Universidad Europea de Madrid. 

Servimos los datos a una pagina web y utilizamos Collaborative Filtering para dar recomendaciones a los clientes. Para una explicación del proyecto en general ver la presentación `BDNG proyecto gurpal.pdf`.

## Cargando las tablas
Para cargar las tablas es necesario conectarse a AWS y crear las tablas `productos` y `Ordenes` en DynamoDB. **El notebook `ETL/CrearDynamo.ipynb` es solo informativo.** Para cargar las tablas utilizar los scripts `ETL/insertarOrdenes.py` y `ETL/insertarProductos.py`. Es necesario proporcionar credenciales AWS en duro o atraves de Environment Variables.

## API 

Para utilizar el API, crear un api gateway y conectarlo a una función lambda de AWS que contenga el codigo en `Lambdas-APIs/catalogo.py`. Es necesario tener una capa con Pandas y Numpy, al igual que insertar un link valido a los csv necesarios (encontrados en `Data/`).

- `/?query=AllItems` - Proporciona todos los productos en el catalogo.
- `/?query=Rec&CLI=<ClientID>` - Proporciona las recomendaciones para el cliente correspondiente. Remplazar `<ClienteID>` con un ID de Cliente valido (todos los ID de clientes se encuentran en `Data/MOCK_CLIENTES.csv`)
-  `/?query=HistOrd&CLI=<ClientID>` - Proporciona todas las compras pasada para el cliente correspondiente.
- `/?CLI=<ClientID>&PR=<ProductID>&RATING=3.0` - Inserta el rating para el producto indicado por el cliente indicado en la tabla de ordenes. **NO IMPLEMENTADO ACTUALMENTE**

## Web
Para poder visualizar la pagina web es necesario activar el servidor demo de CORS para esa *unica* sesión. Se puede hacer en https://cors-anywhere.herokuapp.com/corsdemo.  
Los usuarios para acceder a la web son:
- username: usuario1 -- password: password1
- username: usuario2 -- password: password2
- username: usuario3 -- password: password3

---

# Referencias
- Datos: Adarsh Anil Kumar via Kaggle; Datos sinteticos de Mockaro