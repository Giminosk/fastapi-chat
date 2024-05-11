from datetime import datetime

import pytest

from domain.entities.message import Message
from domain.exceptions.message import EmptyMessageException, TooLongMessageException
from domain.values.message import Text


def test_create_text():
    text = Text(value="hello")

    assert text.value == "hello"
    assert text.as_generic_type() == "hello"


def test_create_text_empty():
    with pytest.raises(EmptyMessageException):
        Text("")


def test_create_text_too_long():
    with pytest.raises(TooLongMessageException):
        Text("a" * 1001)


def test_create_message_success():
    text = Text(value="hello")
    message = Message(text, "test")

    assert message.text == text
    assert message.created_at.date() == datetime.today().date()
