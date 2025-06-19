#representacao do banco de dados
from sqlalchemy import Column, Integer, String, DateTime, Select
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base
#from db import Base
from db import Base

#Base = declarative_base()

class servidoresPorOrgao(Base):
    __tablename__ = 'servidoresPorOrgao'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    codigo_orgao_servidor_lotacao = Column(String) 
    nome_orgao_servidor = Column(String)
    tipo_servidor = Column(String)
    #created_at = Column(DateTime, default=func.now()) #Campo adicionado por mim, ele nao vem na API, campo de controle