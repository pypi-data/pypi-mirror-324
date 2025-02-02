from typing import Optional
from datetime import datetime
from haystack_integrations.document_stores.qdrant import QdrantDocumentStore
from haystack_integrations.components.embedders.fastembed import FastembedTextEmbedder, FastembedDocumentEmbedder
from haystack_integrations.components.retrievers.qdrant import QdrantEmbeddingRetriever
from haystack.components.writers import DocumentWriter
from haystack.document_stores.types import DuplicatePolicy
from haystack.dataclasses import Document
from haystack.utils import Secret
from ..birbtalk import BirbTool

# Save and Recall facts about user
def save_load_memory_tools(qdrant_url: Optional[str] = None, 
                qdrant_key: Optional[str] = None,
                collection_name: str = "memories",
                embedding_model: str = "BAAI/bge-small-en-v1.5",
                embedding_cache_dir: Optional[str] = None,
                embedding_local_only: bool = False,
                embedding_dim: int = 384,
                n_memories: int = 10,
                chat_id: Optional[str] = None):

    # Define document store arguments
    qdrant_kwargs = {
        "index": collection_name,
        "wait_result_from_api": True,
        "embedding_dim": embedding_dim,
        "hnsw_config": {
            "payload_m": 16,
            "m": 0
        },
        "payload_fields_to_index": [{
            "field_name": "meta.chat_id",
            "field_schema": {"type": "keyword", "is_tenant": True}
        }]
    }
    qdrant_args = []
    if qdrant_url: qdrant_kwargs["url"] = qdrant_url
    else: qdrant_args.append(":memory:")
    if qdrant_key: qdrant_kwargs["api_key"] = Secret.from_token(qdrant_key)

    # Define filters
    if chat_id:
        filters = {"field": "meta.chat_id", "operator": "==", "value": chat_id}
    else: filters = None

    # Define components
    document_store = QdrantDocumentStore(*qdrant_args, **qdrant_kwargs)
    text_embedder = FastembedTextEmbedder(
        model=embedding_model,
        cache_dir=embedding_cache_dir,
        local_files_only=embedding_local_only
    )
    retriever = QdrantEmbeddingRetriever(
        document_store=document_store,
        filters=filters,
        top_k=n_memories
    )
    doc_embedder = FastembedDocumentEmbedder(
        model=embedding_model,
        cache_dir=embedding_cache_dir,
        local_files_only=embedding_local_only
    )
    writer = DocumentWriter(document_store=document_store, policy=DuplicatePolicy.NONE)
    doc_embedder.warm_up()
    text_embedder.warm_up()

    # Define load function
    def load_function(query: str, chat_id: Optional[int] = None):
        query = text_embedder.run(text=query)["embedding"]
        documents = retriever.run(query_embedding=query)["documents"]
        if documents:
            text = [f"- {x.content}" for x in documents]
            text = "\n".join(text)
            text = f"# Memories\n\n{text}"
        else:
            text = "Nothing found!"
        return text

    # Define save function
    def save_function(fact: str, chat_id: Optional[int] = None):
        documents = [Document(content=fact, meta={
            "chat_id": chat_id,
            "datetime": datetime.now().isoformat()
        })]
        documents = doc_embedder.run(documents=documents)["documents"]
        writer.run(documents=documents)
        return "Memory saved!"

    # Define tools
    return BirbTool(
        name = "save_memory",
        description = "Save short facts about user in memory.",
        function = save_function,
        arguments = {
            "fact": {
                "type": "string",
                "description": "Fact about user such as their preferences, hobbies, life conditions and etc. Should be short and informative. Only use English."
            }
        },
        required = ["fact"]
    ), BirbTool(
        name = "search_memory",
        description = "Search for facts about user such as their preferences, hobbies or life conditions in memory.",
        function = load_function, 
        arguments = {
            "query": {
                "type": "string",
                "description": "Query for performing search in vector database. Should be specific and contain as much keywords as possible. Only use English."
        }
        },
        required = ["query"]
    )
