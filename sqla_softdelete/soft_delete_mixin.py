from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import event
from sqlalchemy import inspect
from sqlalchemy.orm import Query, Session


class SoftDeleteMixin:
    deleted_at = sa.Column(sa.DateTime, default=None, nullable=True)

    def delete(self, session=None, deleted_at: datetime=datetime.utcnow()):
        """
        Args:
            session (sqlalchemy.orm.Session, optional): optioanlly takes a session object.
                If provided, will commit the changes to the database.
            deleted_at (datetime, optional): optionally takes the deleted_at date. Defaults
                to the current time in UTC.
        Example usage:
            account1.delete(session) -> deleted_at set to datetime.utcnow() and commited to database
            account1.delete(deleted_at=datetime(2020,1,1)) -> deleted at set to Jan 1, 2020 and
                committing to the database is handled by the caller
        """
        self.deleted_at = deleted_at or datetime.utcnow()
        if session:
            session.commit()

    def restore(self, session=None):
        """
        Args:
            session (sqlalchemy.orm.Session, optional): optioanlly takes a session object.
                If provided, will commit the changes to the database.
        Example usage:
            account1.restore(session) -> deleted_at set to None and commited to database
            account1.restore() -> deleted at set to None and committing handled by the caller
        """
        self.deleted_at = None
        if session:
            session.commit()

    @classmethod
    def get(cls, session, row_id, include_deleted=False):
        """
        Args:
            session (sqlalchemy.orm.Session): takes a session object.
            row_id (int): the id of the row that should be fetched from the database
            include_deleted (bool, optional): defaults to False to exclude deleted rows. If
                passed an id of a deleted row, will return None. If passed include_deleted=True,
                will return the deleted row.
        Example usage:
            Account.get(session, 1) -> if row with id 1 is not deleted, will return the row. Otherwise,
                will return None.
            Account.get(session, 1, True) -> will return the row regardless of whether it's been deleted
        """
        query = session.query(cls).filter(cls.id == row_id)
        if include_deleted:
            query = query.execution_options(include_deleted=True)
        return query.first()

@event.listens_for(Query, 'before_compile', retval=True)
def before_compile(query):
    """
    Args:
        query (sqlalchemy.orm.query.Query) takes a sqlalchemy query object.
    Example usage:
       session.query(Account).all() -> returns all non-deleted accounts
       session.query(Account).execution_options(include_deleted=True).all() -> returns
           all accounts, including deleted accounts
    """
    include_deleted = query._execution_options.get('include_deleted', False)
    if include_deleted:
        return query
    for column in query.column_descriptions:
        entity = column['entity']
        if entity is None:
            continue

        inspector = inspect(column['entity'])
        mapper = getattr(inspector, 'mapper', None)
        if mapper and issubclass(mapper.class_, SoftDeleteMixin):
            query = query.enable_assertions(False).filter(
                entity.deleted_at.is_(None),
            )

    return query
