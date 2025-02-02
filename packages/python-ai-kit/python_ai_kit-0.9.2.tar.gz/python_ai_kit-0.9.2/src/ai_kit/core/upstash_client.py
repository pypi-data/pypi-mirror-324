import logging
import uuid
from upstash_vector import Index, Vector
from typing import List, Set
from ai_kit.core.llms.litellm_client import EmbeddingClient

logger = logging.getLogger(__name__)

BATCH_DELETE_SIZE = 100  # Upstash recommended batch size

class UpstashVectorStore:
    """A vector store implementation using Upstash for storing and querying vectors."""
    
    def __init__(self):
        try:
            self.index = Index.from_env()
            self.embedding_client = EmbeddingClient(model="text-embedding-3-small")
            logger.info("VectorStore initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize VectorStore: {e}")
            raise

    def upsert(self, vectors: List[List[float]], data: List[str], metadata: List[dict], ids: List[str]) -> List[str]:
        """
        Upsert vectors with explicit IDs (like file hashes).
        
        Args:
            vectors: List of vector embeddings
            data: List of chunk texts
            metadata: List of metadata dicts (should only contain file info, not chunk text)
            ids: List of vector IDs (file hashes)
        """
        if not (len(vectors) == len(data) == len(metadata) == len(ids)):
            raise ValueError("Number of vectors, data strings, metadata dictionaries, and IDs must match")
        
        try:
            vector_objs = [
                Vector(id=vid, vector=vec, data=dat, metadata=meta)
                for vid, vec, dat, meta in zip(ids, vectors, data, metadata)
            ]
            self.index.upsert(vectors=vector_objs)
            logger.info(f"Batch upserted {len(ids)} vectors successfully")
            return ids
        except Exception as e:
            logger.error(f"Failed to batch upsert vectors: {e}")
            raise

    def delete_vectors(self, ids: List[str]) -> int:
        """
        Delete vectors by their IDs in batches.
        
        Args:
            ids: List of vector IDs to delete
            
        Returns:
            int: Total number of vectors deleted
        """
        if not ids:
            return 0
            
        total_deleted = 0
        try:
            # Process deletions in batches
            for i in range(0, len(ids), BATCH_DELETE_SIZE):
                batch = ids[i:i + BATCH_DELETE_SIZE]
                result = self.index.delete(ids=batch)
                batch_deleted = result.deleted
                total_deleted += batch_deleted
                logger.info(f"Deleted batch of {batch_deleted} vectors")
            
            logger.info(f"Successfully deleted total of {total_deleted} vectors")
            return total_deleted
        except Exception as e:
            logger.error(f"Failed to delete vectors: {e}")
            raise

    def query(self, vector: List[float], k: int = 10) -> List[dict]:
        """
        Query vectors by similarity.
        
        Args:
            vector: Query vector
            k: Number of results to return
            
        Returns:
            List of results, each containing:
            - score: Similarity score
            - data: Chunk text
            - metadata: File info (filename, rel_path, file_hash)
        """
        try:
            results = self.index.query(
                vector, # ! this takes a list of floats not an upstash vector object
                k,
                include_vectors=True,
                include_metadata=True,
                include_data=True
            )
            logger.info(f"Query executed successfully with top {k} results")
            return results
        except Exception as e:
            logger.error(f"Failed to execute query: {e}")
            raise

    async def add_to_vector_store(self, texts: List[str], metadata: List[dict], ids: List[str]) -> List[str]:
        """
        Add texts to vector store.
        
        Args:
            texts: List of chunk texts (will be stored in data field)
            metadata: List of metadata dicts (file info only)
            ids: List of vector IDs (file hashes)
        """
        try:
            if not (len(texts) == len(metadata) == len(ids)):
                raise ValueError("Number of texts, metadata dictionaries, and IDs must match")
            
            embeddings = await self.embedding_client.create_embeddings(texts)
            return self.upsert(embeddings, texts, metadata, ids)
        except Exception as e:
            logger.error(f"Failed to add texts to vector store: {e}")
            raise

    def __enter__(self):
        """Enable context manager support."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up resources when exiting context."""
        logger.info("Closing VectorStore resources")
