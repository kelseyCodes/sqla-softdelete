import pytest
import sqlalchemy as sa

from sqlalchemy.ext.declarative import declarative_base

from sqla_softdelete import SoftDeleteMixin
from tests.database import engine, Session

Base = declarative_base()

class Account(SoftDeleteMixin, Base):
    __tablename__ = 'account'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.Text, nullable=False)
    email = sa.Column(sa.String(128), nullable=True, index=True)


@pytest.fixture(scope='session', autouse=True)
def db():
    """session wide test database"""
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(scope='function', autouse=True)
def test_session():
    """creates a new db session for a test"""
    session = Session()
    # Making sure nothing commits
    try:
        yield session
    finally:
        session.rollback()
        reset_tables()
        session.close()
        Session.remove()


def reset_tables():
    """Clears all tables between tests.

    This allows tests to be isolated from each other
    preventing cross-contamination of test state while
    still allowing the tests to run fast
    """
    session = Session()
    meta = Base.metadata
    for table in meta.sorted_tables:
        session.execute(table.delete())
    session.commit()
