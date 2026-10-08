from typing import List, Dict, Any, Optional
import os
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from rank_bm25 import BM25Okapi
from app.core.config import settings

class HybridVectorStore:
    """Manages Qdrant vector storage with Dense + Sparse BM25 Hybrid Retrieval."""

    def __init__(self, collection_name: str = "financial_docs"):
        self.collection_name = collection_name
        self.storage_path = Path(settings.QDRANT_LOCATION)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize Qdrant Client (Embedded local storage mode - no Docker needed)
        self.client = QdrantClient(path=str(self.storage_path))
        
        # In-memory BM25 index for sparse keyword matching
        self.bm25_corpus: List[Dict[str, Any]] = []
        self.bm25_model: Optional[BM25Okapi] = None
        
        self._ensure_collection()

    def _ensure_collection(self):
        """Creates collection if it doesn't already exist."""
        collections = [c.name for c in self.client.get_collections().collections]
        if self.collection_name not in collections:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=qmodels.VectorParams(
                    size=1536,  # Standard OpenAI text-embedding-3-small dimension
                    distance=qmodels.Distance.COSINE
                )
            )

    def _get_embedding(self, text: str) -> List[float]:
        """Generates embedding vector. Uses OpenAI if key is present, else mock deterministic vector."""
        if settings.OPENAI_API_KEY:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=settings.OPENAI_API_KEY)
                resp = client.embeddings.create(
                    input=text[:8000],
                    model="text-embedding-3-small"
                )
                return resp.data[0].embedding
            except Exception:
                pass

        # Deterministic pseudo-embedding fallback for local testing without API credits
        import hashlib
        h = hashlib.sha256(text.encode("utf-8")).digest()
        # Project 32 bytes into 1536 dimensions
        base = [float(b) / 255.0 for b in h]
        repeated = (base * (1536 // len(base) + 1))[:1536]
        norm = sum(x**2 for x in repeated) ** 0.5 or 1.0
        return [x / norm for x in repeated]

    def index_chunks(self, chunks: List[Dict[str, Any]], session_id: str, ticker: str):
        """Indexes document chunks into both Qdrant (dense) and BM25 (sparse)."""
        points = []
        tokenized_corpus = []

        for idx, chunk in enumerate(chunks):
            embedding = self._get_embedding(chunk["content"])
            point_id = idx + 1
            
            payload = {
                "chunk_id": chunk["chunk_id"],
                "session_id": session_id,
                "ticker": ticker,
                "page_number": chunk["page_number"],
                "is_table": chunk.get("is_table", False),
                "content": chunk["content"]
            }
            
            points.append(
                qmodels.PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=payload
                )
            )

            # Store in BM25 corpus
            self.bm25_corpus.append(payload)
            tokenized_corpus.append(chunk["content"].lower().split())

        # Upload points to Qdrant
        if points:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

        # Build BM25 index
        if tokenized_corpus:
            self.bm25_model = BM25Okapi(tokenized_corpus)

    def hybrid_search(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Executes Hybrid Search combining Dense Cosine + Sparse BM25 via Reciprocal Rank Fusion."""
        # 1. Dense retrieval
        query_vector = self._get_embedding(query)
        dense_results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k * 2
        )

        # 2. Sparse BM25 retrieval
        sparse_scores = []
        if self.bm25_model and self.bm25_corpus:
            tokenized_query = query.lower().split()
            bm25_raw_scores = self.bm25_model.get_scores(tokenized_query)
            ranked_bm25_indices = sorted(range(len(bm25_raw_scores)), key=lambda i: bm25_raw_scores[i], reverse=True)
            for rank, idx in enumerate(ranked_bm25_indices[:top_k * 2]):
                sparse_scores.append((self.bm25_corpus[idx], rank + 1))

        # 3. Reciprocal Rank Fusion (RRF)
        # Score = sum(1 / (k + rank))
        rrf_constant = 60
        fused_scores: Dict[str, Dict[str, Any]] = {}

        for rank, hit in enumerate(dense_results):
            chunk_id = hit.payload.get("chunk_id")
            score = 1.0 / (rrf_constant + (rank + 1))
            if chunk_id not in fused_scores:
                fused_scores[chunk_id] = {"item": hit.payload, "score": score}
            else:
                fused_scores[chunk_id]["score"] += score

        for item, rank in sparse_scores:
            chunk_id = item.get("chunk_id")
            score = 1.0 / (rrf_constant + rank)
            if chunk_id not in fused_scores:
                fused_scores[chunk_id] = {"item": item, "score": score}
            else:
                fused_scores[chunk_id]["score"] += score

        # Sort by combined RRF score
        sorted_results = sorted(fused_scores.values(), key=lambda x: x["score"], reverse=True)
        return [res["item"] for res in sorted_results[:top_k]]
