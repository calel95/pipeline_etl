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

#df = a.orgaos_siape(2)
#print(df)

a.servidores_por_orgao(2,1,16000)