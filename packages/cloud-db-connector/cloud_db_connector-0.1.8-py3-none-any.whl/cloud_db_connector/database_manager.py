from .rds_execute import CloudDatabaseExecutor

def get_cloud_db_service(service, hostname=None, port=None, username=None, password=None, database=None, region=None, server=None, instance_connection_name=None, require_ssl=False):

    if service not in ['aws', 'azure', 'gcp', 'local']:
        raise ValueError(f"Unsupported cloud provider: '{service}'. Supported providers: aws, azure, gcp, local")
    
    if service == 'aws':
        # Create and return an AWS executor
        executor = CloudDatabaseExecutor(
            service=service,
            hostname=hostname,
            password=password,
            port=port,
            username=username,
            database=database,
            region=region
        )
        return executor

    elif service == 'local':
        # Create and return an local executor
        executor = CloudDatabaseExecutor(
            service=service,
            hostname=hostname,
            port=port,
            username=username,
            password=password,
            database=database,
            region=region
        )
        return executor

    elif service == 'azure':
        # Create and return an Azure executor
        executor = CloudDatabaseExecutor(
            service=service,
            server=server,
            username=username,
            database=database        
        )
        return executor

    elif service == 'gcp':
        # Create and return a GCP executor
        executor = CloudDatabaseExecutor(
            service=service,
            instance_connection_name=instance_connection_name,
            username=username,
            database=database,
            require_ssl=False  
        )
        return executor
    """
    Initializes and returns a cloud database service instance based on the specified provider.

    This function supports three cloud providers: AWS, Azure, and GCP. It instantiates the 
    appropriate database service class based on the input parameters and returns the instance.

    Parameters:
        provider (str): The cloud provider to use. Acceptable values include:
            - 'aws': Amazon Web Services
            - 'azure': Microsoft Azure
            - 'gcp': Google Cloud Platform
        
        environment (str): The environment for the database connection, e.g., 'prod' or 'dev'.
        
        hostname (str): The hostname or IP address of the database server.
        
        port (int): The port number for the database connection.
        
        username (str): The username for authentication with the database.
        
        region (str): The cloud provider region where the database is hosted (e.g., 'us-west-2' for AWS, 'eastus' for Azure).
        
        dbname (str): The name of the database to connect to.
        
        connection_string (str, optional): The connection string for Azure databases. This parameter is required for Azure providers.

    Returns:
        CloudDB: An instance of the appropriate cloud database service (AWS, Azure, or GCP) based on the provided provider.

    Raises:
        ValueError: If the specified provider is unsupported, or if required parameters for the provider are missing.

    Examples:
        >>> aws_service = get_cloud_db_service(
        ...     'aws', 
        ...     environment='prod', 
        ...     hostname='aws_host', 
        ...     port=3306, 
        ...     username='user', 
        ...     region='us-west-2', 
        ...     dbname='my_db'
        ... )
        >>> azure_service = get_cloud_db_service(
        ...     'azure', 
        ...     connection_string='your_connection_string', 
        ...     environment='prod', 
        ...     hostname='azure_host', 
        ...     port=1433, 
        ...     username='user', 
        ...     region='eastus', 
        ...     dbname='my_db'
        ... )
        >>> gcp_service = get_cloud_db_service(
        ...     'gcp', 
        ...     environment='prod', 
        ...     hostname='gcp_host', 
        ...     port=5432, 
        ...     username='user', 
        ...     region='us-central1', 
        ...     dbname='my_db'
        ... )

    Notes:
        - Ensure that the required dependencies for the selected cloud provider are installed and configured properly.
    
    See Also:
        - AWSDB
        - AzureDB
        - GCPDB
    """