"""Tests unitarios del ConnectionManager multi-tab (sin BD)."""

from src.api.notifications.connection_manager import ConnectionManager


class FakeWebSocket:
  def __init__(self, name="ws"):
    self.name = name
    self.accepted = False
    self.sent = []
    self._fail_send = False

  async def accept(self):
    self.accepted = True

  async def send_json(self, message):
    if self._fail_send:
      raise RuntimeError("send failed")
    self.sent.append(message)


async def _noop_observer(user_id):
  return None


def _make_manager():
  manager = ConnectionManager()
  manager._observe_notifications = _noop_observer
  return manager


async def test_connect_multiple_tabs_keeps_both_connections():
  manager = _make_manager()
  ws1 = FakeWebSocket("tab1")
  ws2 = FakeWebSocket("tab2")

  await manager.connect(ws1, "user-1")
  await manager.connect(ws2, "user-1")

  assert ws1.accepted and ws2.accepted
  assert len(manager.active_connections["user-1"]) == 2


async def test_disconnect_one_tab_keeps_other():
  manager = _make_manager()
  ws1 = FakeWebSocket("tab1")
  ws2 = FakeWebSocket("tab2")

  await manager.connect(ws1, "user-1")
  await manager.connect(ws2, "user-1")
  manager.disconnect(ws1, "user-1")

  assert ws2 in manager.active_connections["user-1"]
  assert len(manager.active_connections["user-1"]) == 1


async def test_disconnect_last_tab_removes_user():
  manager = _make_manager()
  ws1 = FakeWebSocket("tab1")

  await manager.connect(ws1, "user-1")
  manager.disconnect(ws1, "user-1")

  assert "user-1" not in manager.active_connections


async def test_send_to_user_broadcasts_to_all_tabs():
  manager = _make_manager()
  ws1 = FakeWebSocket("tab1")
  ws2 = FakeWebSocket("tab2")

  await manager.connect(ws1, "user-1")
  await manager.connect(ws2, "user-1")
  await manager.send_to_user("user-1", {"type": "unread_count", "unread_count": 2})

  assert ws1.sent == [{"type": "unread_count", "unread_count": 2}]
  assert ws2.sent == [{"type": "unread_count", "unread_count": 2}]


async def test_send_to_user_removes_failed_connection():
  manager = _make_manager()
  ws_ok = FakeWebSocket("ok")
  ws_bad = FakeWebSocket("bad")
  ws_bad._fail_send = True

  await manager.connect(ws_ok, "user-1")
  await manager.connect(ws_bad, "user-1")
  await manager.send_to_user("user-1", {"type": "unread_count", "unread_count": 1})

  assert ws_bad not in manager.active_connections["user-1"]
  assert ws_ok in manager.active_connections["user-1"]
  assert ws_ok.sent == [{"type": "unread_count", "unread_count": 1}]


async def test_send_to_user_absent_user_is_noop():
  manager = _make_manager()
  await manager.send_to_user("ghost", {"type": "unread_count", "unread_count": 0})