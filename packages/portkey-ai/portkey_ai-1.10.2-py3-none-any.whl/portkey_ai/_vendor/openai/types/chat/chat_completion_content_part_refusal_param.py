# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["ChatCompletionContentPartRefusalParam"]


class ChatCompletionContentPartRefusalParam(TypedDict, total=False):
    refusal: Required[str]
    """The refusal message generated by the model."""

    type: Required[Literal["refusal"]]
    """The type of the content part."""
