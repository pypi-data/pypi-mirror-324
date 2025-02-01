import os

from yoneq_text2sql.anthropic.anthropic_chat import Anthropic_Chat
from yoneq_text2sql.google import GoogleGeminiChat
from yoneq_text2sql.mistral.mistral import Mistral
from yoneq_text2sql.openai.openai_chat import OpenAI_Chat
from yoneq_text2sql.qdrant import Qdrant_VectorStore

try:
    print("Trying to load .env")
    from dotenv import load_dotenv
    load_dotenv()
except Exception as e:
    print(f"Failed to load .env {e}")
    pass

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

class Text2SqlQdrant(Qdrant_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        Qdrant_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)

from qdrant_client import QdrantClient

qdrant_memory_client = QdrantClient(":memory:")

t2s_qdrant = Text2SqlQdrant(config={'client': qdrant_memory_client, 'api_key': OPENAI_API_KEY, 'model': 'gpt-3.5-turbo'})
t2s_qdrant.connect_to_sqlite('https://storage.yandexcloud.net/yoneq-ai/Chinook.sqlite')

def test_t2s_qdrant():
    df_ddl = t2s_qdrant.run_sql("SELECT type, sql FROM sqlite_master WHERE sql is not null")

    for ddl in df_ddl['sql'].to_list():
        t2s_qdrant.train(ddl=ddl)

    sql = t2s_qdrant.generate_sql("What are the top 7 customers by sales?")
    df = t2s_qdrant.run_sql(sql)
    assert len(df) == 7

from yoneq_text2sql.chromadb.chromadb_vector import ChromaDB_VectorStore
from yoneq_text2sql.openai.openai_chat import OpenAI_Chat


class MyText2Sql(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)

t2s_chroma = MyText2Sql(config={'api_key': OPENAI_API_KEY, 'model': 'gpt-3.5-turbo'})
t2s_chroma.connect_to_sqlite('https://storage.yandexcloud.net/yoneq-ai/Chinook.sqlite')

def test_t2s_chroma():
    existing_training_data = t2s_chroma.get_training_data()
    if len(existing_training_data) > 0:
        for _, training_data in existing_training_data.iterrows():
            t2s_chroma.remove_training_data(training_data['id'])

    df_ddl = t2s_chroma.run_sql("SELECT type, sql FROM sqlite_master WHERE sql is not null")

    for ddl in df_ddl['sql'].to_list():
        t2s_chroma.train(ddl=ddl)

    sql = t2s_chroma.generate_sql("What are the top 7 customers by sales?")
    df = t2s_chroma.run_sql(sql)
    assert len(df) == 7


class Text2SqlNumResults(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)

t2s_chroma_n_results = Text2SqlNumResults(config={'api_key': OPENAI_API_KEY, 'model': 'gpt-3.5-turbo', 'n_results': 1})
t2s_chroma_n_results_ddl = Text2SqlNumResults(config={'api_key': OPENAI_API_KEY, 'model': 'gpt-3.5-turbo', 'n_results_ddl': 2})
t2s_chroma_n_results_sql = Text2SqlNumResults(config={'api_key': OPENAI_API_KEY, 'model': 'gpt-3.5-turbo', 'n_results_sql': 3})
t2s_chroma_n_results_documentation = Text2SqlNumResults(config={'api_key': OPENAI_API_KEY, 'model': 'gpt-3.5-turbo', 'n_results_documentation': 4})

def test_n_results():
    for i in range(1, 10):
        t2s_chroma.train(question=f"What are the total sales for customer {i}?", sql=f"SELECT SUM(sales) FROM example_sales WHERE customer_id = {i}")

    for i in range(1, 10):
        t2s_chroma.train(documentation=f"Sample documentation {i}")

    question = "Whare are the top 5 customers by sales?"
    assert len(t2s_chroma_n_results.get_related_ddl(question)) == 1
    assert len(t2s_chroma_n_results.get_related_documentation(question)) == 1
    assert len(t2s_chroma_n_results.get_similar_question_sql(question)) == 1

    assert len(t2s_chroma_n_results_ddl.get_related_ddl(question)) == 2
    assert len(t2s_chroma_n_results_ddl.get_related_documentation(question)) != 2
    assert len(t2s_chroma_n_results_ddl.get_similar_question_sql(question)) != 2

    assert len(t2s_chroma_n_results_sql.get_related_ddl(question)) != 3
    assert len(t2s_chroma_n_results_sql.get_related_documentation(question)) != 3
    assert len(t2s_chroma_n_results_sql.get_similar_question_sql(question)) == 3

    assert len(t2s_chroma_n_results_documentation.get_related_ddl(question)) != 4
    assert len(t2s_chroma_n_results_documentation.get_related_documentation(question)) == 4
    assert len(t2s_chroma_n_results_documentation.get_similar_question_sql(question)) != 4
