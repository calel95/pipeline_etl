#onde fica a regra da engine do banco de dados, configuracoes do DB
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

def get_engine(env):
    load_dotenv(f'.env.{env}', override=True)

#DATABASE_URL = 'sqlite:///./teste2.db'
    USER = os.getenv('DB_USER')
    PASSWORD = os.getenv('DB_PASSWORD')
    HOST = os.getenv('DB_HOST')
    PORT = os.getenv('DB_PORT')
    DB = os.getenv('DB_DB')

    POSTGRESQL_DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
    engine = create_engine(POSTGRESQL_DATABASE_URL)
    return engine
    
#SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=get_engine("dev"))
Base = declarative_base()



