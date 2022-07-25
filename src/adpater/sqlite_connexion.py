import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(
    os.environ.get('SQLALCHEMY_DATABASE_URI'), 
    echo=False, future=True)

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    """
    import all model in here
    """
    import src.domain.model
    Base.metadata.create_all(bind=engine)

