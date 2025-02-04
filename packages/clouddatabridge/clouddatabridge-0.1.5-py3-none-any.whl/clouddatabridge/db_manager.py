from .local_db import LocalDBConnection
from .aws_db import AWSRDSConnection
from .azure_db import AzureSQLConnection 
from .gcp_db import GCPMySQLConnection

def create_db_connection(service, host=None, user=None, password=None, database=None, port=3306, region=None):
    """
    Creates a database connection for either a local or cloud database (AWS, Azure, GCP).

    Based on the `service` parameter, this function establishes a connection to a specified database service 
    by returning a connection object for local, AWS, Azure, or GCP databases. Each cloud provider may have 
    additional requirements, such as an AWS region for RDS connections.

    Parameters:
        service (str): Type of database connection. Accepted values are 'local', 'aws', 'azure', 'gcp'.
        host (str, optional): Database server hostname or IP address.
        user (str, optional): Database username for authentication.
        password (str, optional): Database password for authentication.
        database (str, optional): Name of the target database.
        port (int, optional): Port number for the database connection, default is 3306.
        region (str, optional): AWS region for an RDS connection; required only if `service` is 'aws'.

    Returns:
        Connection object: Returns an instance of LocalDBConnection, AWSRDSConnection, AzureSQLConnection, 
                           or GCPMySQLConnection depending on `service` specified.

    Raises:
        ValueError: If the `service` parameter is invalid or if required parameters are missing:
                    - Unsupported values for `service` outside ['local', 'aws', 'azure', 'gcp'].
                    - Missing `region` for an AWS RDS connection.

    Examples:
        >>> # Create a local database connection
        >>> connection = create_db_connection('local', host='localhost', user='user', password='pass', database='test_db')

        >>> # Create an AWS RDS connection
        >>> connection = create_db_connection('aws', host='db-instance.123456789012.us-east-1.rds.amazonaws.com', 
                                              user='admin', password='pass', database='test_db', region='us-east-1')

        >>> # Create an Azure SQL Database connection
        >>> connection = create_db_connection('azure', host='azure-sql.database.windows.net', user='azure_user', 
                                              password='azure_pass', database='azure_db', port=1433)

        >>> # Create a GCP MySQL connection
        >>> connection = create_db_connection('gcp', host='gcp-mysql-instance.123456789012.us-central1', 
                                              user='gcp_user', password='gcp_pass', database='gcp_db')
    """
    if service not in ['local', 'aws', 'azure', 'gcp']:
        return ValueError(f"Unsupported cloud provider: '{service}'. Supported providers: aws, azure, gcp, local")

    if service == "local":
        return LocalDBConnection(host, user, password, database, port)
    elif service == "aws":
        if not region:
            return ValueError("Region is required for AWS connection.")
        return AWSRDSConnection(host, user, database, region, port)
    elif service == "azure":
        return AzureSQLConnection(host, user, database, password, port)
    elif service == "gcp":
        return GCPMySQLConnection(host, user, password, database, port)
    else:
        raise ValueError("Unsupported service type. Use 'local', 'aws', 'azure', 'gcp'.")