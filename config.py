import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
JWT_SECRET = os.getenv('JWT_SECRET')
MANAGER_SECRET = os.getenv('MANAGER_SECRET')
