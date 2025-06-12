#representacao de como meus dados vao vir da api, SCHEMA OU VIEW
from pydantic import BaseModel,ConfigDict

class ServidorePoOrgaoSchema(BaseModel): #View da minha API, schema de dados
    nome: str

    #model_config = ConfigDict(from_attributes=True)
    class Config:
        from_attributes = True