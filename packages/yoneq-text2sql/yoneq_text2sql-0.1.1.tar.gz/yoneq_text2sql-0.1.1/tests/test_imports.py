

def test_regular_imports():
    from yoneq_text2sql.anthropic.anthropic_chat import Anthropic_Chat
    from yoneq_text2sql.azuresearch.azuresearch_vector import AzureAISearch_VectorStore
    from yoneq_text2sql.base.base import Text2SqlBase
    from yoneq_text2sql.bedrock.bedrock_converse import Bedrock_Converse
    from yoneq_text2sql.chromadb.chromadb_vector import ChromaDB_VectorStore
    from yoneq_text2sql.faiss.faiss import FAISS
    from yoneq_text2sql.google.bigquery_vector import BigQuery_VectorStore
    from yoneq_text2sql.google.gemini_chat import GoogleGeminiChat
    from yoneq_text2sql.hf.hf import Hf
    from yoneq_text2sql.local import LocalContext_OpenAI
    from yoneq_text2sql.marqo.marqo import Marqo_VectorStore
    from yoneq_text2sql.milvus.milvus_vector import Milvus_VectorStore
    from yoneq_text2sql.mistral.mistral import Mistral
    from yoneq_text2sql.ollama.ollama import Ollama
    from yoneq_text2sql.openai.openai_chat import OpenAI_Chat
    from yoneq_text2sql.openai.openai_embeddings import OpenAI_Embeddings
    from yoneq_text2sql.opensearch.opensearch_vector import OpenSearch_VectorStore
    from yoneq_text2sql.pgvector.pgvector import PG_VectorStore
    from yoneq_text2sql.pinecone.pinecone_vector import PineconeDB_VectorStore
    from yoneq_text2sql.qdrant.qdrant import Qdrant_VectorStore
    from yoneq_text2sql.qianfan.Qianfan_Chat import Qianfan_Chat
    from yoneq_text2sql.qianfan.Qianfan_embeddings import Qianfan_Embeddings
    from yoneq_text2sql.qianwen.QianwenAI_chat import QianWenAI_Chat
    from yoneq_text2sql.qianwen.QianwenAI_embeddings import QianWenAI_Embeddings
    from yoneq_text2sql.weaviate.weaviate_vector import WeaviateDatabase
    from yoneq_text2sql.xinference.xinference import Xinference
    from yoneq_text2sql.ZhipuAI.ZhipuAI_Chat import ZhipuAI_Chat
    from yoneq_text2sql.ZhipuAI.ZhipuAI_embeddings import ZhipuAI_Embeddings

def test_shortcut_imports():
    from yoneq_text2sql.anthropic import Anthropic_Chat
    from yoneq_text2sql.azuresearch import AzureAISearch_VectorStore
    from yoneq_text2sql.base import Text2SqlBase
    from yoneq_text2sql.chromadb import ChromaDB_VectorStore
    from yoneq_text2sql.faiss import FAISS
    from yoneq_text2sql.hf import Hf
    from yoneq_text2sql.marqo import Marqo_VectorStore
    from yoneq_text2sql.milvus import Milvus_VectorStore
    from yoneq_text2sql.mistral import Mistral
    from yoneq_text2sql.ollama import Ollama
    from yoneq_text2sql.openai import OpenAI_Chat, OpenAI_Embeddings
    from yoneq_text2sql.opensearch import OpenSearch_VectorStore
    from yoneq_text2sql.pgvector import PG_VectorStore
    from yoneq_text2sql.pinecone import PineconeDB_VectorStore
    from yoneq_text2sql.qdrant import Qdrant_VectorStore
    from yoneq_text2sql.qianfan import Qianfan_Chat, Qianfan_Embeddings
    from yoneq_text2sql.qianwen import QianWenAI_Chat, QianWenAI_Embeddings
    from yoneq_text2sql.vllm import Vllm
    from yoneq_text2sql.weaviate import WeaviateDatabase
    from yoneq_text2sql.xinference import Xinference
    from yoneq_text2sql.ZhipuAI import ZhipuAI_Chat, ZhipuAI_Embeddings
