from dotenv import load_dotenv 
import os
import pyodbc


load_dotenv()


# Retrieve environment variables
server   = os.environ.get('SERVER')
database = os.environ.get('DATABASE')
username = os.environ.get('ADMINUSER')
password = os.environ.get('PASSWORD')

# Print environment variables for debugging
print(f"Server: {server}")
print(f"Database: {database}")
print(f"Username: {username}")

# Construct connection string
connectionString = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"


# Connect to the database
try:
    conn = pyodbc.connect(connectionString)
    print("Connected successfully!")
    # Add your further code here
except Exception as e:
    print(f"Error connecting to the database: {e}")