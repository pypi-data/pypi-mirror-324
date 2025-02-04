import time
import boto3
import pymysql.cursors
# import pyodbc
import google.auth
from google.auth.transport.requests import Request

# Global variable to hold the database connection
db_connection = None

class DatabaseConnection:
    def __init__(self, service, hostname=None, port=None, username=None, password=None, database=None, region=None, server=None, instance_connection_name=None, require_ssl=False):
        """
        Initializes the database connection object for the specified service.
        
        Args:
            service (str): The database service to connect to ('aws', 'azure', 'gcp').
            hostname (str): The hostname for AWS RDS (if applicable).
            port (int): The port number for AWS RDS (if applicable).
            username (str): The username for the database connection.
            password (str): The password for the database connection (for AWS).
            database (str): The name of the database to connect to.
            region (str): The AWS region (if applicable).
            server (str): The Azure SQL server (if applicable).
            instance_connection_name (str): The GCP Cloud SQL instance connection name (if applicable).
            require_ssl (bool): Whether SSL is required for the connection (for GCP).
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

    def create_local_connection(self):
        """Generates an authentication token for AWS RDS."""
        client = boto3.client('rds', region_name=self.region)
        token = client.generate_db_auth_token(
            DBHostname=self.hostname,
            Port=self.port,
            DBUsername=self.username,
            Region=self.region
        )
        return token

    def create_aws_connection(self):
        """Generates an authentication token for AWS RDS."""
        client = boto3.client('rds', region_name=self.region)
        token = client.generate_db_auth_token(
            DBHostname=self.hostname,
            Port=self.port,
            DBUsername=self.username,
            Region=self.region
        )
        return token

    def create_azure_connection(self):
        """Creates a connection to Azure SQL Database."""
        credentials, _ = google.auth.default()
        credentials.refresh(Request())
        token = credentials.token

        connection_string = (
            f"Driver={{ODBC Driver 17 for SQL Server}};"
            f"Server={self.server};"
            f"Database={self.database};"
            f"Uid={self.username};"
            f"Pwd={token};"
            "Encrypt=yes;TrustServerCertificate=yes;"
        )
        return pyodbc.connect(connection_string)

    def create_gcp_connection(self):
        """Creates a connection to Google Cloud SQL."""
        credentials, _ = google.auth.default()
        credentials.refresh(Request())
        token = credentials.token

        connection_args = {
            "user": self.username,
            "password": token,
            "database": self.database,
            "unix_socket": f'/cloudsql/{self.instance_connection_name}',
            "cursorclass": pymysql.cursors.DictCursor
        }

        if self.require_ssl:
            connection_args["ssl"] = {"ca": "/path/to/server-ca.pem"}  # Specify correct CA if needed

        return pymysql.connect(**connection_args)

    def get_db_connection(self, max_retries=5, retry_delay=5):
        """Retrieves a database connection for the specified service."""
        global db_connection

        if db_connection and db_connection.open:
            return db_connection  # Reuse existing connection

        retries = 0

        while retries < max_retries:
            try:
                if self.service == 'aws':
                    password = self.create_aws_connection()
                    db_connection = pymysql.connect(
                        host=self.hostname,
                        user=self.username,
                        password=password,
                        db=self.database,
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor,
                        ssl={"use": True}
                    )
                    return db_connection
                
                elif self.service == 'local':
                    db_connection = pymysql.connect(
                        host=self.hostname,
                        user=self.username,
                        password=self.password,
                        db=self.database,
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor,
                        ssl={"use": True}
                    )
                    return db_connection
                
                elif self.service == 'azure':
                    db_connection = self.create_azure_connection()
                    return db_connection

                elif self.service == 'gcp':
                    db_connection = self.create_gcp_connection()
                    return db_connection

                else:
                    raise ValueError(f"Unsupported service type: {self.service}")

            except pymysql.OperationalError as op_err:
                retries += 1
                time.sleep(retry_delay)

        raise pymysql.OperationalError(f"Failed to connect to the database after {max_retries} retries.")
