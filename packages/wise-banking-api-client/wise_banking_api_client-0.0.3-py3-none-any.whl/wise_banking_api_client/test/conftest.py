"""pytest configuration

You can add responses by running this in your codebase:

    from wise_banking_api_client.test import record

    record()
    # do API requests
    record("name-of-endpoint")

"""

import os
from collections.abc import Generator
from unittest.mock import MagicMock

import pytest
from munch import Munch

from wise_banking_api_client import Client
from wise_banking_api_client.client import DEFAULT_PRIVATE_KEY, DEFAULT_PUBLIC_KEY
from wise_banking_api_client.endpoint import WiseAPIError
from wise_banking_api_client.model.account import (
    AccountRequirement,
    RecipientAccountRequirements,
    RecipientAccountResponse,
)
from wise_banking_api_client.model.account_requirement_type import (
    AccountRequirementType,
)
from wise_banking_api_client.model.currency import Currency, CurrencyCode
from wise_banking_api_client.model.legal_type import LegalType
from wise_banking_api_client.model.payment import PaymentResponse
from wise_banking_api_client.model.profile import Profile, Profiles
from wise_banking_api_client.model.quote import (
    ExampleQuoteRequest,
    PaymentMethod,
    QuoteRequest,
    QuoteResponse,
)
from wise_banking_api_client.model.recipient import Recipient
from wise_banking_api_client.model.recipient.details import RecipientDetails
from wise_banking_api_client.model.transfer import (
    TransferDetails,
    TransferRequest,
    TransferResponse,
)
from wise_banking_api_client.test.record import TestClient


@pytest.fixture(scope="package")
def client() -> Generator[Client, None, None]:
    """We return a sandbox client and dispatch all requests.

    The responses are loaded from the RESPONSES directory.

    """
    client = TestClient()
    yield client
    client.stop()


