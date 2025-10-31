import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', '')
        self.database = os.getenv('DB_NAME', 'wps_office')
        self.port = os.getenv('DB_PORT', '3306')

def create_database():
    """Create database and tables"""
    config = DatabaseConfig()
    
    try:
        # Connect without specifying database first
        connection = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            port=config.port
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config.database}")
            print(f"Database '{config.database}' created successfully")
            
            # Use the database
            cursor.execute(f"USE {config.database}")
            
            # Create tables
            tables_sql = [
                """
                CREATE TABLE IF NOT EXISTS users (
                    id VARCHAR(36) PRIMARY KEY,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS documents (
                    id VARCHAR(36) PRIMARY KEY,
                    user_id VARCHAR(36) NOT NULL,
                    title VARCHAR(500) NOT NULL,
                    document_type ENUM('writer', 'spreadsheet', 'presentation', 'pdf') NOT NULL,
                    content JSON,
                    file_path VARCHAR(500),
                    file_size BIGINT,
                    version INT DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    INDEX idx_user_id (user_id),
                    INDEX idx_document_type (document_type)
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS document_collaborators (
                    id VARCHAR(36) PRIMARY KEY,
                    document_id VARCHAR(36) NOT NULL,
                    user_id VARCHAR(36) NOT NULL,
                    permission_level ENUM('view', 'comment', 'edit') DEFAULT 'view',
                    invited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    UNIQUE KEY unique_document_user (document_id, user_id)
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS document_versions (
                    id VARCHAR(36) PRIMARY KEY,
                    document_id VARCHAR(36) NOT NULL,
                    version_number INT NOT NULL,
                    content JSON,
                    created_by VARCHAR(36) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    change_description TEXT,
                    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE,
                    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE,
                    INDEX idx_document_version (document_id, version_number)
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS ai_processing_history (
                    id VARCHAR(36) PRIMARY KEY,
                    document_id VARCHAR(36) NOT NULL,
                    user_id VARCHAR(36) NOT NULL,
                    ai_action VARCHAR(100) NOT NULL,
                    input_data JSON,
                    output_data JSON,
                    processing_time_ms INT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS user_settings (
                    user_id VARCHAR(36) PRIMARY KEY,
                    theme VARCHAR(50) DEFAULT 'light',
                    language VARCHAR(10) DEFAULT 'en',
                    auto_save BOOLEAN DEFAULT TRUE,
                    ai_assistance BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
                """
            ]
            
            for sql in tables_sql:
                cursor.execute(sql)
            
            # Insert sample data
            sample_data_sql = [
                """
                INSERT IGNORE INTO users (id, email, name, password_hash) 
                VALUES 
                ('user1', 'demo@wps.com', 'Demo User', '$2b$12$examplehashedpassword'),
                ('user2', 'test@wps.com', 'Test User', '$2b$12$examplehashedpassword2')
                """,
                """
                INSERT IGNORE INTO user_settings (user_id) 
                VALUES ('user1'), ('user2')
                """,
                """
                INSERT IGNORE INTO documents (id, user_id, title, document_type, content) 
                VALUES 
                ('doc1', 'user1', 'Sample Document', 'writer', '{"type": "doc", "content": [{"type": "paragraph", "content": [{"text": "Welcome to WPS Office!", "type": "text"}]}]}'),
                ('doc2', 'user1', 'Budget Spreadsheet', 'spreadsheet', '{"sheets": [{"name": "Sheet1", "data": [["Item", "Cost"], ["Laptop", "1000"], ["Software", "200"]]}]}'),
                ('doc3', 'user2', 'Project Presentation', 'presentation', '{"slides": [{"id": 1, "title": "Project Overview", "content": "Team collaboration platform", "layout": "title"}]}')
                """
            ]
            
            for sql in sample_data_sql:
                try:
                    cursor.execute(sql)
                except Error as e:
                    print(f"Error inserting sample data: {e}")
            
            connection.commit()
            print("All tables created successfully")
            
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    create_database()