from typing import Dict
from fastapi import WebSocket
from sqlalchemy.orm import Session
import logging
import asyncio

from src.core.database import SessionLocal
from . import repository

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        # Almacena conexiones activas: {user_id: WebSocket}
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        logger.info(f"WebSocket connected for user {user_id}")
        
        # Iniciar "observador" para este usuario
        asyncio.create_task(self._observe_notifications(user_id))

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            logger.info(f"WebSocket disconnected for user {user_id}")

    async def send_to_user(self, user_id: str, message: dict):
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_json(message)
                logger.debug(f"Sent WebSocket message to user {user_id}")
            except Exception as e:
                logger.error(f"Error sending WebSocket message to user {user_id}: {e}")
                self.disconnect(user_id)

    async def _observe_notifications(self, user_id: str):
        """
        Observa cambios en la BD para el usuario específico.
        Envía actualizaciones automáticas cuando hay cambios (cada 5 segundos).
        """
        last_count = None
        
        while user_id in self.active_connections:
            db = SessionLocal()
            try:
                count = repository.count_unread_by_user_id(db, user_id)
                
                if last_count != count:
                    last_count = count
                    await self.send_to_user(user_id, {
                        "type": "unread_count",
                        "unread_count": count
                    })
            except Exception as e:
                logger.error(f"Error observing notifications for user {user_id}: {e}")
            finally:
                db.close()
            
            await asyncio.sleep(5)  # Revisar cada 5 segundos


manager = ConnectionManager()
