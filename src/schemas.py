#representacao de como meus dados vao vir da api, SCHEMA OU VIEW
from pydantic import BaseModel,ConfigDict
from typing import Optional

class a(BaseModel): #View da minha API, schema de dados
    nome: str

    #model_config = ConfigDict(from_attributes=True)
    class Config:
        from_attributes = True

class ServidoresPorOrgaoSchema(BaseModel):
    id: int
    nome_servidor: str
    codigo_orgao_servidor_lotacao: int
    nome_orgao_servidor: str
    tipo_servidor: str

    class Config:
        from_attributes = True