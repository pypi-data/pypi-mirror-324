import logging
import secrets
from dataclasses import asdict
from typing import Optional

import orjson
import pandas as pd
import requests

from rho_store.exceptions import RhoApiError, InvalidApiKey, RhoServerTimeout
from rho_store.types import SortOption, FilterOption, QueryResult

logger = logging.getLogger(__name__)


class RhoApiGraphqlAdapter:
    REQUEST_TIMEOUT = 10.0

    def __init__(self, base_url: str, api_key: str, client_id: str = "python-sdk"):
        self.base_url = base_url
        self.api_key = api_key
        self.client_id = client_id

        self.session = requests.Session()

    def get_signed_url(self) -> tuple[str, str]:
        file_name = f"{secrets.token_hex(8)}.parquet"
        query = """
        mutation GetUploadUrl($fileName: String!) {
          getUploadUrl(fileName: $fileName) {
            ok
            errorCode
            url
            fileId
          }
        }
        """
        variables = {"fileName": file_name}
        data, errors = self._make_request(query, variables)
        if errors:
            self._raise_graphql_error(errors)
        mutation_result = data["getUploadUrl"]
        self._verify_mutation_result(mutation_result)
        url = mutation_result["url"]
        file_id = mutation_result["fileId"]
        return url, file_id

    def create_table(self, name: str) -> dict:
        query = """
        mutation CreateTable($data: CreateTableInput!) {
          createTable(data: $data) {
            ok
            errorCode
            table {
              id
              name
              workspaceId
            }
          }
        }
        """
        variables = {"data": {"name": name}}
        data, errors = self._make_request(query, variables)
        if errors:
            self._raise_graphql_error(errors)
        mutation_result = data["createTable"]
        self._verify_mutation_result(mutation_result)
        table = mutation_result["table"]
        return table

    def get_table(self, table_id: str) -> dict:
        query = """
        query GetTable($id: String!) {
          table(tableId: $id) {
            id
            name
            workspaceId
            latestVersion
          }
        }
        """
        variables = {"id": table_id}
        data, errors = self._make_request(query, variables)
        if errors:
            self._raise_graphql_error(errors)
        return data.get("table")

    def list_tables(self) -> list[dict]:
        query = """
        query GetTables {
          workspace {
            tables {
              id
              name
              workspaceId
              latestVersion
            }
          }
        }
        """
        data, errors = self._make_request(query)
        if errors:
            self._raise_graphql_error(errors)
        return data.get("workspace", {}).get("tables")

    def process_file(
        self,
        file_id: str,
        table_id: str,
        strategy: Optional[str] = None,
        upsert_options: Optional[dict] = None,
        version: Optional[int] = None,
        run_async: bool = True,
    ) -> dict:
        query = """
        mutation ProcessFile ($data: ProcessFileInput!, $runAsync: Boolean) {
          processFile(data: $data, runAsync: $runAsync) {
            table {
              id
              name
              workspaceId
              latestVersion
            }
            ok
            errorCode
          }
        }
        """
        variables = {
            "data": {
                "fileId": file_id,
                "tableId": table_id,
                "strategy": strategy,
                "version": version,
                "upsertOptions": upsert_options,
            },
            "runAsync": run_async,
        }
        data, errors = self._make_request(query, variables)
        if errors:
            self._raise_graphql_error(errors)
        mutation_result = data["processFile"]
        self._verify_mutation_result(mutation_result)
        table = mutation_result["table"]
        return table

    def process_data(
        self,
        table_id: str,
        data: pd.DataFrame,
        strategy: Optional[str] = None,
        upsert_options: Optional[dict] = None,
        version: Optional[int] = None,
    ) -> dict:
        query = """
        mutation ProcessData ($data: ProcessDataInput!) {
          processData(data: $data) {
            table {
              id
              name
              workspaceId
              latestVersion
            }
            ok
            errorCode
          }
        }
        """
        variables = {
            "data": {
                "tableId": table_id,
                "rawJson": data.to_json(),
                "strategy": strategy,
                "version": version,
                "upsertOptions": upsert_options,
            }
        }
        data, errors = self._make_request(query, variables)
        if errors:
            self._raise_graphql_error(errors)
        mutation_result = data["processData"]
        self._verify_mutation_result(mutation_result)
        table = mutation_result["table"]
        return table

    def query_table(
        self,
        table_id: str,
        columns: list[str] | None = None,
        version: int | None = None,
        sort: list[SortOption] | None = None,
        filters: list[FilterOption] | None = None,
        page: int = 1,
        limit: int = 10000,
        search: str | None = None,
    ) -> QueryResult:
        variables = {
            "tableId": table_id,
            "columns": columns,
            "version": version,
            "page": page,
            "limit": limit,
            "q": search,
        }
        if sort:
            variables["sort"] = [asdict(sort_option) for sort_option in sort]
        if filters:
            variables["filters"] = [asdict(filter_option) for filter_option in filters]

        query = """
        query GetData(
            $tableId: String!,
            $columns: [String!],
            $version: Int,
            $sort: [SortOption!],
            $filters: [FilterOption!],
            $page: Int,
            $limit: Int,
            $q: String
        ) {
            getData (
                tableId: $tableId,
                columns: $columns,
                version: $version,
                sort: $sort,
                filters: $filters,
                page: $page,
                limit: $limit,
                q: $q
            ) {
              id
              time
              rows
              columns
              totalRows
            }
        }
        """
        data, errors = self._make_request(query, variables)
        if errors:
            self._raise_graphql_error(errors)
        fetched_data = data["getData"]
        return QueryResult(
            id=fetched_data["id"],
            time=fetched_data["time"],
            rows=fetched_data["rows"],
            columns=fetched_data["columns"],
            total_rows=fetched_data["totalRows"],
        )

    @staticmethod
    def _raise_graphql_error(errors: list[dict]) -> None:
        logger.debug(f"GraphQL errors: {errors}")
        error_messages = ",".join([error["message"] for error in errors])
        raise RhoApiError(error_messages)

    @staticmethod
    def _verify_mutation_result(mutation_result: dict) -> None:
        if not mutation_result["ok"]:
            error_code = mutation_result["errorCode"]
            raise RhoApiError(error_code)

    def _make_request(self, query: str, variables: dict = None) -> tuple[dict, list[dict]]:
        operation_name = self.get_operation_name(query)
        payload = {"query": query, "operationName": operation_name}
        if variables:
            payload["variables"] = variables
        headers = self.get_headers()
        params = {"operation": operation_name}
        try:
            response = self.session.post(
                self.base_url, json=payload, headers=headers, params=params, timeout=self.REQUEST_TIMEOUT
            )
        except requests.exceptions.Timeout as e:
            raise RhoServerTimeout("Server timed out") from e

        if response.status_code == 403:
            raise InvalidApiKey("Invalid API key")
        if response.status_code == 401:
            raise InvalidApiKey("No access")

        try:
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            # default
            raise RhoApiError(f"Bad response from server: {response.status_code}") from e

        # response_data = response.json()
        response_data = orjson.loads(response.content)
        data, errors = response_data.get("data"), response_data.get("errors")
        return data, errors

    def get_headers(self) -> dict:
        return {"Content-Type": "application/json", "X-Api-Key": self.api_key, "X-Client-ID": self.client_id}

    @staticmethod
    def get_operation_name(query: str) -> str:
        first_part = query.split("{")[0].strip()
        operation_name = first_part.split(" ")[1]
        if "(" in operation_name:
            operation_name = operation_name.split("(")[0]
        return operation_name.strip()


__all__ = ["RhoApiGraphqlAdapter"]
