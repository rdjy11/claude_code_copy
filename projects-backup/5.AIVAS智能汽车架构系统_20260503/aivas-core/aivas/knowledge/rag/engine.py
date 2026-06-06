"""RAG engine — pgvector-backed retrieval-augmented generation for architecture knowledge."""

from __future__ import annotations

import uuid
from typing import Any


class RAGEngine:
    """Retrieval-Augmented Generation engine using pgvector for embedding search.

    Indexes requirements, functions, and architecture documents as vector embeddings.
    Falls back to keyword search when pgvector is not available.
    """

    def __init__(self, db=None):
        self.db = db
        self._embedding_model = "text-embedding-3-small"

    async def index_requirement(self, req_id: str, project_id: str, content: str, embedding: list[float] | None = None):
        """Index a requirement with its embedding vector."""
        if not self.db:
            return

        try:
            from sqlalchemy import text
            if embedding:
                embedding_str = f"[{','.join(str(x) for x in embedding)}]"
                await self.db.execute(
                    text(
                        "INSERT INTO requirement_embeddings (requirement_id, project_id, content, embedding) "
                        "VALUES (:req_id, :project_id, :content, :embedding::vector) "
                        "ON CONFLICT (requirement_id) DO UPDATE SET embedding = :embedding::vector, content = :content"
                    ),
                    {"req_id": req_id, "project_id": project_id, "content": content, "embedding": embedding_str},
                )
                await self.db.commit()
        except Exception:
            await self.db.rollback()

    async def search_similar(
        self, project_id: str, query_embedding: list[float], top_k: int = 5
    ) -> list[dict]:
        """Vector similarity search — find semantically similar requirements."""
        if not self.db:
            return []

        try:
            from sqlalchemy import text
            embedding_str = f"[{','.join(str(x) for x in query_embedding)}]"
            result = await self.db.execute(
                text(
                    "SELECT requirement_id, content, 1 - (embedding <=> :embedding::vector) AS similarity "
                    "FROM requirement_embeddings "
                    "WHERE project_id = :project_id "
                    "ORDER BY embedding <=> :embedding::vector "
                    "LIMIT :limit"
                ),
                {"embedding": embedding_str, "project_id": project_id, "limit": top_k},
            )
            rows = result.fetchall()
            return [
                {"requirement_id": row[0], "content": row[1][:200], "similarity": round(float(row[2]), 4)}
                for row in rows
            ]
        except Exception:
            return []

    async def keyword_search(self, project_id: str, query: str, top_k: int = 5) -> list[dict]:
        """Fallback: PostgreSQL full-text search on requirements."""
        if not self.db:
            return []

        try:
            from sqlalchemy import select, text
            from aivas.models.requirement import Requirement

            result = await self.db.execute(
                select(Requirement)
                .where(
                    Requirement.project_id == uuid.UUID(project_id),
                    Requirement.content.ilike(f"%{query}%"),
                )
                .limit(top_k)
            )
            reqs = result.scalars().all()
            return [
                {"requirement_id": str(r.id), "type": r.type, "content": r.content[:200]}
                for r in reqs
            ]
        except Exception:
            return []

    async def hybrid_search(
        self, project_id: str, query: str, query_embedding: list[float] | None = None, top_k: int = 5
    ) -> dict[str, Any]:
        """Combined vector + keyword search with result fusion."""
        vector_results = await self.search_similar(project_id, query_embedding, top_k) if query_embedding else []
        keyword_results = await self.keyword_search(project_id, query, top_k)

        # Deduplicate and merge
        seen_ids: set[str] = set()
        merged: list[dict] = []
        for r in vector_results:
            if r["requirement_id"] not in seen_ids:
                seen_ids.add(r["requirement_id"])
                merged.append({**r, "source": "vector"})

        for r in keyword_results:
            if r["requirement_id"] not in seen_ids:
                seen_ids.add(r["requirement_id"])
                merged.append({**r, "source": "keyword", "similarity": 0.5})

        return {
            "query": query,
            "results": merged[:top_k],
            "total_vector": len(vector_results),
            "total_keyword": len(keyword_results),
        }

    async def build_context(self, project_id: str, query: str, top_k: int = 5) -> str:
        """Build a RAG context string from search results for prompt injection."""
        search_result = await self.hybrid_search(project_id, query, top_k=top_k)
        if not search_result["results"]:
            return ""

        lines = ["## 相关需求上下文 (RAG)"]
        for i, r in enumerate(search_result["results"], 1):
            lines.append(f"{i}. [{r.get('type', 'N/A')}] {r['content']}")
        return "\n".join(lines)


# Singleton
_rag: RAGEngine | None = None


def get_rag_engine(db=None) -> RAGEngine:
    global _rag
    if _rag is None:
        _rag = RAGEngine(db)
    return _rag
