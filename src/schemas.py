#representacao de como meus dados vao vir da api, SCHEMA OU VIEW
from pydantic import BaseModel,ConfigDict
from typing import Optional

class OrgaosSiapeSchema(BaseModel): #View da minha API, schema de dados
    qnt_pessoas: int
    descricao_situacao: str
    descricao_tipo_vinculo: str
    descricao_tipo_servidor: str
    codigo_orgao_exercicio_siape: int
    nome_orgao_exercicio_siape: str

    #model_config = ConfigDict(from_attributes=True)
    class Config:
        from_attributes = True

class ServidoresPorOrgaoSchema(BaseModel):
    id: int
    nome_servidor: str
    codigo_orgao_servidor_lotacao: int
    nome_orgao_servidor: str
    tipo_servidor: str
    cargo: str

    class Config:
        from_attributes = True

class ServidorRemuneracaoSchema(BaseModel):
    id_servidor: int
    nome_servidor: str
    situacao: str
    codigo_orgao_servidor_lotacao: int
    orgao_servidor_lotacao: str
    mes_ano: str
    remuneracao_liquida: float
    remuneracao_bruta: float

    class Config:
        from_attributes = True