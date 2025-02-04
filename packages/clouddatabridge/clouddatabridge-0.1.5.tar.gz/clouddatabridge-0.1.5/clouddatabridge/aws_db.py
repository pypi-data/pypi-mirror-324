import pymysql
import boto3
import time

class AWSRDSConnection:
    """
    A class to manage a connection to an AWS RDS MySQL database.

    This class provides methods to establish a connection to an AWS RDS instance, generate an authentication token, 
    and manage the connection lifecycle, including automatic retries for connection attempts.

    Attributes:
        host (str): The hostname of the RDS instance.
        user (str): The username used to authenticate with the database.
        database (str): The name of the database to connect to.
        region (str): The AWS region where the RDS instance is located.
        port (int): The port number for the database connection (default is 3306).
        db_connection: The database connection object (initially None).
    """
    def __init__(self, host, user, database, region, port=3306):
        """
        Initializes the AWSRDSConnection with the specified parameters.

        Parameters:
            host (str): The hostname of the RDS instance.
            user (str): The username for the database connection.
            database (str): The name of the database.
            region (str): The AWS region for the RDS instance.
            port (int, optional): The port for the connection. Defaults to 3306.
        """
        self.host = host
        self.user = user
        self.database = database
        self.region = region
        self.port = port
        self.db_connection = None

    def create_connection_token(self):
        """
        Generates an authentication token for connecting to AWS RDS.

        This token is used in place of a password for authentication to enhance security.

        Returns:
            str: The generated authentication token for the RDS instance.

        Raises:
            Exception: If there is an error generating the token.
        """
        client = boto3.client('rds', region_name=self.region)
        return client.generate_db_auth_token(
            DBHostname=self.host,
            Port=self.port,
            DBUsername=self.user,
            Region=self.region
        )

    def get_db_connection(self, max_retries=5, retry_delay=5):
        """
        Establishes a connection to the AWS RDS database with retry logic.

        This method attempts to connect to the database up to a specified number of retries. 
        If the connection is successful, it returns the connection object; otherwise, it returns an error.

        Parameters:
            max_retries (int, optional): Maximum number of connection attempts. Defaults to 5.
            retry_delay (int, optional): Delay in seconds between retries. Defaults to 5.

        Returns:
            pymysql.Connection: A connection object to the database if successful.

        Raises:
            pymysql.OperationalError: If the connection fails after the maximum number of retries.
        """
        if self.db_connection and self.db_connection.open:
            return self.db_connection

        retries = 0
        while retries < max_retries:
            try:
                self.db_connection = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.create_connection_token(),
                    password=self.password,
                    db=self.database,
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor,
                    ssl={"use": True}
                )
                return self.db_connection

            except pymysql.OperationalError as e:
                retries += 1
                print(f"OperationalError: {e}. Retrying {retries}/{max_retries}...")
                time.sleep(retry_delay)

        return pymysql.OperationalError(f"Failed to connect to the database after {max_retries} retries.")

    def close_connection(self):
        """
        Closes the database connection if it is open.

        This method ensures that the connection is properly closed and sets the connection object to None.
        """
        if self.db_connection:
            self.db_connection.close()
            self.db_connection = None
