import os
import csv
import zipfile
import pandas as pd
import datetime
import requests
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from db import get_engine
from models import servidoresPorOrgao, Base, OrgaosSiape, servidoresRemuneracao
from schemas import ServidoresPorOrgaoSchema, OrgaosSiapeSchema, ServidorRemuneracaoSchema

engine = get_engine("prd")  # Use the production environment
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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
        load_dotenv('.env.prd')
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
    
    def orgaos_siape(self,tipo_servidor: int, salvar_bd: bool = False, merge: bool = False):
        """
        Esta função faz uma requisição à API do Portal da Transparência para obter informações sobre órgãos do SIAPE.
        Args:
            tipo_servidor (str): Tipo de servidor, por exemplo, 1 para servidores civis e 2 para militares.
        """
        qtd_Registros = []
        df_lista = []
        pagina = 1

        while True:

            url = f'https://api.portaldatransparencia.gov.br/api-de-dados/servidores/por-orgao?tipoServidor={tipo_servidor}&pagina={pagina}'
            load_dotenv('.env.prd')
            headers = {os.getenv('API_PORTAL_DA_TRANSPARENCIA_KEY'): os.getenv('API_PORTAL_DA_TRANSPARENCIA_TOKEN')}
            response = requests.get(url,headers=headers)
            data = response.json()
            qtd_Registros.append(len(data))
            
            if not data:
                print("Não encontrado nova página.")
                break

            if salvar_bd:
                with SessionLocal() as db:
                    for i in data:
                        schema = OrgaosSiapeSchema(
                        qnt_pessoas = i['qntPessoas'],
                        descricao_situacao = i['descSituacao'],
                        descricao_tipo_vinculo = i['descTipoVinculo'],
                        descricao_tipo_servidor = i['descTipoServidor'],
                        codigo_orgao_exercicio_siape = i['codOrgaoExercicioSiape'],
                        nome_orgao_exercicio_siape = i['nomOrgaoExercicioSiape']
                        )

                        model = OrgaosSiape(
                            qnt_pessoas=schema.qnt_pessoas,
                            descricao_situacao=schema.descricao_situacao,
                            descricao_tipo_vinculo=schema.descricao_tipo_vinculo,
                            descricao_tipo_servidor=schema.descricao_tipo_servidor,
                            codigo_orgao_exercicio_siape=schema.codigo_orgao_exercicio_siape,
                            nome_orgao_exercicio_siape=schema.nome_orgao_exercicio_siape
                        )

                        # Verifica se o registro já existe, se sim, faz merge, se não, adiciona
                        if merge:
                            db.merge(model)
                        else:
                            db.add(model)
                    db.commit()
                print(f"Registros salvos na base de dados: {len(data)}")
            else:
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


                df = pd.DataFrame(df_lista)
                print(df)
            pagina = pagina + 1
        print(f"Total de registros lidos: {sum(qtd_Registros)}")
        #return df

    def servidores_por_orgao(self, tpo_servidor, situacao_servidor: int, codigo_orgao: int,salvar_bd: bool = False, merge: bool = False):
        """Faz uma requisição para obter informações sobre quantidade de servidores de um órgão específico, situacao especifica e tipo do servidor especifico.

        Args:
            tipo_servidor (int): Tipo do Servidor (Civil=1 ou Militar=2)
            situacao_servidor (int): Situação do Servidor (Ativo=1, Inativo=2 ou Pensionista=3)
            codigo_orgao (int): Código do Órgão do SIAPE, por exemplo, 16000 para o comando do exército.
        """
        lista_ids = []
        qtd_Registros = []
        lista = []
        pagina = 1
        while True:

            url = f'https://api.portaldatransparencia.gov.br/api-de-dados/servidores?tipoServidor={tpo_servidor}&situacaoServidor={situacao_servidor}&orgaoServidorExercicio={codigo_orgao}&pagina={pagina}'
            print(f"Carregando dados da pagina: {pagina}")
            load_dotenv('.env.prd')
            headers = {os.getenv('API_PORTAL_DA_TRANSPARENCIA_KEY'): os.getenv('API_PORTAL_DA_TRANSPARENCIA_TOKEN')}
            response = requests.get(url,headers=headers)
            data = response.json()
            qtd_Registros.append(len(data))
        #print(len(qtd_Registros))

            if not data:
                print("Nenhum registro encontrado.")
                break


            if salvar_bd:
                with SessionLocal() as db:
                    for i in data:
                        schema = ServidoresPorOrgaoSchema(
                            id = i["servidor"]["idServidorAposentadoPensionista"],
                            nome_servidor =  i['servidor']['pessoa']['nome'],
                            codigo_orgao_servidor_lotacao =  i['servidor']['orgaoServidorLotacao']['codigo'],
                            nome_orgao_servidor = i['servidor']['orgaoServidorLotacao']['nome'],
                            tipo_servidor = i['servidor']['tipoServidor'],
                            cargo = i['fichasMilitar'][0]['cargo']
                        )

                        model = servidoresPorOrgao(id=schema.id, 
                                                    nome_servidor=schema.nome_servidor,
                                                    codigo_orgao_servidor_lotacao=schema.codigo_orgao_servidor_lotacao,
                                                    nome_orgao_servidor=schema.nome_orgao_servidor,
                                                    tipo_servidor=schema.tipo_servidor,
                                                    cargo=schema.cargo)
                        
                        #lista_ids.append(model.id)
                        yield model.id
                        #print(lista_ids)
                        
                        if merge:
                            db.merge(model)
                        else:
                            db.add(model)
                    
                    db.commit()
                
                #print(f"Total de registros salvos no banco da pagina: {len(data)}")
            else:
                for i in data:
                    registro = {
                        'id': i["servidor"]["idServidorAposentadoPensionista"],
                        'nome_servidor': i['servidor']['pessoa']['nome'],
                        'codigo_orgao_servidor_lotacao': i['servidor']['orgaoServidorLotacao']['codigo'],
                        'nome_orgao_servidor': i['servidor']['orgaoServidorLotacao']['nome'],
                        'tipo_servidor': i['servidor']['tipoServidor'],
                        'cargo': i['fichasMilitar'][0]['cargo']
                    }
                    lista.append(registro)
                    #return registro["nome_servidor"]

                df = pd.DataFrame(lista)
                #print(df)
                return df["id"]

            pagina = pagina + 1
        print(f"Total de registros lidos: {sum(qtd_Registros)}")
        #return lista_ids

         

    def servidor_remuneracao(self, id_servidor, ano_mes: str = 202501, salvar_bd: bool = False, merge: bool = False):

        lista = []

        url = f'https://api.portaldatransparencia.gov.br/api-de-dados/servidores/remuneracao?id={id_servidor}&mesAno={ano_mes}&pagina=1'
        load_dotenv('.env.prd')
        headers = {os.getenv('API_PORTAL_DA_TRANSPARENCIA_KEY'): os.getenv('API_PORTAL_DA_TRANSPARENCIA_TOKEN')}
        response = requests.get(url,headers=headers)
        data = response.json()
        
        if not data:
            print("Nenhum registro encontrado.")
            return None

        if salvar_bd:
                with SessionLocal() as db:
                    for i in data:
                        schema = servidoresRemuneracao(
                            id_servidor = id_servidor, #i["servidor"]["idServidorAposentadoPensionista"],
                            nome_servidor = i['servidor']['pessoa']['nome'],
                            situacao = i['servidor']['situacao'],
                            codigo_orgao_servidor_lotacao = i['servidor']['orgaoServidorLotacao']['codigo'],
                            orgao_servidor_lotacao = i['servidor']['orgaoServidorLotacao']['nome'],
                            mes_ano = i['remuneracoesDTO'][0]['mesAno'],
                            remuneracao_liquida = float((i['remuneracoesDTO'][0]['valorTotalRemuneracaoAposDeducoes']).replace('.', '').replace(',', '.')),
                            remuneracao_bruta = i['remuneracoesDTO'][0]['rubricas'][0]['valor']

                        )

                        model = servidoresRemuneracao(
                                                    id_servidor=schema.id_servidor,
                                                    nome_servidor=schema.nome_servidor,
                                                    situacao=schema.situacao,
                                                    codigo_orgao_servidor_lotacao=schema.codigo_orgao_servidor_lotacao,
                                                    orgao_servidor_lotacao=schema.orgao_servidor_lotacao,
                                                    mes_ano=schema.mes_ano,
                                                    remuneracao_liquida=schema.remuneracao_liquida,
                                                    remuneracao_bruta=schema.remuneracao_bruta)
                        
                        if merge:
                            db.merge(model)
                        else:
                            db.add(model)

                    db.commit()
                print(f"Registros salvos no banco de dados: {len(data)}")
        
        for i in data:
            registro = {
                'id_servidor': id_servidor, #i["servidor"]["idServidorAposentadoPensionista"],
                'nome_servidor': i['servidor']['pessoa']['nome'],
                'situacao': i['servidor']['situacao'],
                'codigo_orgao_servidor_lotacao': i['servidor']['orgaoServidorLotacao']['codigo'],
                'orgao_servidor_lotacao': i['servidor']['orgaoServidorLotacao']['nome'],
                'mes_ano': i['remuneracoesDTO'][0]['mesAno'],
                'remuneracao_liquida': i['remuneracoesDTO'][0]['valorTotalRemuneracaoAposDeducoes'],
                'remuneracao_bruta': i['remuneracoesDTO'][0]['rubricas'][0]['valor']
            }
            lista.append(registro)

        df = pd.DataFrame(lista)
        print(df)

