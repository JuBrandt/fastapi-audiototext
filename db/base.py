import databases
import sqlalchemy

from core.config import DATABASE_URL



metadata = sqlalchemy.MetaData()
database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(DATABASE_URL)