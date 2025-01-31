from collections import defaultdict, namedtuple
from pathlib import Path

from requests.exceptions import ConnectionError

from wise_banking_api_client import Currency
from wise_banking_api_client.model.requirements import RequiredFieldType
from wise_banking_api_client.test import TestClient

#   SchemaError: regex parse error:
# error: backreferences are not supported
BACK_REFERENCES = ["(?!", r"\1", r"\2", r"\3", r"\4", r"\5"]


def generate_recipient_details():
    HERE = Path(__file__).parent
    client = TestClient()
    select = defaultdict(set)
    TEXT = namedtuple("TEXT", ["start", "examples", "min_length", "max_length", "pattern"])
    text = dict()
    for currency in Currency.all_currencies():
        try:
            requirements = client.recipient_accounts.get_requirements_for_currency(
                source=currency, target=currency, source_amount=100
            )
        except ConnectionError:
            continue
        for requirement in requirements:
            for field in requirement.fields:
                for group in field.group:
                    key = group.key
                    added = False
                    if (
                        group.type in [RequiredFieldType.select, RequiredFieldType.radio]
                        and group.valuesAllowed
                    ):
                        for value in group.valuesAllowed:
                            select[key].add(value.key)
                        added = True
                    if (
                        not added
                    ):  # group.type == RequiredFieldType.text or group.type == RequiredFieldType.date:
                        start, examples, min_length, max_length, pattern = text.get(
                            key, TEXT("", set(), None, None, set())
                        )
                        if not start:
                            start = f"{group.key} : Optional[{'str' if group.type != RequiredFieldType.date else 'date'}] = Field("
                        if group.example:
                            examples.add(group.example)
                        if group.minLength and (min_length is None or group.minLength < min_length):
                            min_length = group.minLength
                        if group.maxLength and (max_length is None or group.maxLength > max_length):
                            max_length = group.maxLength
                        if group.validationRegexp:
                            pattern.add(
                                ".*"
                                if any(br in group.validationRegexp for br in BACK_REFERENCES)
                                else group.validationRegexp
                            )
                        text[key] = TEXT(start, examples, min_length, max_length, pattern)
    text.pop("dateOfBirth")
    for key, value in text.copy().items():
        pattern = "(" + ")|(".join(sorted(value[4])) + ")" if value[4] else None
        examples = sorted(value[1]) if value[1] else None
        text[key] = (
            value[0]
            + f"examples={examples!r}, "
            + f"min_length={value[2]}, "
            + f"max_length={value[3]}, "
            + f"pattern={pattern!r}"
            + ", default=None)"
        )

    with (HERE / "literals.py").open("w") as f:
        print(
            """
# generated file
#    python -m wise_banking_api_client.model.recipient && black .

from typing import Literal, TypeAlias

""",
            file=f,
        )
        literals = []
        for key, values in sorted(select.copy().items()):
            k = key.upper().replace(".", "_")
            print(f"{k}_VALUES = {sorted(values)}", file=f)
            print(f"{k} : TypeAlias = Literal[*{k}_VALUES]", file=f)
            literals.append(k)
        literals = sorted(literals)
        print(f"__all__ = {literals}", file=f)

    with (HERE / "details.py").open("w") as f:
        print(
            f'''
# generated file
#    python -m wise_banking_api_client.model.recipient && black .

from wise_banking_api_client.model.timestamp import Date
from .address import AddressDetails
from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import date
from .literals import {", ".join(literals)}
        
class RecipientDetails(BaseModel):
    """The recipient details model.

    See https://docs.wise.com/api-docs/api-reference/recipient
    """
    dateOfBirth: Optional[date] = Field(description="Date of birth", default=None)
    address: Optional[AddressDetails] = None
    legalType : Optional[LegalType] = None
    ''',
            file=f,
        )
        for key, values in sorted(select.items()):
            if not key.startswith("address"):
                print(
                    f"    {key}: Optional[{key.upper().replace('.', '_')}] = None",
                    file=f,
                )
        for key, value in sorted(text.items()):
            if not key.startswith("address"):
                print(f"    {value}", file=f)
        print(
            """
              
__all__ = ["RecipientDetails"]
""",
            file=f,
        )

    with (HERE / "address.py").open("w") as f:
        print(
            '''
# generated file
#    python -m wise_banking_api_client.model.recipient && black .

from pydantic import BaseModel, Field
from typing import Optional, ClassVar
from .literals import ADDRESS_COUNTRY
              
class AddressDetails(BaseModel):
    """The address details of a transfer or recipient.

    Attributes:
        firstLine: address first line
        city: address city
        stateCode: address state code
        countryCode: address country code
        postCode: address zip code
    """
    
    EXAMPLE_JSON : ClassVar[
        str
    ] = """
    {
        "firstLine": "Salu tee 14",
        "city": "Tallinn",
        "stateCode": null,
        "countryCode": "EE",
        "postCode": "12112"
    }
    """
    
    stateCode: Optional[str] = None
    countryCode: Optional[ADDRESS_COUNTRY] = None
    
    @property
    def country_code(self) -> ADDRESS_COUNTRY:
        """The country code."""
        return self.countryCode or self.country
''',
            file=f,
        )
        for key, value in sorted(text.items()):
            if key.startswith("address"):
                print(f"    {value[8:]}", file=f)
        for key, values in sorted(select.items()):
            if key.startswith("address"):
                print(
                    f"    {key[8:]}: Optional[{key.upper().replace('.', '_')}] = None",
                    file=f,
                )
        print(
            """
__all__ = ["AddressDetails"]
""",
            file=f,
        )


if __name__ == "__main__":
    generate_recipient_details()
