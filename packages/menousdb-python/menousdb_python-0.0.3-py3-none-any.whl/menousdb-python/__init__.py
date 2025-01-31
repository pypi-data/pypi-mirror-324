import requests as req
import logging
import os
from typing import List, Dict, Optional, Union
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MenousDB:
    """
    A Python client for interacting with the MenousDB database.
    """

    def __init__(self, url: str, key: str, database: Optional[str] = None):
        """
        Initialize the MenousDB client.

        :param url: The base URL of the MenousDB API.
        :param key: The API key for authentication.
        :param database: The name of the database to interact with.
        """
        self.url = url.rstrip('/') + '/'
        self.key = key
        self.database = database
        self.session = req.Session()
        self.session.headers.update({'key': self.key})

    def _make_request(self, method: str, endpoint: str, headers: Optional[Dict] = None, json_data: Optional[Dict] = None) -> Union[Dict, str]:
        """
        Make an HTTP request to the MenousDB API.

        :param method: The HTTP method (e.g., 'GET', 'POST', 'DELETE').
        :param endpoint: The API endpoint to call.
        :param headers: Additional headers to include in the request.
        :param json_data: JSON data to send in the request body.
        :return: The response from the API as a dictionary or string.
        """
        url = self.url + endpoint
        try:
            response = self.session.request(method, url, headers=headers, json=json_data, timeout=10)
            response.raise_for_status()
            try:
                return response.json()
            except json.JSONDecodeError:
                return response.text
        except req.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise Exception(f"Request failed: {e}")

    def readDb(self) -> Union[Dict, str]:
        """
        Read the entire database.

        :return: The database content as a dictionary or string.
        """
        if not self.database:
            raise ValueError("No database specified")
        return self._make_request('GET', 'read-db', headers={'database': self.database})

    def createDb(self) -> str:
        """
        Create a new database.

        :return: A message indicating success or failure.
        """
        if not self.database:
            raise ValueError("No database specified")
        return self._make_request('POST', 'create-db', headers={'database': self.database})

    def deleteDb(self) -> str:
        """
        Delete the specified database.

        :return: A message indicating success or failure.
        """
        if not self.database:
            raise ValueError("No database specified")
        return self._make_request('DELETE', 'del-database', headers={'database': self.database})

    def checkDbExists(self) -> str:
        """
        Check if the specified database exists.

        :return: A message indicating whether the database exists.
        """
        if not self.database:
            raise ValueError("No database specified")
        return self._make_request('GET', 'check-db-exists', headers={'database': self.database})

    def createTable(self, table: str, attributes: List[str]) -> str:
        """
        Create a new table in the database.

        :param table: The name of the table to create.
        :param attributes: A list of attributes (columns) for the table.
        :return: A message indicating success or failure.
        """
        if not self.database:
            raise ValueError("No database specified")
        return self._make_request('POST', 'create-table', headers={'database': self.database, 'table': table}, json_data={'attributes': attributes})

    def checkTableExists(self, table: str) -> str:
        """
        Check if the specified table exists in the database.

        :param table: The name of the table to check.
        :return: A message indicating whether the table exists.
        """
        if not self.database:
            raise ValueError("No database specified")
        return self._make_request('GET', 'check-table-exists', headers={'database': self.database, 'table': table})

    def insertIntoTable(self, table: str, values: List[Dict]) -> str:
        """
        Insert data into the specified table.

        :param table: The name of the table to insert data into.
        :param values: A list of dictionaries representing the rows to insert.
        :return: A message indicating success or failure.
        """
        if not self.database:
            raise ValueError("No database specified")
        return self._make_request('POST', 'insert-into-table', headers={'database': self.database, 'table': table}, json_data={'values': values})

    def getTable(self, table: str) -> Union[Dict, str]:
        """
        Retrieve the entire content of the specified table.

        :param table: The name of the table to retrieve.
        :return: The table content as a dictionary or string.
        """
        if not self.database:
            raise ValueError("No database specified")
        return self._make_request('GET', 'get-table', headers={'database': self.database, 'table': table})

    def selectWhere(self, table: str, conditions: Dict) -> Union[Dict, str]:
        """
        Select rows from the table that match the specified conditions.

        :param table: The name of the table to query.
        :param conditions: A dictionary of conditions to filter rows.
        :return: The filtered rows as a dictionary or string.
        """
        if not self.database:
            raise ValueError("No database specified")
        return self._make_request('GET', 'select-where', headers={'database': self.database, 'table': table}, json_data={'conditions': conditions})

    def selectColumns(self, table: str, columns: List[str]) -> Union[Dict, str]:
        """
        Select specific columns from the table.

        :param table: The name of the table to query.
        :param columns: A list of columns to select.
        :return: The selected columns as a dictionary or string.
        """
        if not self.database:
            raise ValueError("No database specified")
        return self._make_request('GET', 'select-columns', headers={'database': self.database, 'table': table}, json_data={'columns': columns})

    def selectColumnsWhere(self, table: str, columns: List[str], conditions: Dict) -> Union[Dict, str]:
        """
        Select specific columns from the table that match the specified conditions.

        :param table: The name of the table to query.
        :param columns: A list of columns to select.
        :param conditions: A dictionary of conditions to filter rows.
        :return: The filtered columns as a dictionary or string.
        """
        if not self.database:
            raise ValueError("No database specified")
        return self._make_request('GET', 'select-columns-where', headers={'database': self.database, 'table': table}, json_data={'columns': columns, 'conditions': conditions})

    def deleteWhere(self, table: str, conditions: Dict) -> Union[Dict, str]:
        """
        Delete rows from the table that match the specified conditions.

        :param table: The name of the table to delete from.
        :param conditions: A dictionary of conditions to filter rows.
        :return: A message indicating success or failure.
        """
        if not self.database:
            raise ValueError("No database specified")
        return self._make_request('DELETE', 'delete-where', headers={'database': self.database, 'table': table}, json_data={'conditions': conditions})

    def deleteTable(self, table: str) -> Union[Dict, str]:
        """
        Delete the specified table.

        :param table: The name of the table to delete.
        :return: A message indicating success or failure.
        """
        if not self.database:
            raise ValueError("No database specified")
        return self._make_request('DELETE', 'delete-table', headers={'database': self.database, 'table': table})

    def updateWhere(self, table: str, conditions: Dict, values: Dict) -> Union[Dict, str]:
        """
        Update rows in the table that match the specified conditions.

        :param table: The name of the table to update.
        :param conditions: A dictionary of conditions to filter rows.
        :param values: A dictionary of values to update.
        :return: A message indicating success or failure.
        """
        if not self.database:
            raise ValueError("No database specified")
        return self._make_request('POST', 'update-table', headers={'database': self.database, 'table': table}, json_data={'conditions': conditions, 'values': values})

    def getDatabases(self) -> Union[Dict, str]:
        """
        Retrieve a list of all databases.

        :return: A list of databases as a dictionary or string.
        """
        return self._make_request('GET', 'get-databases')

    def getApiKey(self, username: str, password: str) -> Union[Dict, str]:
        """
        Retrieve an API key using the provided username and password.

        :param username: The username for authentication.
        :param password: The password for authentication.
        :return: The API key as a dictionary or string.
        """
        return self._make_request('GET', 'get-api-key', headers={'username': username, 'password': password})

    def __str__(self) -> str:
        return f"MenousDB Client (Database: {self.database})"