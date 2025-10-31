import mysql.connector
from mysql.connector import Error, pooling
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    _connection_pool = None
    
    @classmethod
    def initialize_pool(cls):
        """Initialize connection pool"""
        try:
            cls._connection_pool = pooling.MySQLConnectionPool(
                pool_name="wps_pool",
                pool_size=5,
                host=os.getenv('DB_HOST', 'localhost'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', ''),
                database=os.getenv('DB_NAME', 'wps_office'),
                port=os.getenv('DB_PORT', '3306'),
                autocommit=True
            )
            logger.info("Database connection pool initialized successfully")
        except Error as e:
            logger.error(f"Error initializing connection pool: {e}")
            raise
    
    @classmethod
    def get_connection(cls):
        """Get connection from pool"""
        if cls._connection_pool is None:
            cls.initialize_pool()
        
        try:
            connection = cls._connection_pool.get_connection()
            if connection.is_connected():
                return connection
        except Error as e:
            logger.error(f"Error getting connection from pool: {e}")
            raise
    
    @classmethod
    def execute_query(cls, query, params=None, fetch=False):
        """Execute query and return results if fetch=True"""
        connection = None
        cursor = None
        try:
            connection = cls.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
                return result
            else:
                connection.commit()
                return cursor.rowcount
                
        except Error as e:
            logger.error(f"Error executing query: {e}")
            if connection:
                connection.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @classmethod
    def execute_single_query(cls, query, params=None):
        """Execute query and return single result"""
        connection = None
        cursor = None
        try:
            connection = cls.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            cursor.execute(query, params or ())
            result = cursor.fetchone()
            return result
                
        except Error as e:
            logger.error(f"Error executing single query: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

# Initialize pool when module is imported
Database.initialize_pool()