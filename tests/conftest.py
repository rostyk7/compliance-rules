import pytest
from compliance_rules import ScreeningRequest


@pytest.fixture
def make_request():
    def _make(**kwargs) -> ScreeningRequest:
        defaults = dict(
            order_id="order-123",
            customer_email="user@example.com",
            amount=5000,
            currency="USD",
            card_token="tok_abc",
        )
        return ScreeningRequest(**{**defaults, **kwargs})
    return _make
