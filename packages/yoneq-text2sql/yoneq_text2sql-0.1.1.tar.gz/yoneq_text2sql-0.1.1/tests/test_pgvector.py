import os

from dotenv import load_dotenv

# from text2sql.pgvector import PG_VectorStore
# from text2sql.openai import OpenAI_Chat

# assume .env file placed next to file with provided env vars
load_dotenv()

# def get_text2sql_connection_string():
#     server = os.environ.get("PG_SERVER")
#     driver = "psycopg"
#     port = os.environ.get("PG_PORT", 5432)
#     database = os.environ.get("PG_DATABASE")
#     username = os.environ.get("PG_USERNAME")
#     password = os.environ.get("PG_PASSWORD")

# def test_pgvector_e2e():
#     # configure Text2Sql to use OpenAI and PGVector
#     class Text2SqlCustom(PG_VectorStore, OpenAI_Chat):
#         def __init__(self, config=None):
#             PG_VectorStore.__init__(self, config=config)
#             OpenAI_Chat.__init__(self, config=config)
    
#     t2s = Text2SqlCustom(config={
#         'api_key': os.environ['OPENAI_API_KEY'],
#         'model': 'gpt-3.5-turbo',
#         "connection_string": get_text2sql_connection_string(),
#     })

#     # connect to SQLite database
#     t2s.connect_to_sqlite('https://storage.yandexcloud.net/yoneq-ai/Chinook.sqlite')

#     # train Text2Sql on DDLs
#     df_ddl = t2s.run_sql("SELECT type, sql FROM sqlite_master WHERE sql is not null")
#     for ddl in df_ddl['sql'].to_list():
#         t2s.train(ddl=ddl)
#     assert len(t2s.get_related_ddl("dummy question")) == 10  # assume 10 DDL chunks are retrieved by default
    
#     question = "What are the top 7 customers by sales?"
#     sql = t2s.generate_sql(question)
#     df = t2s.run_sql(sql)
#     assert len(df) == 7

#     # test if Text2Sql can generate an answer
#     answer = t2s.ask(question)
#     assert answer is not None

