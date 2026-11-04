import os 
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

def conexao ():
    return psycopg.connect(
    user= os.environ["DB_USER"],
    password= os.environ["DB_PASSWORD"],
    host= os.environ["DB_HOST"],
    dbname= os.environ["DB_NAME"],
    row_factory=dict_row
)