@pytest.fixture(params=Currency.all_currencies())
def currency(request):
    return request.param


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add options to the pytest run."""
    parser.addoption("--api-key", help="Run the tests on the real Wise Sandbox API.", default=None)


@pytest.fixture(scope="session")
def api_token(request: pytest.FixtureRequest) -> str:
    """Return the API token or skip the test."""
    api_token = request.config.getoption("--api-key")
    if api_token is None:
        api_token = os.environ.get("WISE_API_KEY")
    if api_token is None:
        pytest.skip(
            "--api-key option and WISE_API_KEY environment variable not provided, skipping tests."
        )
    return api_token


@pytest.fixture(scope="session")
def sandbox_client(api_token: str) -> Client:
    """The client communicating with the Wise Sandbox API."""
    return Client(api_key=api_token, private_key_file=DEFAULT_PRIVATE_KEY)


@pytest.fixture(scope="session")
def sandbox_profiles(sandbox_client: Client) -> Profiles:
    """Return the profiles from the sandbox."""
    return sandbox_client.profiles.list()


@pytest.fixture(scope="session")
def sandbox_currencies(sandbox_client: Client) -> list[Currency]:
    """Return the profiles from the sandbox."""
    return sandbox_client.currencies.list()


@pytest.fixture(scope="session")
def sandbox_personal_profile(sandbox_profiles: Profiles) -> Profile:
    """A personal profile."""
    if not sandbox_profiles.personal:
        pytest.skip("No personal profile found.")
    return sandbox_profiles.personal[0]


@pytest.fixture(scope="session")
def sandbox_business_profile(sandbox_profiles: Profiles) -> Profile:
    """A personal profile."""
    if not sandbox_profiles.business:
        pytest.skip("No business profile found.")
    return sandbox_profiles.business[0]


@pytest.fixture(scope="session")
def sandbox_personal_balances(
    sandbox_personal_profile: Profile, sandbox_client: Client
) -> list[Munch]:
    """The balances of a personal profile."""
    return sandbox_client.balances.list(profile=sandbox_personal_profile)


@pytest.fixture(scope="session")
def sandbox_requirements_gbp(sandbox_client: Client) -> list[AccountRequirement]:
    return sandbox_client.recipient_accounts.get_requirements_for_currency(
        source=Currency.GBP, target=Currency.GBP, source_amount=100
    )


@pytest.fixture(scope="session")
def example_quote_request() -> ExampleQuoteRequest:
    """An example quote request."""
    return ExampleQuoteRequest(
        sourceCurrency="GBP",
        targetCurrency="USD",
        sourceAmount=None,
        targetAmount=110,
    )


@pytest.fixture(scope="session")
def quote_request() -> QuoteRequest:
    """An example quote request."""
    return QuoteRequest(
        sourceCurrency="GBP",
        targetCurrency="EUR",
        sourceAmount=None,
        targetAmount=110,
        targetAccount=None,
        payOut=PaymentMethod.BANK_TRANSFER,
        preferredPayIn=PaymentMethod.BANK_TRANSFER,
    )


@pytest.fixture(scope="session")
def sandbox_example_quote(
    sandbox_client: Client, example_quote_request: ExampleQuoteRequest
) -> QuoteRequest:
    """An example quote request."""
    return sandbox_client.quotes.example(example_quote_request)


@pytest.fixture
def mock():
    return MagicMock()


@pytest.fixture(scope="session")
def sandbox_email_recipient_request(sandbox_personal_profile: Profile) -> Recipient:
    """The data to request creating a new email recipient."""
    return Recipient(
        currency=CurrencyCode.EUR,
        type=AccountRequirementType.email,
        profile=sandbox_personal_profile.id,
        accountHolderName="John Doe",
        ownedByCustomer=False,
        details=RecipientDetails(email="john@doe.com"),
    )


@pytest.fixture(scope="session")
def sandbox_email_recipient(
    sandbox_client: Client, sandbox_email_recipient_request: Recipient
) -> RecipientAccountResponse:
    """Create an email recipient."""
    answer = sandbox_client.recipient_accounts.create_recipient(sandbox_email_recipient_request)
    print(answer.model_dump_json(indent=4))
    return sandbox_client.recipient_accounts.get(answer)


@pytest.fixture(scope="session")
def sandbox_iban_recipient_request(sandbox_business_profile: Profile) -> Recipient:
    """The data to request creating a new email recipient."""
    return Recipient(
        currency=CurrencyCode.EUR,
        type=AccountRequirementType.iban,
        profile=sandbox_business_profile.id,
        accountHolderName="Max Mustermann",
        ownedByCustomer=False,
        details=RecipientDetails(
            email="max@mustermann.de",
            IBAN="BE19967722383012",
            legalType=LegalType.PRIVATE,
        ),
    )


@pytest.fixture(scope="session")
def sandbox_iban_recipient(
    sandbox_client: Client, sandbox_iban_recipient_request: Recipient
) -> RecipientAccountResponse:
    """Create an iban recipient."""
    answer = sandbox_client.recipient_accounts.create_recipient(sandbox_iban_recipient_request)
    return sandbox_client.recipient_accounts.get(answer)


@pytest.fixture(scope="session")
def sandbox_quote_request() -> QuoteRequest:
    """The quote request for Max Mustermann 100 EUR."""
    return QuoteRequest(
        sourceCurrency="EUR",
        targetCurrency="EUR",
        sourceAmount=100,
        targetAccount=None,
        payOut=PaymentMethod.BANK_TRANSFER,
        preferredPayIn=PaymentMethod.BANK_TRANSFER,
    )


@pytest.fixture(scope="session")
def sandbox_quote(
    sandbox_client: Client,
    sandbox_quote_request: QuoteRequest,
    sandbox_business_profile: Profile,
) -> QuoteResponse:
    """A Quote to send money to Max Mustermann."""
    return sandbox_client.quotes.create(sandbox_quote_request, sandbox_business_profile)


@pytest.fixture(scope="session")
def sandbox_quote_requirements(
    sandbox_client: Client, sandbox_quote: QuoteResponse
) -> RecipientAccountRequirements:
    """Get the requirements for a quote."""
    return sandbox_client.recipient_accounts.get_requirements_for_quote(sandbox_quote)


@pytest.fixture(scope="session")
def sandbox_quote_updated(
    sandbox_client: Client,
    sandbox_quote: QuoteResponse,
    sandbox_iban_recipient: RecipientAccountResponse,
) -> QuoteResponse:
    """Update the quote with the account."""
    return sandbox_client.quotes.update(sandbox_iban_recipient, sandbox_quote)


@pytest.fixture(scope="session")
def sandbox_transfer_request(
    sandbox_quote_updated: QuoteResponse,
    sandbox_iban_recipient: RecipientAccountResponse,
) -> TransferRequest:
    """Create a transfer request."""
    return TransferRequest(
        targetAccount=sandbox_iban_recipient.id,
        quoteUuid=sandbox_quote_updated.id,
        details=TransferDetails(reference="Geschenk"),
    )


@pytest.fixture(scope="session")
def sandbox_transfer_requirements(
    sandbox_client: Client, sandbox_transfer_request: TransferRequest
) -> TransferResponse:
    """Create a transfer."""
    return sandbox_client.transfers.get_requirements(sandbox_transfer_request)


@pytest.fixture(scope="session")
def sandbox_transfer(
    sandbox_client: Client, sandbox_transfer_request: TransferRequest
) -> TransferResponse:
    """Create a transfer."""
    return sandbox_client.transfers.create(sandbox_transfer_request)


@pytest.fixture(scope="session")
def sandbox_payment(
    sandbox_client: Client,
    sandbox_transfer: TransferResponse,
    sandbox_business_profile: Profile,
) -> PaymentResponse:
    """Return the payment response."""
    try:
        return sandbox_client.transfers.fund(sandbox_transfer.id, sandbox_business_profile.id)
        # return sandbox_client.transfers.fund(sandbox_transfer)
    except WiseAPIError as e:
        print(
            f"""
              Activate SCA at https://sandbox.transferwise.tech/settings/public-keys
              And upload the public key to your BUSINESS account.
              {DEFAULT_PUBLIC_KEY}
              Otherwise, the next steps do not work.
              """
        )
        raise e
