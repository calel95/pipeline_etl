import os
import csv
import zipfile
import pandas as pd
from utils import Util
import datetime


#a = Util()
#a.zip_extract("202501_Militares.zip")

a = Util()
#a.bolsa_familia_por_municipio_request_api("202501", 4314902)

#x = a.codigo_ibge_por_municipio("sapucaia do sul")
#a.bolsa_familia_por_municipio("202501", x)

#df = a.orgaos_siape(tipo_servidor=1,salvar_bd=True, merge=False)
#print(df)

# xx = a.servidores_por_orgao(tpo_servidor=1,situacao_servidor=1,codigo_orgao=70000,salvar_bd=True, merge=False)

# for i in xx:
#     #print(i)
#     a.servidor_remuneracao(id_servidor=i,ano_mes=202501, salvar_bd=True)
a.servidor_remuneracao(id_servidor=622109,ano_mes=202501, salvar_bd=True)

#a.servidores_por_orgao(tpo_servidor=1,situacao_servidor=1,codigo_orgao=70000,salvar_bd=False, merge=False)

#VERIFICAR O ID CIVIL 622109 QUE NAO TRAZ O CAMPO DE remuneracoesDTO, AJUSTAR O CODIGO PARA NAO QUEBRAR