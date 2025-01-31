from __future__ import annotations

import functools
from functools import partial, update_wrapper, wraps
from typing import Any, Callable, Optional

import apiron
from apiron.endpoint import JsonEndpoint as ApironJsonEndpoint
from requests import JSONDecodeError
from requests.exceptions import HTTPError

from wise_banking_api_client.model.error import WiseAPIErrorResponse
from wise_banking_api_client.signing import sign_sca_challenge


class WiseAPIError(HTTPError):
    """This is a special error for HTTPRequests that includes information from the JSON response.

    Example response:

        {
            "type":"about:blank",
            "title":"Unsupported Media Type",
            "status":415,
            "detail":"Content-Type'null' is not supported.",
            "instance":"/public/v3/quotes"
        }

    """

    @classmethod
    def from_http_error(cls, http_error: HTTPError) -> WiseAPIError:
        error = cls(*http_error.args, response=http_error.response)
        error.with_traceback(http_error.__traceback__)
        return error

    def __init__(self, *args, request=..., response=...):
        """Create a new API Error."""
        super().__init__(*args, request=request, response=response)
        self.original_message = args[0] if args else ""

    def __repr__(self) -> str:
        """The error."""
        return f"{self.__class__.__name__} {self!s}"

    def __str__(self) -> str:
        """The error description."""
        json = self.json
        return f"{json.status} at {json.instance}: {json.title}: {json.detail}"

    @property
    def json(self) -> WiseAPIErrorResponse:
        """The JSON response from the API."""
        error = {
            "type": str(self.response.status_code),
            "title": self.response.reason,
            "status": self.response.status_code,
            "detail": self.original_message,
            "instance": self.response.url,
        }
        try:
            json = self.response.json()
            for k in error:
                if k in json:
                    error[k] = json[k]
            error["json"] = json
            if "errors" in json:
                # [{'code': 'NOT_VALID', 'message': 'Please specify a valid IBAN.', 'path': 'IBAN', 'arguments': ['IBAN', 'DE12345678901234567890']}]
                error["detail"] += ": " + str(json["errors"])
        except JSONDecodeError:
            pass
        return WiseAPIErrorResponse(**error)

    @classmethod
    def replace_HTTPError(cls, func: Callable) -> Callable:
        """A annotation to replace HTTPError with APIError."""

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except HTTPError as e:
                raise cls.from_http_error(e)

        return wrapper


class PrivateKeyForSCARequired(ValueError):
    """In order to use this endpoint, we need a private key."""


class JsonEndpoint(ApironJsonEndpoint):
    """A JSONEndpoint with customizations for this API."""

    def __init__(
        self,
        *args: Any,
        additional_headers: Optional[dict[str, str]] = None,
        **kwargs: Any,
    ):
        """Create a new endpoint."""
        super().__init__(*args, **kwargs)
        self.additional_headers = (
            additional_headers.copy() if additional_headers is not None else {}
        )

    @staticmethod
    def __get__(self, instance: JsonEndpoint, owner: type[Base]):
        """Return the callable endpoint."""
        caller = super().__get__(instance, owner)
        caller = WiseAPIError.replace_HTTPError(caller)

        @wraps(caller)
        def wrapper(*args, **kwargs):
            """Divide the arguments in those passed to replace the path and
            those that are used by apiron.client.call.

            Those for the path will undergo a replacement.
            """
            kwargs = owner.adjust_endpoint_call(kwargs)
            return caller(*args, **kwargs)

        return wrapper

    @property
    def required_headers(self) -> dict[str, str]:
        headers = super().required_headers.copy()
        headers.update(self.additional_headers)
        if self.default_method == "POST":
            headers.setdefault("Content-Type", "application/json")
        return headers


class JsonEndpointWithSCA(JsonEndpoint):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.sca_headers: dict[str, str] = {}

    # apiron's required_headers should be called override_headers
    @property
    def required_headers(self) -> dict[str, str]:
        # It looks like 2FA only needs to be performed every few minutes,
        # but there seems to be no harm in re-sending the signature.
        return {**super().required_headers, **self.sca_headers}

    def __get__(self, instance: Base | None, owner: type[Base]) -> Callable[..., Any]:
        caller = partial(apiron.client.call, owner, self)
        caller = WiseAPIError.replace_HTTPError(caller)
        update_wrapper(caller, apiron.client.call)

        @wraps(apiron.client.call)
        def perform_2fa_if_needed(*args: Any, **kwargs: Any) -> Any:
            kwargs = owner.adjust_endpoint_call(kwargs)
            try:
                return caller(*args, **kwargs)
            except HTTPError as e:
                resp = e.response
                if resp.status_code == 403 and resp.headers["X-2FA-Approval-Result"] == "REJECTED":
                    challenge = resp.headers["X-2FA-Approval"]
                    if owner.client.private_key_data is None:  # type: ignore[union-attr]
                        raise PrivateKeyForSCARequired(
                            "Please provide private_key_file or private_key_data to perform SCA authentication."
                        ) from e

                    self.sca_headers["X-Signature"] = sign_sca_challenge(
                        challenge,
                        owner.client.private_key_data,  # type: ignore[union-attr]
                    )
                    self.sca_headers["X-2FA-Approval"] = challenge
                    return caller(*args, **kwargs)
                raise

        return perform_2fa_if_needed


__all__ = [
    "JsonEndpoint",
    "JsonEndpointWithSCA",
    "PrivateKeyForSCARequired",
    "WiseAPIError",
]
