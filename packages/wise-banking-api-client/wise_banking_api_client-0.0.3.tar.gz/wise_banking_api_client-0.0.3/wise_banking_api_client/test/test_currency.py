"""Test the currencies and the endpoint."""

from wise_banking_api_client.model.currency import Currency


def test_currency_has_code():
    """Test that we have the currencies available."""
    assert Currency.AED.code == "AED"


def test_get_all_currencies():
    """Make sure the list is not empty."""
    assert Currency.ARS in Currency.all_currencies()


def get_all_currencies(sandbox):
    """We get all currencies."""
