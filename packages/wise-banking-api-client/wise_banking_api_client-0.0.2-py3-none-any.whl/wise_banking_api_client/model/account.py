"""The account models.


See https://docs.wise.com/api-docs/api-reference/recipient

"""

from typing import Annotated, ClassVar, Optional

from pydantic import BeforeValidator, Field

from wise_banking_api_client.model.account_requirement_type import (
    AccountRequirementType,
)
from wise_banking_api_client.model.annotations import WithoutNone
from wise_banking_api_client.model.base import DOCUMENTED_BUT_ABSENT, BaseModel
from wise_banking_api_client.model.country import COUNTRY_CODE
from wise_banking_api_client.model.currency import CURRENCY
from wise_banking_api_client.model.enum import StrEnum
from wise_banking_api_client.model.legal_type import LegalType
from wise_banking_api_client.model.recipient.details import (
    RecipientDetails as RecipientAccountRequestDetails,
)
from wise_banking_api_client.model.requirements import (
    AccountRequirement,
    RequiredField,
    RequirementsList,
)


class RecipientName(BaseModel):
    """The recipient name.

    Attributes:
        fullName: Recipient full name
        givenName: Recipient first name
        familyName: Recipient surname
        middleName: Recipient middle name
        patronymicName: The patronymic name of the recipient.
        cannotHavePatronymicName: The patronymic name of the recipient.
    """

    EXAMPLE_JSON: ClassVar[
        str
    ] = """
    {
        "fullName": "John Doe",
        "givenName": null,
        "familyName": null,
        "middleName": null,
        "patronymicName": null,
        "cannotHavePatronymicName": null
    }
    """
    fullName: str
    givenName: Optional[str] = None
    familyName: Optional[str] = None
    middleName: Optional[str] = None
    patronymicName: Optional[str] = None
    cannotHavePatronymicName: object = None


class CommonFieldMap(BaseModel):
    """Map of key lookup fields on the account.

    Attributes:
        bankCodeField: Bank sort code identifier field
    """

    EXAMPLE_JSON: ClassVar[
        str
    ] = """
    {
        "accountNumberField": "accountNumber",
        "bankCodeField": "sortCode"
    }
    """
    accountNumberField: Optional[str] = None
    bankCodeField: Optional[str] = None


class DisplayField(BaseModel):
    """Lookup fields."""

    EXAMPLE_JSON: ClassVar[
        str
    ] = """
    {
        "key": "details/sortCode",
        "label": "UK sort code",
        "value": "04-00-75"
    }
    """

    key: str
    label: str
    value: str


class LegalEntityType(StrEnum):
    """The legal type of a recipient account."""

    PERSON = "PERSON"
    BUSINESS = "BUSINESS"
    INSTITUTION = "INSTITUTION"


