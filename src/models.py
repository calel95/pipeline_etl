#representacao do banco de dados
from sqlalchemy import Column, Integer, String, DateTime, Select
from sqlalchemy.sql import func
from db import Base

class servidoresPorOrgao(Base):
    __tablename__ = 'servidoresPorOrgao'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    #created_at = Column(DateTime, default=func.now()) #Campo adicionado por mim, ele nao vem na API, campo de controle