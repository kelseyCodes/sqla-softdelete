from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DB_URL = 'postgresql://sqla-user:@localhost:5432/sqla-softdelete-test'
engine = create_engine(DB_URL)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
