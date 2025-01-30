import json
import queue
import time
from typing import Generic, List, TypeVar
from flask_sock import Sock, Server, ConnectionClosed
from shared_types import UDP_UP_MSG_TYPES
import threading

T = TypeVar("T")


class BaseFlaskSock(Generic[T]):
    def __init__(self, sock: Sock, rel_url: str):
        self._sock = sock
        self._sock.route(rel_url)(self.ws_route)
        self._data_queue = queue.Queue()
        self._ws_connections: List[Server] = []
        self._send_thread = threading.Thread(target=self._send)
        self._recv_thread = threading.Thread(target=self._recv)
        self._send_thread.daemon = True
        self._recv_thread.daemon = True
        self._send_thread.start()
        self._recv_thread.start()

    def on_open(self, ws: Server):
        """
        连接建立时调用，仅对新建立的websocket有效
        """
        pass

    def on_message(self, data):
        """
        处理收到的消息
        """
        pass

    def msg_to_log(self, msg: UDP_UP_MSG_TYPES):
        """
        将消息转换为日志类型
        要求：
        1. msg['type']为字符串
        2. msg['name']为字符串
        """
        msg = msg.copy()
        log_msg = {"time": time.time(), "name": msg.pop(
            "name"), "type": "log", "data": msg}
        return log_msg

    def send_data(self, data):
        self._data_queue.put(json.dumps(data))

    def _send(self):
        """
        Blocking send message
        """
        while True:
            data = self._data_queue.get()
            for ws in self._ws_connections:
                try:
                    ws.send(data)
                except ConnectionClosed as e:
                    self._ws_connections.remove(ws)

    def _recv(self):
        while True:
            for ws in self._ws_connections:
                try:
                    data = ws.receive(0.1)
                    if data is not None:
                        self.on_message(data)
                except ConnectionClosed as e:
                    self._ws_connections.remove(ws)
                    import traceback

                    traceback.print_exc()

    def ws_route(self, ws: Server):
        self._ws_connections.append(ws)
        self.on_open(ws)
        while True:
            time.sleep(1)
