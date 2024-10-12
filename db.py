from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# El engine permite a SQLAlchemy comunicarse con la base de datos
# https://docs.sqlachemy.org/en/14/core/engines.html
engine = create_engine('sqlite:///database/productos.db',
                       connect_args = {'check_same_thread': False})
# Advertencia, crear el engine no conecta inmediatamente a la base de datos solo selecciona el motor elegido
# Cuando trabajamos con paginas webs hay que agregar si o si connect_args = {'check_same_thread': False}) para con. db


# Ahora crearemos la sesion, lo que nos permite realizar transacciones dentro de la base de datos
Session = sessionmaker(bind=engine)
session = Session()

# Esta clase se encarga de mapear la info de las clases en las que hereda y
# vincular su informacion a tablas de la base de datos
Base = declarative_base()