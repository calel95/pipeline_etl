import pytest
from src.db import  get_engine
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
# src/test_db.py



def test_database_connection_prd():
    engine = get_engine("prd")
    with engine.connect() as connection:
        result = connection.execute(text('select count(*) from (select count(*) from "servidoresPorOrgao") "servidoresPorOrgao" limit 1')).first()
        #value = result.fetchone()[0]
        #assert result[0] == 1, "Database connection successful."
        #assert result is not None, "Database connection successful."
        assert result[0] == 1, "Database connection successful."

# def test_database_connection_2():
#     db_prd()
#     with engine.connect() as connection:
#         result = connection.execute(text('select 1')).first()
#         #value = result.fetchone()[0]
#         #assert result[0] == 1, "Database connection successful."
#         #assert result is not None, "Database connection successful."
#         assert result[0] == 1