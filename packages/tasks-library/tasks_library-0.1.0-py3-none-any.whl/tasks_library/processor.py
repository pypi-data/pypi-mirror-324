from typing import Optional, Dict
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import connection as _connection
from utils.logger import configure_logger


class TaskProcessor:
    """
    A class to manage task processing functionalities, such as fetching and updating tasks.
    """

    def __init__(self, conn: _connection, schema: str = "tasks", table: str = "tasks"):
        """
        Initialize the TaskProcessor with the specified schema and table.

        Args:
            conn (_connection): A psycopg2 database connection.
            schema (str, optional): The schema where the table resides. Defaults to "tasks".
            table (str, optional): The name of the table to manage. Defaults to "tasks".
        """
        self.schema = schema
        self.table = table
        self.conn = conn
        self.logger = configure_logger(__name__)  # Centralized logger configuration

    def get_next_task(self, processor_id: int) -> Optional[Dict[str, str]]:
        """
        Fetch the next available task for a given processor.

        Args:
            processor_id (int): The processor ID.

        Returns:
            Optional[Dict[str, str]]: The task details or None if no task is found.
        """
        query = sql.SQL("SELECT * FROM {}.{} WHERE processor_id = %s LIMIT 1").format(
            sql.Identifier(self.schema), sql.Identifier(self.table)
        )
        with self.conn.cursor() as cur:
            cur.execute(query, (processor_id,))
            task = cur.fetchone()
            return dict(task) if task else None
