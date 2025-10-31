import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def update_schema():
    """Update database schema for OAuth support"""
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'wps_office'),
        'port': os.getenv('DB_PORT', '3306')
    }
    
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # Add google_id column if it doesn't exist
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'users' AND COLUMN_NAME = 'google_id'
        """, (config['database'],))
        
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE users ADD COLUMN google_id VARCHAR(255) NULL AFTER password_hash")
            print("✅ Added google_id column to users table")
        
        # Create index for google_id
        cursor.execute("""
            SELECT INDEX_NAME 
            FROM INFORMATION_SCHEMA.STATISTICS 
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'users' AND INDEX_NAME = 'idx_google_id'
        """, (config['database'],))
        
        if not cursor.fetchone():
            cursor.execute("CREATE UNIQUE INDEX idx_google_id ON users(google_id)")
            print("✅ Created idx_google_id index")
        
        connection.commit()
        print("✅ Database schema updated successfully for OAuth")
        
    except Error as e:
        print(f"❌ Error updating schema: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    update_schema()