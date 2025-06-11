import os
import csv
import zipfile
import pandas as pd
import datetime
import requests
from requests.auth import HTTPDigestAuth
from dotenv import load_dotenv


class Util:
    def __init__(self):
        pass

    def zip_extract(self,file: str):
        
        path_origin = f"data/origin/{file}"
        myzip = zipfile.ZipFile(path_origin)
        myzip.extractall(f"data/raw/{datetime.datetime.now().strftime('%Y%m%d_%H_%M_%S')}")
        print(f"Arquivo {file} extraído com sucesso na raw.")

    def bolsa_familia_por_municipio_request_api(self, ano_mes: str, codigo_ibge: int):
        """
        Esta função faz uma requisição à API do Portal da Transparência para obter o valor total e a quantidade de beneficiados no Bolsa Família por município em um determinado mês e ano.

        Args:
            ano_mes (str): Formato 'YYYYMM', por exemplo, '202501' para janeiro de 2025.
            codigo_ibge (str): Código IBGE do município, por exemplo, '3300258' para o município de ARRAIAL DO CABO.
        """
        url = f'https://api.portaldatransparencia.gov.br/api-de-dados/novo-bolsa-familia-por-municipio?mesAno={ano_mes}&codigoIbge={codigo_ibge}&pagina=1'
        load_dotenv('.env')
        headers = {os.getenv('API_PORTAL_DA_TRANSPARENCIA_KEY'): os.getenv('API_PORTAL_DA_TRANSPARENCIA_TOKEN')}
        response = requests.get(url,headers=headers)
        data = response.json()
        #print(data)

        municipio = data[0]['municipio']['nomeIBGE']
        uf = data[0]['municipio']['uf']['sigla']
        valor = data[0]['valor']
        quantidade_beneficiados = data[0]['quantidadeBeneficiados']
        print(municipio)
        print(uf)
        print(valor)
        print(quantidade_beneficiados)

        # Cria um DataFrame com os dados
        df = pd.DataFrame({
            'municipio': [municipio],
            'uf': [uf],
            'valor': [valor],
            'quantidade_beneficiados': [quantidade_beneficiados]
        })
        print(df)
        return df

    def codigo_ibge_por_municipio(self, municipio: str):
        """
        Esta função recebe o nome de um município e retorna o código IBGE correspondente.

        Args:
            municipio (str): Nome do município, por exemplo, 'ARACAJU'.

        Returns:
            str: Código IBGE do município.
        """
        url = f'https://servicodados.ibge.gov.br/api/v1/localidades/municipios?orderBy=nome'
        response = requests.get(url)
        data = response.json()
        #print(data)

        for item in data:
            if item['nome'].upper() == municipio.upper():
                codigo_ibge = item['id']
                print(f"Código IBGE de {municipio.upper()}: {codigo_ibge}")
        
        return codigo_ibge
    

