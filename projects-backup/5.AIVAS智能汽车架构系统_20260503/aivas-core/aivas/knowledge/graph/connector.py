"""Neo4j graph connector — stores and queries architecture relationships as a knowledge graph."""

from __future__ import annotations

import uuid
from typing import Any


class Neo4jConnector:
    """Connector to Neo4j graph database for architecture knowledge graph.

    Represents RFLP relationships, PLE variant trees, and baseline lineages
    as labeled property graph nodes and edges.

    Gracefully degrades to in-memory mode when Neo4j is not available.
    """

    def __init__(self, uri: str = "bolt://localhost:7687", user: str = "neo4j", password: str = "aivas_dev"):
        self.uri = uri
        self.user = user
        self.password = password
        self._driver = None
        self._memory_graph: dict[str, list[dict]] = {"nodes": [], "edges": []}

    async def connect(self) -> bool:
        """Attempt to connect to Neo4j. Returns True if successful."""
        try:
            from neo4j import AsyncGraphDatabase
            self._driver = AsyncGraphDatabase.driver(self.uri, auth=(self.user, self.password))
            async with self._driver.session() as session:
                await session.run("RETURN 1")
            return True
        except Exception:
            self._driver = None
            return False

    @property
    def connected(self) -> bool:
        return self._driver is not None

    async def upsert_requirement(self, req_id: str, project_id: str, req_type: str, content: str):
        """Create or update a Requirement node."""
        if self._driver:
            try:
                async with self._driver.session() as session:
                    await session.run(
                        """
                        MERGE (r:Requirement {id: $id})
                        SET r.project_id = $project_id, r.type = $type, r.content = $content,
                            r.updated_at = datetime()
                        """,
                        id=req_id, project_id=project_id, type=req_type, content=content[:500],
                    )
            except Exception:
                pass

        self._memory_graph["nodes"].append({
            "id": req_id, "label": "Requirement", "type": req_type, "content": content[:200],
        })

    async def upsert_function(self, func_id: str, project_id: str, name: str, description: str | None = None):
        """Create or update a Function node."""
        if self._driver:
            try:
                async with self._driver.session() as session:
                    await session.run(
                        """
                        MERGE (f:Function {id: $id})
                        SET f.project_id = $project_id, f.name = $name,
                            f.description = $description, f.updated_at = datetime()
                        """,
                        id=func_id, project_id=project_id, name=name,
                        description=description or "",
                    )
            except Exception:
                pass

        self._memory_graph["nodes"].append({
            "id": func_id, "label": "Function", "name": name,
        })

    async def create_trace_link(self, source_id: str, source_label: str, target_id: str, target_label: str):
        """Create a TRACES relationship between two RFLP-layer nodes."""
        rel_type = "TRACES_TO"
        if self._driver:
            try:
                async with self._driver.session() as session:
                    await session.run(
                        f"""
                        MATCH (a:{source_label} {{id: $source_id}})
                        MATCH (b:{target_label} {{id: $target_id}})
                        MERGE (a)-[r:{rel_type}]->(b)
                        SET r.updated_at = datetime()
                        """,
                        source_id=source_id, target_id=target_id,
                    )
            except Exception:
                pass

        self._memory_graph["edges"].append({
            "source": source_id, "target": target_id,
            "relationship": rel_type,
            "source_label": source_label, "target_label": target_label,
        })

    async def query_rflp_chain(self, req_id: str) -> list[dict]:
        """Traverse the full RFLP chain from a requirement to ECUs."""
        if self._driver:
            try:
                async with self._driver.session() as session:
                    result = await session.run(
                        """
                        MATCH (r:Requirement {id: $req_id})
                        OPTIONAL MATCH (r)-[:TRACES_TO]->(f:Function)
                        OPTIONAL MATCH (f)-[:TRACES_TO]->(sc:SC)
                        OPTIONAL MATCH (sc)-[:CONTAINS]->(ssc:SSC)
                        OPTIONAL MATCH (ssc)-[:ALLOCATED_TO]->(ecu:ECU)
                        RETURN r, f, sc, ssc, ecu
                        """,
                        req_id=req_id,
                    )
                    records = await result.data()
                    return records
            except Exception:
                pass
        return []

    async def get_subgraph(self, project_id: str, depth: int = 3) -> dict:
        """Return the full architecture subgraph for a project."""
        if self._driver:
            try:
                async with self._driver.session() as session:
                    result = await session.run(
                        """
                        MATCH (n)
                        WHERE n.project_id = $project_id
                        OPTIONAL MATCH (n)-[r]-(m)
                        WHERE m.project_id = $project_id
                        RETURN n, r, m
                        LIMIT 200
                        """,
                        project_id=project_id,
                    )
                    records = await result.data()
                    return {"nodes": len(records), "project_id": project_id}
            except Exception:
                pass
        return {"nodes": 0, "project_id": project_id, "mode": "memory"}

    async def delete_project(self, project_id: str):
        """Remove all nodes for a project from the graph."""
        if self._driver:
            try:
                async with self._driver.session() as session:
                    await session.run(
                        """
                        MATCH (n {project_id: $project_id})
                        DETACH DELETE n
                        """,
                        project_id=project_id,
                    )
            except Exception:
                pass

    async def close(self):
        if self._driver:
            await self._driver.close()
            self._driver = None


# Singleton
_neo4j: Neo4jConnector | None = None


def get_neo4j_connector() -> Neo4jConnector:
    global _neo4j
    if _neo4j is None:
        _neo4j = Neo4jConnector()
    return _neo4j
