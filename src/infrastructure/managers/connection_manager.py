from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field

from fastapi import WebSocket


@dataclass
class BaseConnectionManager(ABC):
    connections_map: dict[str, list[WebSocket]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    @abstractmethod
    async def accept_connection(self, websocket: WebSocket, key: str) -> None:
        pass

    @abstractmethod
    async def remove_connection(self, websocket: WebSocket, key: str) -> None:
        pass

    @abstractmethod
    async def send_all(self, key: str, message: bytes) -> None:
        pass


@dataclass
class ConnectionManager(BaseConnectionManager):
    async def accept_connection(self, websocket: WebSocket, key: str) -> None:
        await websocket.accept()
        self.connections_map[key].append(websocket)

    async def remove_connection(self, websocket: WebSocket, key: str) -> None:
        websocket.close()
        self.connections_map[key].remove(websocket)

    async def send_all(self, key: str, message: bytes) -> None:
        for websocket in self.connections_map[key]:
            await websocket.send_bytes(message)
