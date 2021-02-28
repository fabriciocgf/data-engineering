import pandas as pd
import json
from sqlalchemy import create_engine, Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import pymysql
from tqdm import tqdm

# Lendo dados
file = open('logs_1.txt', 'r')
json_list_1 = file.readlines()
file.close()
file = open('logs_2.txt', 'r')
json_list_2 = file.readlines()
file.close()
json_list = json_list_1 + json_list_2
print('Extraindo Dados de logs')

# Extraindo dados relevantes
df = pd.DataFrame(columns=['consumer_id', 'service_id', 'proxy', 'kong', 'request', 'host', 'name', 'request_host'])
serie_list = []
for json_str in json_list:
    data = json.loads(json_str)
    serie = {
        'consumer_id': data["authenticated_entity"]["consumer_id"]["uuid"],
        'service_id': data["service"]["id"],
        'proxy': data["latencies"]["proxy"],
        'kong': data["latencies"]["kong"],
        'request': data["latencies"]["request"],
        'host': data["service"]["host"],
        'name': data["service"]["name"],
        'request_host': data["request"]["headers"]["host"]
    }
    serie_list.append(serie)

df = df.append(serie_list, ignore_index=True)
df.index += 1

# Tabela serviços
servicos = df.drop_duplicates(subset=['service_id']).reset_index(drop=True)\
.drop(['consumer_id','proxy','kong','request','request_host'], axis=1)
servicos.index += 1
servicos_map = servicos['service_id'].to_dict()
servicos_inv_map = {v: k for k, v in servicos_map.items()}

# Tabela de Consumidores
costumer = df.drop_duplicates(subset=['consumer_id']).reset_index(drop=True)\
.drop(['service_id','proxy','kong','request','host','name','request_host'], axis=1)
costumer.index += 1
costumer_map = costumer['consumer_id'].to_dict()
costumer_inv_map = {v: k for k, v in costumer_map.items()}

# Tabela de Requisições
requisicoes = df.replace({"consumer_id": costumer_inv_map, "service_id": servicos_inv_map}).drop(['host','name'], axis=1)

# Criando tabelas no sevidor
user = 'test:1234'
dbPath = 'mysql+pymysql://' + user + '@127.0.0.1:3306/test'
sqlEngine = create_engine(dbPath, pool_recycle=3600)
dbConnection = sqlEngine.connect()
Base = declarative_base()


class Consumers(Base):
    __tablename__ = "consumers"
    index = Column(Integer, Sequence('index_seq'), primary_key=True)
    consumer_id = Column(String(200))


class Services(Base):
    __tablename__ = "services"
    index = Column(Integer, Sequence('index_seq'), primary_key=True)
    service_id = Column(String(200))
    host = Column(String(100))
    name = Column(String(100))


class Requests(Base):
    __tablename__ = "requests"
    index = Column(Integer, Sequence('index_seq'), primary_key=True)
    consumer_id = Column(Integer, ForeignKey(Consumers.index))
    service_id = Column(Integer, ForeignKey(Services.index))
    proxy = Column(Integer)
    kong = Column(Integer)
    request = Column(Integer)
    request_host = Column(String(100))
    consumer = relationship('Consumers', foreign_keys='Consumers.index')
    Service = relationship('Services', foreign_keys='Services.index')


Consumers.__table__.create(bind=sqlEngine, checkfirst=True)
Services.__table__.create(bind=sqlEngine, checkfirst=True)
Requests.__table__.create(bind=sqlEngine, checkfirst=True)
dbConnection.close()

# Colocanda dados nas tabelas
try:
    sqlEngine = create_engine(dbPath, pool_recycle=3600)
    dbConnection = sqlEngine.connect()
    frame = costumer.to_sql("consumers", dbConnection, if_exists='append')
    frame = servicos.to_sql("services", dbConnection, if_exists='append')
    frame = requisicoes.to_sql("requests", dbConnection, if_exists='append');
except ValueError as vx:
    print(vx)
except Exception as ex:
    print(ex)
else:
    print("Tabelas criadas no banco");
finally:
    dbConnection.close()

# Requisições por consumidor
print('Salvando Dados de requsições por consumidor:')
sqlEngine = create_engine(dbPath, pool_recycle=3600)
dbConnection = sqlEngine.connect()
consumers = pd.read_sql_query('select * from consumers', dbConnection, index_col='index')
for consumer in tqdm(consumers.iterrows(), total=consumers.shape[0]):
    querry = 'select \
                r.index,\
                r.proxy,\
                r.kong,\
                r.request,\
                r.request_host,\
                s.service_id \
            from \
            test.requests as r \
            inner join test.services as s \
            on r.service_id = s.index \
            and r.service_id = ' + str(consumer[0])
    pd.read_sql_query(querry, dbConnection, index_col='index').to_csv('consumers/' + consumer[1][0] +'.csv')
dbConnection.close()
print('Requsições por consumidor salvas em consumers/')

# Requisições por serviço
print('Salvando Dados de requsições por serviço:')
sqlEngine = create_engine(dbPath, pool_recycle=3600)
dbConnection = sqlEngine.connect()
services = pd.read_sql_query('select * from services', dbConnection, index_col='index')
for service in tqdm(services.iterrows(), total=services.shape[0]):
    querry = 'select \
                r.index,\
                r.proxy,\
                r.kong,\
                r.request,\
                r.request_host,\
                s.service_id \
            from \
                test.requests as r \
            inner join test.services as s \
            on r.service_id = s.index \
            and r.service_id = ' + str(service[0])
    pd.read_sql_query(querry, dbConnection, index_col='index').to_csv('services/' + service[1][0] +'.csv')
dbConnection.close()
print('Requsições por serviço salvas em services/')

# Tempo médio de request, proxy e kong por serviço
sqlEngine = create_engine(dbPath, pool_recycle=3600)
dbConnection = sqlEngine.connect()
querry='select \
            avg(sd.proxy) as "proxy", \
            avg(sd.kong) as "kong", \
            avg(sd.request) as "request", \
            sd.service_id as "service_id" \
        from \
            (select \
                r.index, \
                r.proxy, \
                r.kong, \
                r.request, \
                r.request_host, \
                s.service_id \
            from \
            test.requests as r \
            inner join test.services as s on r.service_id = s.index) as sd \
        group by sd.service_id'
pd.read_sql_query(querry, dbConnection).to_csv('services/medias_por_servico.csv')
dbConnection.close()
print('Tempo médio de request, proxy e kong por serviço salvo em services/')
