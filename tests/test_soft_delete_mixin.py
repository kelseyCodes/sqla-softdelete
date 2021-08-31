from datetime import datetime

import pytest
from sqlalchemy.orm.exc import ObjectDeletedError

from tests.conftest import Account


class TestSoftDeleteMixin:

    @pytest.fixture(scope='function')
    def account1(self, test_session):
        account1 = Account(name='account1')
        test_session.add(account1)
        test_session.commit()

        return account1

    @pytest.fixture(scope='function')
    def account2(self, test_session):
        account2 = Account(name='account2')
        test_session.add(account2)
        test_session.commit()

        return account2

    @pytest.fixture(scope='function')
    def account3(self, test_session):
        account3 = Account(name='account3')
        test_session.add(account3)
        test_session.commit()

        return account3

    def test_query_all(self, test_session, account1, account2, account3):
        import pdb; pdb.set_trace()
        actual_accounts = test_session.query(Account).all()
        assert set(actual_accounts) == {account1, account2, account3}

    def test_get_all_not_deleted(self, test_session, account1, account2):
        account1.delete(test_session)

        actual_accounts = test_session.query(Account).all()
        assert actual_accounts == [account2]


    def test_filter_not_deleted(self, test_session, account1, account2, account3):
        account1.delete(test_session)

        actual_accounts = test_session.query(Account).filter(Account.name == 'account2').all()
        assert actual_accounts == [account2]

    def test_get_not_deleted(self, test_session, account1):
        actual_account = Account.get(test_session, account1.id)

        assert actual_account == account1

    def test_get_deleted(self, test_session, account1):
        account1.delete(test_session)
        deleted_account =Account.get(test_session, account1.id)

        assert deleted_account is None

    def test_get_deleted_with_include_deleted(self, test_session, account1):
        account1.delete(test_session)

        deleted_account = Account.get(test_session, account1.id, True)
        assert deleted_account == account1
        assert deleted_account.deleted_at is not None

    def test_get_deleted_no_session(self, test_session, account1):
        account1.delete()
        test_session.commit()

        deleted_account = Account.get(test_session, account1.id, True)
        assert deleted_account == account1
        assert deleted_account.deleted_at is not None

    def test_restore(self, test_session, account1):
        account1.delete(test_session)
        account1.restore(test_session)

        restored_account = Account.get(test_session, account1.id)
        assert restored_account == account1
        assert restored_account.deleted_at is None

    def test_query_all_after_restore(self, test_session, account1, account2, account3):
        account1.delete(test_session)
        account1.restore(test_session)

        actual_accounts = test_session.query(Account).all()
        assert len(actual_accounts) == 3
        assert all([acc.deleted_at == None for acc in actual_accounts]) is True

    def test_get_restored_no_session(self, test_session, account1):
        account1.delete(test_session)
        account1.restore()
        test_session.commit()

        deleted_account = Account.get(test_session, account1.id)
        assert deleted_account == account1
        assert deleted_account.deleted_at is None

    def test_update_to_deleted(self, test_session, account1):
        account1.deleted_at = datetime.utcnow()
        test_session.commit()

        get_response = Account.get(test_session, account1.id)
        deleted_account = Account.get(test_session, account1.id, True)
        assert get_response is None
        assert deleted_account is not None
        assert deleted_account is not None

    def test_update_to_restored(self, test_session, account1):
        account1.delete(test_session)
        account1.deleted_at = None
        test_session.commit()

        actual_account = Account.get(test_session, account1.id)
        assert actual_account is not None
        assert actual_account.deleted_at is None
