import pytest

from logic.commands.chat import CreateChatCommand
from logic.exceptions.chat import ChatWithTitleAlreadyExistsException
from logic.mediator import Mediator
from repositories.base import BaseChatRepository


@pytest.mark.asyncio
async def test_create_chat_success(
    mediator: Mediator,
    chat_repository: BaseChatRepository,
):
    command = CreateChatCommand("Title")
    chat1, *_ = await mediator.execute([command])

    assert chat1 is not None
    assert chat1.title.value == "Title"

    chat2 = await chat_repository.get_chat_by_title("Title")

    assert chat2 is not None
    assert chat2.title.value == "Title"
    assert chat1 is chat2


@pytest.mark.asyncio
async def test_create_chat_already_exists(
    mediator: Mediator,
    chat_repository: BaseChatRepository,
):
    command = CreateChatCommand("Title")
    chat1, *_ = await mediator.execute([command])

    with pytest.raises(ChatWithTitleAlreadyExistsException):
        await mediator.execute([command])
