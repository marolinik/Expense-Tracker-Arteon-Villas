"""
PostgreSQL Database Setup Script for Arteon Villas Expense Tracker

This script helps set up the PostgreSQL database for the application.
Run this before running init_db.py
"""

import psycopg2
from psycopg2 import sql
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_database():
    """Create the PostgreSQL database if it doesn't exist"""
    
    # Get connection parameters from environment or use defaults
    db_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/arteon_villas_expenses')
    
    # Parse the database URL
    try:
        # Extract components from URL
        parts = db_url.replace('postgresql://', '').split('@')
        user_pass = parts[0].split(':')
        host_port_db = parts[1].split('/')
        host_port = host_port_db[0].split(':')
        
        username = user_pass[0]
        password = user_pass[1] if len(user_pass) > 1 else ''
        host = host_port[0]
        port = host_port[1] if len(host_port) > 1 else '5432'
        database_name = host_port_db[1]
        
    except Exception as e:
        print(f"Error parsing database URL: {e}")
        print("Please check your DATABASE_URL format")
        return False
    
    try:
        # Connect to PostgreSQL server (not to a specific database)
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database='postgres'  # Connect to default postgres database
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (database_name,)
        )
        exists = cursor.fetchone()
        
        if not exists:
            # Create database
            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(database_name)
                )
            )
            print(f"✓ Database '{database_name}' created successfully!")
        else:
            print(f"✓ Database '{database_name}' already exists.")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"✗ Could not connect to PostgreSQL server: {e}")
        print("\nPlease ensure:")
        print("1. PostgreSQL is installed and running")
        print("2. The connection details in your .env file are correct")
        print("3. The PostgreSQL user has permission to create databases")
        return False
        
    except Exception as e:
        print(f"✗ An error occurred: {e}")
        return False

def test_connection():
    """Test the database connection"""
    db_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/arteon_villas_expenses')
    
    try:
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"✓ Successfully connected to PostgreSQL!")
        print(f"  PostgreSQL version: {version}")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Could not connect to database: {e}")
        return False

if __name__ == "__main__":
    print("PostgreSQL Database Setup for Arteon Villas Expense Tracker")
    print("=" * 55)
    
    # Create database
    if create_database():
        print("\nTesting database connection...")
        if test_connection():
            print("\n✓ Database setup complete!")
            print("You can now run 'python init_db.py' to initialize the tables and users.")
        else:
            print("\n✗ Database connection test failed.")
            print("Please check your configuration and try again.")
    else:
        print("\n✗ Database setup failed.")
        print("Please fix the issues above and try again.") 