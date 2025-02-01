# Copyright 2023-2025 Sébastien Demanou. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
import json
import logging
from collections.abc import Callable
from collections.abc import Coroutine
from ssl import SSLContext
from typing import Any
from typing import Generic
from typing import TypeVar

from .event import EventData
from .wsclient import WebSocketClient
from .wsclient import WebSocketClientEventData

__all__ = [
  'ResponseCallback',
  'WebSocketJsonRpcClient',
]

ResponseCallback = Callable[[Any], Coroutine[None, None, None]]
WebSocketJsonRpcClientOnMessage = Callable[[dict], Coroutine[None, None, None]]

NotificationType = TypeVar('NotificationType')
NotificationData = TypeVar('NotificationData')


class WebSocketJsonRpcClient(WebSocketClient, Generic[NotificationType, NotificationData]):
  def __init__(
    self,
    *,
    user_agent: str,
    logger: logging.Logger,
    ssl: SSLContext | None = None,
  ) -> None:
    super().__init__(user_agent=user_agent, logger=logger, ssl=ssl)

    self._request_callbacks: dict[int, ResponseCallback] = {}
    self._error_callbacks: dict[int, ResponseCallback] = {}
    self._request_id = 1

  async def on_message_received(self, message: WebSocketClientEventData) -> None:
    data = json.loads(message)

    if 'id' in data:
      await self._handle_message_dict(data)
    else:
      await self._handle_message_notification(data)

  async def _handle_message_dict(self, data: dict) -> None:
    request_id = data['id']

    if 'error' in data:
      if request_id in self._error_callbacks:
        await self._error_callbacks[request_id](data['error'])
        del self._error_callbacks[request_id]
    else:
      if request_id in self._request_callbacks:
        await self._request_callbacks[request_id](data['result'])
        del self._request_callbacks[request_id]

  async def _handle_message_notification(self, data: dict) -> None:
    await self._event_manager.trigger(data['method'], data['params'])

  async def send_request(
    self,
    method: str,
    params: list | dict | None = None,
    *,
    on_response: ResponseCallback | None = None,
    on_error: ResponseCallback | None = None,
  ) -> None:
    data = {
      'id': self._request_id,
      'jsonrpc': '2.0',
      'method': method,
    }

    if params is not None:
      data['params'] = params

    if on_response is not None:
      self._request_callbacks[self._request_id] = on_response

    if on_error is not None:
      self._error_callbacks[self._request_id] = on_error

    await self.send_json(data)
    self._request_id += 1

  async def exec(
    self,
    method: str,
    params: list | dict | None = None,
  ) -> Any:
    event = EventData()

    async def on_response(data: Any) -> None:
      event.data = data
      event.set()

    async def on_error(error_message: str) -> None:
      event.failed(Exception(error_message))

    await self.send_request(method, params, on_response=on_response, on_error=on_error)
    await event.wait()

    return event.data
