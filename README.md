# sqla-softdelete
Simple soft delete for SQLAlchemy ORM

How to install
------------  
```
  pip install sqla-softdelete
```

How to use
------------    
To make your SQLAlchemy model support soft deletes, just inherit from `SoftDeleteMixin`.

## Example Class Creation

```python
from sqlalchemy.ext.declarative import declarative_base
from sqla_softdelete import SoftDeleteMixin

Base = declarative_base()

class Account(SoftDeleteMixin, Base):
    __tablename__ = 'account'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.Text, nullable=False)
    email = sa.Column(sa.String(128), nullable=False, index=True)

```

## Example Usage

### Fetching Non-Deleted Data

(Soft) Deleted accounts will automatically be excluded from query results.
```python
    account = Account(name='account')

    Session.add(account)
    Session.commit()

    actual_accounts = Session.query(Account).all()
    print(f'Actual accounts: {actual_accounts}')
```

(Soft) Deleted accounts will automatically be excluded when fetching via `get`.
```python
    account = Account(name='account')

    Session.add(account)
    Session.commit()

    actual_account = Account.get(Session, account.id)
    print(f'Actual accounts: {actual_account}')
```

### Fetching All Data

(Soft) Deleted accounts will be included from query results when `execution_options` are passed.
```python
    account = Account(name='account')

    Session.add(account)
    account.delete()
    Session.commit()

    actual_accounts = Session.query(Account).execution_options(include_deleted=True).all()
    print(f'Actual accounts: {actual_accounts}')
```

(Soft) Deleted accounts will be included when fetching via `get` with `include_deleted = True`.
```python
    account = Account(name='account')

    Session.add(account)
    account.delete()
    Session.commit()

    actual_account = Account.get(Session, account.id, True)
    print(f'Actual accounts: {actual_account}')
```

### Deleting Data
Deleting accounts is easy: call `delete` on the account object, with or without passing a `session`. If the session is passed, it will commit the changes to the database. The `deleted_at` date can also be passed; otherwise, `deleted_at` defaults to use the current time in UTC.
```python
    account = Account(name='account')

    Session.add(account)
    Session.commit()

    account.delete(Session)

    actual_account = Account.get(Session, account.id)
    print(f'Actual accounts: {actual_account}')
```
In the above example, `actual_account` will return `None`.

Additionally, this can be done using the normal sqlalchemey update syntax.
```python
    account = Account(name='account')

    Session.add(account)
    account.deleted_at = datetime.utcnow()
    Session.commit()


    actual_account = Account.get(Session, account.id)
    print(f'Actual accounts: {actual_account}')
```
This will also return `None`.

### Restoring Data
Restoring accounts is easy: call `restore` on the account object, with or without passing a `session`. If the session is passed, it will commit the changes to the database.
```python
    account = Account(name='account')

    Session.add(account)
    account.delete()
    account.restore()
    Session.commit()

    actual_account = Account.get(Session, account.id)
    print(f'Actual accounts: {actual_account}')
```
In the above example, `actual_account` will return the row and `deleted_at` will be `y`.

Additionally, this can be done using the normal sqlalchemey update syntax.
```python
    account = Account(name='account')

    Session.add(account)
    account.delete()
    account.deleted_at = None
    Session.commit()


    actual_account = Account.get(Session, account.id)
    print(f'Actual accounts: {actual_account}')
```
This will also return the restored row.
