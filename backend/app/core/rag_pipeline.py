"""
RAG Pipeline — ChromaDB + LangChain retrieval for SAR regulatory templates.

Owner: P2
"""
from typing import Optional


class RAGPipeline:
    """Retrieval-Augmented Generation pipeline for SAR context."""

    def __init__(self, persist_dir: str = "./chroma_db", collection_name: str = "sar_knowledge_base"):
        self.persist_dir = persist_dir
        self.collection_name = collection_name
        self.vectorstore = None
        self.retriever = None

    async def initialize(self):
        """
        Set up ChromaDB and index the knowledge base documents.
        """
        import os
        from langchain_ollama import OllamaEmbeddings
        from langchain_community.vectorstores import Chroma
        from langchain_community.document_loaders import DirectoryLoader, TextLoader
        from langchain_text_splitters import RecursiveCharacterTextSplitter

        # Initialize Embeddings
        self.embeddings = OllamaEmbeddings(
            model="llama3.1:8b",
            base_url="http://localhost:11434"
        )

        # Check if vectorstore exists
        if os.path.exists(self.persist_dir) and os.listdir(self.persist_dir):
            print(f"Loading existing vectorstore from {self.persist_dir}")
            self.vectorstore = Chroma(
                persist_directory=self.persist_dir,
                embedding_function=self.embeddings,
                collection_name=self.collection_name
            )
        else:
            print("Creating new vectorstore...")
            # Load documents
            # Resolving path relative to backend root
            current_dir = os.path.dirname(os.path.abspath(__file__)) # app/core
            backend_root = os.path.dirname(os.path.dirname(current_dir)) # backend
            kb_path = os.path.join(backend_root, "knowledge_base")
            
            loaders = [
                DirectoryLoader(os.path.join(kb_path, "regulations"), glob="**/*.txt", loader_cls=TextLoader),
                DirectoryLoader(os.path.join(kb_path, "sar_templates"), glob="**/*.txt", loader_cls=TextLoader),
                DirectoryLoader(os.path.join(kb_path, "sar_templates"), glob="**/*.md", loader_cls=TextLoader)
            ]
            
            documents = []
            for loader in loaders:
                try:
                    docs = loader.load()
                    documents.extend(docs)
                except Exception as e:
                    print(f"Error loading documents: {e}")

            if not documents:
                print("No documents found to index.")
                # Initialize empty vectorstore
                self.vectorstore = Chroma(
                    persist_directory=self.persist_dir,
                    embedding_function=self.embeddings,
                    collection_name=self.collection_name
                )
                return

            # Split documents
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            splits = text_splitter.split_documents(documents)

            # Create Vectorstore
            self.vectorstore = Chroma.from_documents(
                documents=splits,
                embedding=self.embeddings,
                persist_directory=self.persist_dir,
                collection_name=self.collection_name
            )
            print(f"Indexed {len(splits)} chunks into ChromaDB.")

        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})

    async def retrieve_context(self, query: str, top_k: int = 5) -> list[dict]:
        """
        Retrieve relevant regulatory context for a given query.
        """
        if not self.vectorstore:
            await self.initialize()
            
        if not self.retriever:
             self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": top_k})
             
        try:
            docs = await self.retriever.ainvoke(query)
            return [
                {
                    "content": doc.page_content,
                    "source": doc.metadata.get("source", "unknown"),
                    "relevance_score": 0.0 # Chroma doesn't return score by default with invoke, need similarity_search_with_score
                }
                for doc in docs
            ]
        except Exception as e:
            print(f"Error retrieving context: {e}")
            return []

    def add_documents(self, documents: list[dict]):
        """
        Add new documents to the knowledge base.
        """
        from langchain_core.documents import Document
        
        if not self.vectorstore:
             # run sync version of initialize or just warn
             print("Vectorstore not initialized. Cannot add documents.")
             return

        docs_to_add = [
            Document(page_content=d["content"], metadata=d.get("metadata", {}))
            for d in documents
        ]
        
        self.vectorstore.add_documents(docs_to_add)

