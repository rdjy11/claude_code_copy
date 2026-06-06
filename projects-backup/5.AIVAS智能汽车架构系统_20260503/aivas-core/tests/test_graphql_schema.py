"""GraphQL schema validation tests."""

import pytest
from aivas.api.graphql import schema


class TestGraphQLSchema:
    def test_schema_exists(self):
        assert schema is not None

    def test_schema_has_query_type(self):
        assert schema.query_type is not None

    def test_schema_has_mutation_type(self):
        assert schema.mutation_type is not None

    def test_query_fields_exist(self):
        query_fields = [f.name for f in schema.query_type.fields]
        assert "project" in query_fields or "projects" in query_fields

    def test_mutation_fields_exist(self):
        mutation_fields = [f.name for f in schema.mutation_type.fields]
        assert len(mutation_fields) > 0


class TestGraphQLTypeNames:
    def test_project_type(self):
        type_map = schema.type_map
        assert "Project" in type_map or any("Project" in k for k in type_map.keys())

    def test_requirement_type(self):
        type_map = schema.type_map
        assert "Requirement" in type_map or any("Requirement" in k for k in type_map.keys())
