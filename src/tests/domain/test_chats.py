from datetime import datetime

import pytest

from domain.entities.chat import Chat
from domain.entities.message import Message
from domain.events.chat import ChatCreatedEvent, NewMessageReceivedEvent
from domain.exceptions.chat import (
    EmptyTitleException,
    TitleStrartsWithNoCapital,
    TooLongTitleException,
)
from domain.values.chat import Title
from domain.values.message import Text


def test_create_title_success():
    title = Title("Title")

    assert title.value == "Title"
    assert title.as_generic_type() == "Title"


def test_create_title_empty():
    with pytest.raises(EmptyTitleException):
        Title("")


def test_create_title_too_long():
    with pytest.raises(TooLongTitleException):
        Title("A" * 101)


def test_create_title_starts_with_no_capital():
    with pytest.raises(TitleStrartsWithNoCapital):
        Title("title")


def test_create_chat_sucess():
    title = Title("Title")
    chat = Chat.create_chat(title=title)

    assert chat.title == title
    assert chat.messages == []
    assert chat.created_at.date() == datetime.today().date()


def test_add_message_to_chat():
    chat = Chat.create_chat(Title("Title"))
    message = Message(Text("hello"), chat.oid)

    chat.add_message(message)

    assert message in chat.messages
    assert chat.messages == [message]


def test_chat_message_events():
    chat = Chat.create_chat(Title("Title"))
    message = Message(Text("hello"), chat.oid)

    chat.add_message(message)

    events = chat.pull_events()

    assert len(chat.pull_events()) == 0
    assert len(events) == 2

    first = events[0]
    assert isinstance(first, ChatCreatedEvent)
    assert first.chat_oid == chat.oid and first.title == chat.title.as_generic_type()

    second = events[1]
    assert isinstance(second, NewMessageReceivedEvent)
    assert (
        second.chat_oid == chat.oid
        and second.message_oid == message.oid
        and second.message_text == message.text.as_generic_type()
    )
