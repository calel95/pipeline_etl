#representacao de como meus dados vao vir da api, SCHEMA OU VIEW
from pydantic import BaseModel,ConfigDict
from typing import Optional

class ServidorePoOrgaoSchema(BaseModel): #View da minha API, schema de dados
    nome: str

    #model_config = ConfigDict(from_attributes=True)
    class Config:
        from_attributes = True

class ServidoresPorOrgaoSchema(BaseModel):
    tipo_servidor: Optional[int] = None
    situacao_servidor: Optional[int] = None
    codigo_orga: Optional[int] = None

    class Config:
        from_attributes = True