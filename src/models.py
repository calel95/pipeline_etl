#representacao do banco de dados
from sqlalchemy import Column, Integer, String, DateTime, Select, Float, ForeignKey
from sqlalchemy.sql import func
#from db import Base
from db import Base


class servidoresPorOrgao(Base):
    __tablename__ = 'servidoresPorOrgao'
    id = Column(Integer, primary_key=True)
    nome_servidor = Column(String)
    codigo_orgao_servidor_lotacao = Column(Integer) 
    nome_orgao_servidor = Column(String)
    tipo_servidor = Column(String)
    #created_at = Column(DateTime, default=func.now()) #Campo adicionado por mim, ele nao vem na API, campo de controle

class OrgaosSiape(Base):
    __tablename__ = 'orgaosSiape'
    id = Column(Integer, primary_key=True, autoincrement=True)
    qnt_pessoas = Column(Integer)
    descricao_situacao = Column(String)
    descricao_tipo_vinculo = Column(String)
    descricao_tipo_servidor = Column(String)
    codigo_orgao_exercicio_siape = Column(Integer)
    nome_orgao_exercicio_siape = Column(String)
    #created_at = Column(DateTime, default=func.now()) #Campo adicionado por mim, ele nao vem na API, campo de controle

class servidoresRemuneracao(Base):
    __tablename__ = 'servidoresRemuneracao'
    id = Column(Integer, primary_key=True)
    id_servidor = Column(Integer, ForeignKey('servidoresPorOrgao.id'))
    id_servidor = Column(Integer)
    nome_servidor = Column(String)
    situacao = Column(String)
    codigo_orgao_servidor_lotacao = Column(Integer) 
    orgao_servidor_lotacao = Column(String)
    mes_ano = Column(String) 
    remuneracao_liquida = Column(Float)
    remuneracao_bruta = Column(Float)