"""
RAG Vector Store — Pure-Python lightweight vector store using Gemini embeddings.
No external dependencies (no numpy, no ChromaDB).
"""

import json
import math
import os
import google.generativeai as genai

from app.config import get_settings
from app.services.rag.knowledge import ALGORITHM_PATTERNS

settings = get_settings()


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    """Pure-Python cosine similarity between two vectors."""
    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


class VectorStore:
    """
    Lightweight in-memory vector store using Gemini Embedding API.
    Pure-Python — zero native dependencies.
    Persists embeddings to a JSON file so they only need to be computed once.
    """

    def __init__(self):
        # Only configure Gemini if API key is available (for embeddings)
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
        self._documents: list[dict] = []
        self._embeddings: list[list[float]] = []
        self._persist_path = os.path.join(settings.CHROMA_PERSIST_DIR, "embeddings.json")

    def seed_knowledge_base(self):
        """Seed the vector store with algorithm patterns."""
        # Try loading persisted embeddings first
        if self._load_persisted():
            return

        # Skip seeding if no API key configured (dev mode)
        if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "your_gemini_api_key_here":
            self._documents = [
                {
                    "id": p["id"],
                    "title": p["title"],
                    "content": p["content"],
                    "tags": p["tags"],
                    "text": f"{p['title']}\n\n{p['content']}",
                }
                for p in ALGORITHM_PATTERNS
            ]
            # Use simple keyword matching as fallback when no API key
            return

        # Generate embeddings for all patterns using Gemini
        self._documents = []
        texts = []
        for pattern in ALGORITHM_PATTERNS:
            doc = {
                "id": pattern["id"],
                "title": pattern["title"],
                "content": pattern["content"],
                "tags": pattern["tags"],
                "text": f"{pattern['title']}\n\n{pattern['content']}",
            }
            self._documents.append(doc)
            texts.append(doc["text"])

        # Try embedding with Gemini API, fall back to keyword search if it fails
        try:
            self._embeddings = []
            for text in texts:
                result = genai.embed_content(
                    model="models/text-embedding-004",
                    content=text,
                    task_type="retrieval_document",
                )
                self._embeddings.append(result["embedding"])

            # Persist to disk
            self._persist()
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning(
                f"Embedding generation failed ({e}), using keyword search fallback"
            )
            self._embeddings = []  # Clear — will use keyword fallback

    def query(self, text: str, n_results: int = 3) -> list[dict]:
        """
        Query the vector store for relevant algorithm patterns.
        Uses cosine similarity between the query embedding and stored embeddings.
        Falls back to keyword matching if no embeddings available.
        """
        if not self._documents:
            return []

        # If no embeddings (no API key), use keyword fallback
        if not self._embeddings:
            return self._keyword_search(text, n_results)

        # Embed the query
        try:
            result = genai.embed_content(
                model="models/text-embedding-004",
                content=text,
                task_type="retrieval_query",
            )
            query_embedding = result["embedding"]
        except Exception:
            return self._keyword_search(text, n_results)

        # Compute similarities
        scored = []
        for i, doc_embedding in enumerate(self._embeddings):
            score = _cosine_similarity(query_embedding, doc_embedding)
            scored.append((i, score))

        # Sort by score descending
        scored.sort(key=lambda x: x[1], reverse=True)

        patterns = []
        for idx, score in scored[:n_results]:
            doc = self._documents[idx]
            patterns.append({
                "content": doc["text"],
                "title": doc["title"],
                "tags": doc["tags"],
                "relevance_score": score,
            })

        return patterns

    def _keyword_search(self, text: str, n_results: int) -> list[dict]:
        """Simple keyword-based fallback search when embeddings aren't available."""
        text_lower = text.lower()
        scored = []
        for doc in self._documents:
            # Count keyword matches
            score = 0
            for tag in doc["tags"]:
                if tag.lower() in text_lower:
                    score += 2
            for word in doc["title"].lower().split():
                if word in text_lower:
                    score += 1
            scored.append((doc, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [
            {
                "content": doc["text"],
                "title": doc["title"],
                "tags": doc["tags"],
                "relevance_score": score / 10.0,
            }
            for doc, score in scored[:n_results]
            if score > 0
        ]

    def format_context(self, patterns: list[dict]) -> str:
        """Format retrieved patterns into context string for the LLM prompt."""
        if not patterns:
            return ""

        parts = []
        for p in patterns:
            score = p.get("relevance_score", 0)
            parts.append(f"**{p['title']}** (relevance: {score:.2f})\n{p['content']}")

        return "\n\n---\n\n".join(parts)

    def _persist(self):
        """Save embeddings to disk for reuse."""
        os.makedirs(os.path.dirname(self._persist_path), exist_ok=True)
        data = {
            "documents": self._documents,
            "embeddings": self._embeddings,
        }
        with open(self._persist_path, "w") as f:
            json.dump(data, f)

    def _load_persisted(self) -> bool:
        """Load embeddings from disk. Returns True if successful."""
        if not os.path.exists(self._persist_path):
            return False
        try:
            with open(self._persist_path, "r") as f:
                data = json.load(f)
            self._documents = data["documents"]
            self._embeddings = data["embeddings"]
            return True
        except Exception:
            return False


# Singleton
_store: VectorStore | None = None


def get_vector_store() -> VectorStore:
    """Get or create the vector store singleton."""
    global _store
    if _store is None:
        _store = VectorStore()
        _store.seed_knowledge_base()
    return _store
