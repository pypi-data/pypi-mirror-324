import pymysql.cursors
from .db_connection import DatabaseConnection


class CloudDatabaseExecutor:
    def __init__(self, service, hostname=None, port=None, username=None, password=None, database=None, region=None, server=None, instance_connection_name=None, require_ssl=False):
        """
        Initialize the CloudDatabaseExecutor with connection parameters.

        :param service: The cloud service type ('aws', 'azure', or 'gcp').
        :param hostname: The hostname for AWS RDS (only required for AWS).
        :param port: The port for the database connection (default is typically 3306 for MySQL).
        :param username: The database username for authentication.
        :param database: The name of the database to connect to.
        :param region: The AWS region (only required for AWS).
        :param server: The server name for Azure SQL Database (only required for Azure).
        :param instance_connection_name: The instance connection name for Google Cloud SQL (only required for GCP).
        :param require_ssl: Boolean flag indicating if SSL is required for the connection.
        """
        self.service = service
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.region = region
        self.server = server
        self.instance_connection_name = instance_connection_name
        self.require_ssl = require_ssl
        self.connection = None

    @staticmethod
    def get_operation_from_query(query):
        """
        Determine the SQL operation type from the given SQL query.

        :param query: The SQL query as a string.
        :return: The operation type as a lowercase string (e.g., 'select', 'insert', 'update', 'delete').
        """
        operation = query.strip().split()[0].lower()
        return operation

    def connect(self):
        """Establish a database connection using the provided service details."""
        db_conn = DatabaseConnection(
            service=self.service,
            hostname=self.hostname,
            port=self.port,
            username=self.username,
            password=self.password,
            database=self.database,
            region=self.region,
            server=self.server,
            instance_connection_name=self.instance_connection_name,
            require_ssl=self.require_ssl
        )
        self.connection = db_conn.get_db_connection()

    def close(self):
        """Close the database connection if it's open."""
        if self.connection:
            self.connection.close()

    def execute(self, query, params=None):
        """
        Execute a SQL query on the cloud database.

        :param query: The SQL query string to execute.
        :param params: Optional parameters for the SQL query (for parameterized queries).
        :return: The results of the query for 'select' operations; None for other operations.
        """
        try:
            if not self.connection:
                self.connect()

            with self.connection.cursor() as cursor:
                if params:
                    cursor.execute(query, params)  # Parameterized query
                else:
                    cursor.execute(query)

                operation = self.get_operation_from_query(query)

                if operation in ['insert', 'update', 'delete']:
                    self.connection.commit()

                if operation == 'select':
                    return cursor.fetchall()

        except pymysql.OperationalError as op_err:
            print(f'OperationalError encountered while executing query: "{query}". Error: {op_err}')
            raise

        except ValueError as val_err:
            print(f'ValueError encountered: {val_err}')
            raise

        except Exception as e:
            print(f'An unexpected error occurred while executing query: "{query}". Error: {e}')
            raise

        finally:
            self.close()