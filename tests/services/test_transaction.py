import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, cast
from unittest.mock import Mock, create_autospec

import pytest
from fastapi import HTTPException

from app.dbmodel.transaction import Transaction
from app.repository.transaction_repository import TransactionRepository
from app.services.transaction import TransactionService
from app.viewmodel.transaction import FilterTransactions, TransactionBase
from app.viewmodel.user import UserResponse

# ---------- Fixtures ----------

@pytest.fixture
def mock_repository() -> Any:
    """Provides a fully mocked TransactionRepository."""
    return create_autospec(TransactionRepository, instance=True)


@pytest.fixture
def transaction_service(mock_repository: Any) -> TransactionService:
    """Provides a TransactionService with a mocked repository."""
    return TransactionService(repository=mock_repository)


@pytest.fixture
def test_user() -> UserResponse:
    """A consistent test user."""
    return UserResponse(
        id=uuid.uuid4(),
        username="testuser",
        email="test@example.com",
        full_name="Test User",
    )


@pytest.fixture
def sample_transaction() -> Transaction:
    """A deterministic transaction record."""
    fixed_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    return Transaction(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        amount=Decimal("100.50"),
        occurred_on=fixed_time,
        description="Test transaction",
        currency="USD",
        category_id=uuid.uuid4(),
        created_at=fixed_time,
    )


# ---------- Tests: read_transactions ----------

def test_read_transactions_success(
    transaction_service: TransactionService,
    test_user: UserResponse,
    sample_transaction: Transaction,
) -> None:
    mock_repo = transaction_service.repository
    mock_repo.get_user_transactions.return_value = [sample_transaction] # type: ignore
    filter_query = FilterTransactions()  # currently unused

    result = transaction_service.read_transactions(test_user, filter_query)

    assert len(result) == 1
    tx = result[0]
    assert tx.amount == sample_transaction.amount
    assert tx.description == sample_transaction.description
    cast(Mock, mock_repo.get_user_transactions).assert_called_once_with(test_user.id)


def test_read_transactions_empty(
    transaction_service: TransactionService,
    test_user: UserResponse,
) -> None:
    mock_repo = transaction_service.repository
    mock_repo.get_user_transactions.return_value = [] # type: ignore
    filter_query = FilterTransactions()

    result = transaction_service.read_transactions(test_user, filter_query)

    assert result == []
    cast(Mock, mock_repo.get_user_transactions).assert_called_once_with(test_user.id)


# ---------- Tests: read_transaction ----------

def test_read_transaction_success(
    transaction_service: TransactionService,
    test_user: UserResponse,
    sample_transaction: Transaction,
) -> None:
    mock_repo = transaction_service.repository
    mock_repo.get_user_transaction.return_value = sample_transaction # type: ignore

    result = transaction_service.read_transaction(test_user, sample_transaction.id)

    assert result.id == sample_transaction.id
    assert result.amount == sample_transaction.amount
    assert result.description == sample_transaction.description
    cast(Mock, mock_repo.get_user_transaction).assert_called_once_with(test_user.id, sample_transaction.id)


def test_read_transaction_not_found(
    transaction_service: TransactionService,
    test_user: UserResponse,
) -> None:
    mock_repo = transaction_service.repository
    mock_repo.get_user_transaction.return_value = None # type: ignore
    tx_id = uuid.uuid4()

    with pytest.raises(HTTPException) as exc_info:
        transaction_service.read_transaction(test_user, tx_id)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Transaction not found"
    cast(Mock, mock_repo.get_user_transaction).assert_called_once_with(test_user.id, tx_id)


# ---------- Tests: create_transaction ----------

def test_create_transaction_success(
    transaction_service: TransactionService,
    test_user: UserResponse,
    sample_transaction: Transaction,
) -> None:
    mock_repo = transaction_service.repository
    mock_repo.insert_transaction.return_value = sample_transaction # type: ignore

    tx_base = TransactionBase(
        amount=sample_transaction.amount,
        occurred_on=sample_transaction.occurred_on,
        description=sample_transaction.description,
        currency=sample_transaction.currency,
        category_id=sample_transaction.category_id,
        created_at=sample_transaction.created_at,
    )

    result = transaction_service.create_transaction(test_user, tx_base)

    assert result.amount == tx_base.amount
    assert result.description == tx_base.description
    cast(Mock, mock_repo.insert_transaction).assert_called_once()
    # Optional deeper check:
    args, _ = cast(Mock, mock_repo.insert_transaction).call_args
    assert args[0].user_id == test_user.id


# ---------- Tests: remove_transaction ----------

def test_remove_transaction_success(
    transaction_service: TransactionService,
    test_user: UserResponse,
) -> None:
    mock_repo = transaction_service.repository
    cast(Mock, mock_repo.delete_transaction).return_value = 1
    tx_id = uuid.uuid4()

    transaction_service.remove_transaction(test_user, tx_id)

    cast(Mock, mock_repo.delete_transaction).assert_called_once_with(test_user.id, tx_id)


def test_remove_transaction_not_found(
    transaction_service: TransactionService,
    test_user: UserResponse,
) -> None:
    mock_repo = transaction_service.repository
    mock_repo.delete_transaction.return_value = 0 # type: ignore
    tx_id = uuid.uuid4()

    with pytest.raises(HTTPException) as exc_info:
        transaction_service.remove_transaction(test_user, tx_id)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Transaction not found"
    cast(Mock, mock_repo.delete_transaction).assert_called_once_with(test_user.id, tx_id)

# ---------- Tests: mappers ----------

def test_transaction_to_response(
    sample_transaction: Transaction,
) -> None:
    from app.services.transaction import transaction_to_response

    result = transaction_to_response(sample_transaction)

    assert result.id == sample_transaction.id
    assert result.amount == sample_transaction.amount
    assert result.description == sample_transaction.description
    assert result.occurred_on == sample_transaction.occurred_on
    assert result.currency == sample_transaction.currency
    assert result.category_id == sample_transaction.category_id
    assert result.created_at == sample_transaction.created_at
    
def test_base_to_transaction(
    sample_transaction: Transaction,
) -> None:
    from app.services.transaction import TransactionBase, base_to_transaction

    tx_base = TransactionBase(
        amount=sample_transaction.amount,
        occurred_on=sample_transaction.occurred_on,
        description=sample_transaction.description,
        currency=sample_transaction.currency,
        category_id=sample_transaction.category_id,
        created_at=sample_transaction.created_at,
    )

    user_id = uuid.uuid4()
    result = base_to_transaction(user_id, tx_base)

    assert result.user_id == user_id
    assert result.amount == tx_base.amount
    assert result.description == tx_base.description
    assert result.occurred_on == tx_base.occurred_on
    assert result.currency == tx_base.currency
    assert result.category_id == tx_base.category_id
    assert result.created_at == tx_base.created_at