from typing import List, Dict, Any

class CrossEncoderReranker:
    """Reranks retrieved candidate chunks to maximize precision and suppress noise."""

    def __init__(self, model_name: str = "ms-marco-TinyBERT-L-2-v2"):
        self.model_name = model_name
        self.ranker = None
        try:
            from flashrank import Ranker
            self.ranker = Ranker(model_name=self.model_name)
        except Exception:
            # Fallback if flashrank native binaries are not yet compiled
            self.ranker = None

    def rerank(self, query: str, candidates: List[Dict[str, Any]], top_n: int = 5) -> List[Dict[str, Any]]:
        """Reranks candidate chunks based on query-passage relevance."""
        if not candidates:
            return []

        # If flashrank is available, use neural cross-encoder
        if self.ranker:
            try:
                from flashrank import RerankRequest
                passages = [
                    {"id": idx, "text": c["content"], "meta": c}
                    for idx, c in enumerate(candidates)
                ]
                req = RerankRequest(query=query, passages=passages)
                results = self.ranker.rerank(req)
                return [r["meta"] for r in results[:top_n]]
            except Exception:
                pass

        # Robust heuristic fallback: prioritizes tables and keyword density
        def score_passage(passage: Dict[str, Any]) -> float:
            content = passage["content"].lower()
            query_terms = query.lower().split()
            term_matches = sum(1 for term in query_terms if term in content)
            
            # Boost financial tables as they contain definitive numbers
            table_boost = 2.0 if passage.get("is_table") else 1.0
            return (term_matches * 1.5) * table_boost

        sorted_candidates = sorted(candidates, key=score_passage, reverse=True)
        return sorted_candidates[:top_n]
