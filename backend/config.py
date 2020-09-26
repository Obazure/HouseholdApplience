import os

BACKEND_PORT = int(os.getenv('BACKEND_PORT', '8000'))

THEGUARDIANCOM_API_TOKEN = os.getenv('THEGUARDIANCOM_API_TOKEN', 'test')

DB_DRIVER = os.getenv('DB_DRIVER', 'mysql+mysqldb')
DB_USER = os.getenv('MYSQL_USER', 'test')
DB_PASSWORD = os.getenv('MYSQL_PASSWORD', 'test')
DB_NAME = os.getenv('MYSQL_DATABASE', 'test')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')

SQLALCHEMY_DATABASE_URL = "%s://%s:%s@%s:%s/%s" % (DB_DRIVER, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)


NLTK_DATA_PATH = os.path.abspath(os.path.join(__file__, "../lib/nltk_data/"))