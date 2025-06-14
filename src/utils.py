import os
import csv
import zipfile
import pandas as pd
import datetime
import requests
from dotenv import load_dotenv
from db import SessionLocal, engine, Base
from models import servidoresPorOrgao
from schemas import ServidorePoOrgaoSchema

Base.metadata.create_all(bind=engine)

class Util:
    def __init__(self):
        pass

    def zip_extract(self,file: str):
        
        path_origin = f"data/origin/{file}"
        myzip = zipfile.ZipFile(path_origin)
        myzip.extractall(f"data/raw/{datetime.datetime.now().strftime('%Y%m%d_%H_%M_%S')}")
        print(f"Arquivo {file} extraído com sucesso na raw.")

    def bolsa_familia_por_municipio(self, ano_mes: str, codigo_ibge: int):
        """
        Esta função faz uma requisição à API do Portal da Transparência para obter o valor total e a quantidade de beneficiados no Bolsa Família por município em um determinado mês e ano.

        Args:
            ano_mes (str): Formato 'YYYYMM', por exemplo, '202501' para janeiro de 2025.
            codigo_ibge (int): Código IBGE do município, por exemplo, 3300258 para o município de ARRAIAL DO CABO.
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
    
    def orgaos_siape(self,tipo_servidor: int):
        """
        Esta função faz uma requisição à API do Portal da Transparência para obter informações sobre órgãos do SIAPE.
        Args:
            tipo_servidor (str): Tipo de servidor, por exemplo, 1 para servidores civis e 2 para militares.
        """


        url = f'https://api.portaldatransparencia.gov.br/api-de-dados/servidores/por-orgao?tipoServidor={tipo_servidor}&pagina=1'
        load_dotenv('.env')
        headers = {os.getenv('API_PORTAL_DA_TRANSPARENCIA_KEY'): os.getenv('API_PORTAL_DA_TRANSPARENCIA_TOKEN')}
        response = requests.get(url,headers=headers)
        data = response.json()
        #print(data)

        df_lista = []

        for item in data:
            registro = {
                'qnt_pessoas': item['qntPessoas'],
                'descricao_situacao': item['descSituacao'],
                'descricao_tipo_vinculo': item['descTipoVinculo'],
                'descricao_tipo_servidor': item['descTipoServidor'],
                'codigo_orgao_exercicio_siape': item['codOrgaoExercicioSiape'],
                'nome_orgao_exercicio_siape': item['nomOrgaoExercicioSiape']
            }
            df_lista.append(registro)


            # df = pd.DataFrame({
            # 'qnt_pessoas': [qnt_pessoas],
            # 'descricao_situacao': [descricao_situacao],
            # 'descricao_tipo_vinculo': [descricao_tipo_vinculo],
            # 'descricao_tipo_servidor': [descricao_tipo_servidor],
            # 'codigo_orgao_exercicio_siape': [codigo_orgao_exercicio_siape],	
            # 'nome_orgao_exercicio_siape': [nome_orgao_exercicio_siape]
            # })
            #df = pd.DataFrame(item, columns=['qntPessoas','descSituacao','descTipoVinculo','descTipoServidor','codOrgaoExercicioSiape','nomOrgaoExercicioSiape'], index=[0])

        df = pd.DataFrame(df_lista)
        #print(df)
        return df
    
    def servidores_por_orgao(self, tipo_servidor: int, situacao_servidor: int, codigo_orgao: int,salvar: bool = False):
        """Faz uma requisição para obter informações sobre quantidade de servidores de um órgão específico, situacao especifica e tipo do servidor especifico.

        Args:
            tipo_servidor (int): Tipo do Servidor (Civil=1 ou Militar=2)
            situacao_servidor (int): Situação do Servidor (Ativo=1, Inativo=2 ou Pensionista=3)
            codigo_orgao (int): Código do Órgão do SIAPE, por exemplo, 16000 para o comando do exército.
        """

        url = f'https://api.portaldatransparencia.gov.br/api-de-dados/servidores?tipoServidor={tipo_servidor}&situacaoServidor={situacao_servidor}&orgaoServidorExercicio={codigo_orgao}&pagina=1'
        load_dotenv('.env')
        headers = {os.getenv('API_PORTAL_DA_TRANSPARENCIA_KEY'): os.getenv('API_PORTAL_DA_TRANSPARENCIA_TOKEN')}
        response = requests.get(url,headers=headers)
        data = response.json()
        #print(data)
        with SessionLocal() as db:
            for i in data:
                id =i["servidor"]["idServidorAposentadoPensionista"]
                nome_servidor =  i['servidor']['pessoa']['nome']
                codigo_orgao_servidor_lotacao =  i['servidor']['orgaoServidorLotacao']['codigo']
                nome_orgao_servidor = i['servidor']['orgaoServidorLotacao']['nome']
                tipo_servidor = i['servidor']['tipoServidor']
                
                #lista.append(ServidorePoOrgaoSchema(nome=nome_servidor))
                db.add(servidoresPorOrgao(id=id, 
                                          nome=nome_servidor,
                                          codigo_orgao_servidor_lotacao=codigo_orgao_servidor_lotacao,
                                          nome_orgao_servidor=nome_orgao_servidor,
                                          tipo_servidor=tipo_servidor))
            db.commit()


        