class RecipientAccountResponse(BaseModel):
    """The recipient account as received from the API.

    Attributes:
        id: The ID of the recipient account.
        profileId: ABSENT - replaced by profile
            Personal or business profile ID.
        creatorId: ABSENT - replaced by user.
            Account entity that owns the recipient account
        name: Recipient name details
        currency: 3 character currency code
        type: Recipient type
        legalEntityType: ABSENT - replaced by details.legalType.
            Legal Entity type of recipient
        active: Whether the recipient account is active - Status of the recipient
        details: Recipient account details
        commonFieldMap: Map of key lookup fields on the account
        hash: Account hash for change tracking
        accountSummary: Summary of account details for ease of lookup
        longAccountSummary: Account details summary
        displayFields: Lookup fields
        isInternal: Whether the recipient account is internal
        ownedByCustomer: If recipient account belongs to profile owner

    """

    id: int
    creatorId: DOCUMENTED_BUT_ABSENT[int] = None
    profileId: DOCUMENTED_BUT_ABSENT[int] = None
    name: Optional[RecipientName] = None
    currency: str = CURRENCY
    # country: Optional[str] = COUNTRY_CODE
    type: Annotated[
        AccountRequirementType,
        BeforeValidator(AccountRequirementType.from_camel_case),
    ]
    legalEntityType: DOCUMENTED_BUT_ABSENT[LegalEntityType | LegalType] = None
    active: bool
    commonFieldMap: Optional[CommonFieldMap] = None
    hash: str
    accountSummary: str
    longAccountSummary: str
    displayFields: list[DisplayField]
    isInternal: bool
    ownedByCustomer: bool
    email: Optional[str] = None

    EXAMPLE_JSON: ClassVar[
        str
    ] = """
    {
        "id": 40000000,
        "creatorId": 41000000,
        "profileId": 30000000,
        "name": {
            "fullName": "John Doe",
            "givenName": null,
            "familyName": null,
            "middleName": null,
            "patronymicName": null,
            "cannotHavePatronymicName": null
        },
        "currency": "GBP",
        "type": "sort_code",
        "legalEntityType": "PERSON",
        "active": true,
        "commonFieldMap": {
            "accountNumberField": "accountNumber",
            "bankCodeField": "sortCode"
        },
        "hash": "666ef880f8aa6113fa112ba6531d3ed2c26dd9fgbd7de5136bfb827a6e800479",
        "accountSummary": "(04-00-75) 37778842",
        "longAccountSummary": "GBP account ending in 8842",
        "displayFields": [
            {
                "key": "details/sortCode",
                "label": "UK sort code",
                "value": "04-00-75"
            },
            {
                "key": "details/accountNumber",
                "label": "Account number",
                "value": "37778842"
            }
        ],
        "isInternal": false,
        "ownedByCustomer": false,
        "email": null
    }
    """


ACCOUNT_HOLDER_NAME_REGEX = r"[0-9A-Za-zÀ-ÖØ-öø-ÿ-_()'*,.\s]+"


class RecipientAccountRequest(BaseModel):
    """Data to create a recipient account.

    Attributes:
        currency: 3 character currency code
        type: Recipient type
        profile: Personal or business profile ID. It is highly advised to pass the
            business profile ID in this field if your business account
            is managed by multiple users, so that the recipient can be
            accessed by all users authorized on the business account.
        ownedByCustomer: Whether this account is owned by the sending user
        accountHolderName: Recipient full name
        details: Currency specific fields
    """

    EXAMPLE_JSON: ClassVar[
        str
    ] = """
    {
        "currency": "GBP",
        "type": "sort_code",
        "profile": 30000000,
        "ownedByCustomer": true,
        "accountHolderName": "John Doe",
        "details": {
            "dateOfBirth": "1961-01-01",
            "legalType": "PRIVATE",
            "accountNumber": "37778842",
            "sortCode": "040075"
        }
    }
    """

    currency: str = CURRENCY
    type: AccountRequirementType
    profile: int
    ownedByCustomer: bool
    accountHolderName: str = Field(pattern=ACCOUNT_HOLDER_NAME_REGEX)
    details: WithoutNone[RecipientAccountRequestDetails]


class FilledInRecipientAccountRequest(RecipientAccountRequest):
    """The result of creating a recipient.

    Attributes:
        id: Recipient account ID
        business: Business profile ID
        confirmations: unclear
        country: Recipient country code
        user: User ID
        active: Whether the recipient account is active
    """

    EXAMPLE_JSON: ClassVar[
        str
    ] = """
    {
        "currency": "GBP",
        "type": "sort_code",
        "profile": 30000000,
        "ownedByCustomer": true,
        "accountHolderName": "John Doe",
        "details": {
            "dateOfBirth": "1961-01-01",
            "legalType": "PRIVATE",
            "accountNumber": "37778842",
            "sortCode": "040075"
        },
        "id": 40000000,
        "business": 30000000,
        "confirmations": null,
        "country": "GB",
        "user": 41000000,
        "active": true
    }
    """

    id: int
    business: Optional[int] = None
    confirmations: object  # TODO: What is this?
    country: Optional[str] = COUNTRY_CODE
    user: Optional[int] = None
    active: bool


class RecipientAccountsSorting(BaseModel):
    """Sorting configuration."""

    EXAMPLE_JSON: ClassVar[
        str
    ] = """
    {
        "empty": true,
        "sorted": false,
        "unsorted": true
    }
    """

    empty: bool
    sorted: bool
    unsorted: bool


