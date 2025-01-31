"""Test Goodfire Chat API wrapper."""

import os
from typing import List

import goodfire
import pytest
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage

from langchain_goodfire.chat_model import (
    ChatGoodfire,
    format_for_goodfire,
)

os.environ["GOODFIRE_API_KEY"] = "test_key"


def get_valid_variant() -> goodfire.Variant:
    return goodfire.Variant("meta-llama/Llama-3.3-70B-Instruct")


def test_goodfire_model_param() -> None:
    base_variant = get_valid_variant()
    llm = ChatGoodfire(model=base_variant)
    assert isinstance(llm.model, goodfire.Variant)
    assert llm.model.base_model == base_variant.base_model


def test_goodfire_initialization() -> None:
    """Test goodfire initialization with API key."""
    llm = ChatGoodfire(model=get_valid_variant(), goodfire_api_key="test_key")
    # Check that clients were initialized with the API key
    assert llm.sync_client is not None
    assert llm.async_client is not None
    # Could also verify the clients were initialized with correct key if the client
    # exposes that information (though it probably shouldn't for security reasons)


@pytest.mark.parametrize(
    ("messages", "expected"),
    [
        ([HumanMessage(content="Hello")], [{"role": "user", "content": "Hello"}]),
        (
            [HumanMessage(content="Hello"), AIMessage(content="Hi there!")],
            [
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi there!"},
            ],
        ),
        (
            [
                SystemMessage(content="You're an assistant"),
                HumanMessage(content="Hello"),
                AIMessage(content="Hi there!"),
            ],
            [
                {"role": "system", "content": "You're an assistant"},
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi there!"},
            ],
        ),
    ],
)
def test_message_formatting(messages: List[BaseMessage], expected: List[dict]) -> None:
    result = format_for_goodfire(messages)
    assert result == expected


def test_invalid_message_type() -> None:
    class CustomMessage(BaseMessage):
        content: str
        type: str = "custom"

    with pytest.raises(ValueError, match="Unknown message type"):
        format_for_goodfire([CustomMessage(content="test")])
