from __future__ import annotations

import logging
import os
from typing import Any, ClassVar, Dict, List

from gql import Client, gql
from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.piscada_foresight.http_piscada import (
    ForesightHTTPXTransport,  # type: ignore[import]
)

log = logging.getLogger(__name__)


class QueryManager:
    """
    Manages loading query templates (Jinja or .graphql) and executing them
    against a Piscada Foresight GraphQL endpoint.
    """

    _instance: ClassVar[QueryManager | None] = None
    _query_dict: ClassVar[Dict[str, str]] = {}
    _queries_dir: ClassVar[str] = ""

    def __new__(cls, *args: Any, **kwargs: Any) -> QueryManager:
        if cls._instance is None:
            cls._instance = super(QueryManager, cls).__new__(cls)
            cls._instance._load_queries()
            cls._queries_dir = os.path.dirname(__file__)
        return cls._instance

    def __init__(self, domain: str) -> None:
        super().__init__()
        self.client: Client = self._get_client(domain)
        self.query_text: str | None = None

    def _get_client(self, domain: str) -> Client:
        transport = ForesightHTTPXTransport(domain)  # type: ignore[call-arg]
        fs_client = Client(transport=transport, fetch_schema_from_transport=False)
        return fs_client

    def _load_queries(self) -> None:
        """
        Load .j2 or .graphql query templates from ../queries
        storing their relative paths in self._query_dict.
        """
        queries_dir = os.path.join(os.path.dirname(__file__))
        self.__class__._query_dict = {}

        for root, _, files in os.walk(queries_dir):
            for file in files:
                if file.endswith(".j2") or file.endswith(".graphql"):
                    relative_path = os.path.relpath(
                        os.path.join(root, file), queries_dir
                    )
                    query_name = os.path.splitext(file)[0]
                    self.__class__._query_dict[query_name] = relative_path

    @property
    def queries_dir(self) -> str:
        return self.__class__._queries_dir

    @queries_dir.setter
    def queries_dir(self, value: str) -> None:
        self.__class__._queries_dir = value

    def get_query_dict(self) -> Dict[str, str]:
        """
        Return the dictionary of loaded query templates:
        { 'some_query_name': 'path/to/some_query.j2', ... }
        """
        return self.__class__._query_dict

    def load_query(self, query_name: str, jinja_variables: List[str] | None) -> str:
        template_path = self.__class__._query_dict.get(query_name)
        if not template_path:
            raise ValueError(f"Query '{query_name}' not found in _query_dict.")
        full_path = os.path.join(self.queries_dir, template_path)
        if template_path.endswith(".j2"):

            jinja_env = Environment(
                loader=FileSystemLoader(self.queries_dir),
                autoescape=select_autoescape(),
                trim_blocks=True,
                lstrip_blocks=True,
            )
            jinja_vars = jinja_variables
            template = jinja_env.get_template(template_path)
            query_text = template.render(variable_names=jinja_vars)
        elif template_path.endswith(".graphql"):
            with open(full_path, "r", encoding="utf-8") as file:
                query_text = file.read()
        else:
            raise ValueError(f"Unsupported query file type: '{template_path}'.")

        self.query_text = query_text
        return query_text

    def execute_query(self, query: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = self.client.execute(gql(query), variable_values=variables)
        except Exception as execution_error:
            raise RuntimeError(
                f"An error occurred while executing the query: {execution_error}.\n"
                f"Query: {query}\nVariables: {variables}"
            ) from execution_error
        return response

    def run_query(
        self,
        query_name: str,
        jinja_variables: List[str] | None = None,
        query_variables: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        if jinja_variables is None:
            jinja_variables = []
        if query_variables is None:
            query_variables = {}

        query_text = self.load_query(query_name, jinja_variables)
        response = self.execute_query(query_text, query_variables)
        return response