class RecipientAccountListResponse(BaseModel):
    """A list paginated of recipient accounts."""

    EXAMPLE_JSON: ClassVar[
        str
    ] = """
    {
        "content": [],
        "sort": {
            "empty": true,
            "sorted": false,
            "unsorted": true
        },
        "size": 0
    }
    """

    content: list[RecipientAccountResponse]
    sort: RecipientAccountsSorting
    size: int


class RecipientAccountRequirements(RequirementsList[AccountRequirement]):
    """An easy access to all the requirements."""

    aba: Optional[AccountRequirement]
    argentina: Optional[AccountRequirement]
    australian: Optional[AccountRequirement]
    australian_bpay: Optional[AccountRequirement]
    bangladesh: Optional[AccountRequirement]
    bkash: Optional[AccountRequirement]
    brazil: Optional[AccountRequirement]
    brazil_business: Optional[AccountRequirement]
    canadian: Optional[AccountRequirement]
    chile: Optional[AccountRequirement]
    chinese_alipay: Optional[AccountRequirement]
    chinese_wechatpay: Optional[AccountRequirement]
    colombia: Optional[AccountRequirement]
    costa_rica: Optional[AccountRequirement]
    czech: Optional[AccountRequirement]
    email: Optional[AccountRequirement]
    emirates: Optional[AccountRequirement]
    fiji_mobile: Optional[AccountRequirement]
    hongkong: Optional[AccountRequirement]
    hong_kong_fps: Optional[AccountRequirement]
    hungarian: Optional[AccountRequirement]
    iban: Optional[AccountRequirement]
    indian: Optional[AccountRequirement]
    indian_upi: Optional[AccountRequirement]
    indonesian: Optional[AccountRequirement]
    interac: Optional[AccountRequirement]
    israeli_local: Optional[AccountRequirement]
    japanese: Optional[AccountRequirement]
    kenya_local: Optional[AccountRequirement]
    kenya_mobile: Optional[AccountRequirement]
    malaysian: Optional[AccountRequirement]
    malaysian_duitnow: Optional[AccountRequirement]
    mexican: Optional[AccountRequirement]
    morocco: Optional[AccountRequirement]
    mozambique_local: Optional[AccountRequirement]
    namibia_local: Optional[AccountRequirement]
    nepal: Optional[AccountRequirement]
    newzealand: Optional[AccountRequirement]
    nigeria: Optional[AccountRequirement]
    peru: Optional[AccountRequirement]
    philippines: Optional[AccountRequirement]
    philippinesmobile: Optional[AccountRequirement]
    polish: Optional[AccountRequirement]
    privatbank: Optional[AccountRequirement]
    russiarapida: Optional[AccountRequirement]
    singapore: Optional[AccountRequirement]
    singapore_paynow: Optional[AccountRequirement]
    sort_code: Optional[AccountRequirement]
    southafrica: Optional[AccountRequirement]
    south_korean_paygate: Optional[AccountRequirement]
    south_korean_paygate_business: Optional[AccountRequirement]
    srilanka: Optional[AccountRequirement]
    tanzania_local: Optional[AccountRequirement]
    thailand: Optional[AccountRequirement]
    turkish_earthport: Optional[AccountRequirement]
    uganda_local: Optional[AccountRequirement]
    uruguay: Optional[AccountRequirement]
    vietname_earthport: Optional[AccountRequirement]
    fedwire_local: Optional[AccountRequirement]
    swift_code: Optional[AccountRequirement]


RecipientAccountRequirements._add_getters_from_enum(AccountRequirementType, AccountRequirement)


class RecipientAccountList(list[RecipientAccountResponse]):
    """A list of recipient accounts."""


__all__ = [
    "AccountRequirement",
    "AccountRequirementType",
    "CommonFieldMap",
    "DisplayField",
    "FilledInRecipientAccountRequest",
    "LegalEntityType",
    "RecipientAccountListResponse",
    "RecipientAccountRequest",
    "RecipientAccountRequestDetails",
    "RecipientAccountRequirements",
    "RecipientAccountResponse",
    "RecipientAccountsSorting",
    "RecipientName",
    "RequiredField",
]
