from typing import Dict, Set
from fastapi import WebSocket
import logging
import asyncio

from src.core.database import AsyncSessionLocal
from . import repository

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self):
        # Almacena conexiones activas por usuario: {user_id: set[WebSocket]}
        # Soporta múltiples pestañas/ventanas abiertas con el mismo usuario.
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        connections = self.active_connections.setdefault(user_id, set())
        connections.add(websocket)
        logger.info(f"WebSocket connected for user {user_id} ({len(connections)} active)")

        # Iniciar un único "observador" por usuario (no uno por pestaña)
        if len(connections) == 1:
            asyncio.create_task(self._observe_notifications(user_id))

    def disconnect(self, websocket: WebSocket, user_id: str):
        connections = self.active_connections.get(user_id)
        if connections:
            connections.discard(websocket)
            if connections:
                logger.info(f"WebSocket disconnected for user {user_id} ({len(connections)} active)")
            else:
                del self.active_connections[user_id]
                logger.info(f"WebSocket disconnected for user {user_id} (no active connections)")

    async def send_to_user(self, user_id: str, message: dict):
        connections = self.active_connections.get(user_id)
        if not connections:
            return

        closed = []
        for websocket in list(connections):
            try:
                await websocket.send_json(message)
                logger.debug(f"Sent WebSocket message to user {user_id}")
            except Exception as e:
                logger.error(f"Error sending WebSocket message to user {user_id}: {e}")
                closed.append(websocket)

        for websocket in closed:
            self.disconnect(websocket, user_id)

    async def _observe_notifications(self, user_id: str):
        """
        Observa cambios en la BD para el usuario específico.
        Envía actualizaciones automáticas cuando hay cambios (cada 5 segundos).
        Termina cuando el usuario ya no tiene conexiones activas.
        """
        last_count = None

        while user_id in self.active_connections:
            async with AsyncSessionLocal() as db:
                try:
                    count = await repository.count_unread_by_user_id(db, user_id)

                    if last_count != count:
                        last_count = count
                        await self.send_to_user(user_id, {
                            "type": "unread_count",
                            "unread_count": count
                        })
                except Exception as e:
                    logger.error(f"Error observing notifications for user {user_id}: {e}")

            await asyncio.sleep(5)  # Revisar cada 5 segundos


manager = ConnectionManager()