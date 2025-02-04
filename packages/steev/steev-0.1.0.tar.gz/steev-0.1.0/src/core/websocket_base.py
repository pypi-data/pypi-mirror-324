import logging
from threading import Event, Thread
from typing import TYPE_CHECKING, Optional

import click
import websocket

from src.models.message import parse_model
from src.settings import WS_BASE_URL
from src.utils.credentials import cred
from src.utils.print import typing_print

if TYPE_CHECKING:
    from src.utils.credentials import Credential

logger = logging.getLogger(__name__)


class WebSocketClientBase:
    def __init__(self, url: str, cred: "Credential" = cred):
        self.url = WS_BASE_URL + url  # type: ignore
        self.ws: Optional[websocket.WebSocketApp] = None
        self.thread: Optional[Thread] = None
        self.cred = cred
        self.connected = Event()
        self.log_finished = Event()
        self.is_start_generate_code = Event()
        self.is_generate_code_finished = Event()
        self.is_start_code_review = Event()
        self.is_code_review_finished = Event()

    def on_message(self, ws, message):
        data = parse_model(message)
        if hasattr(data, "type"):
            handler_name = data.type.replace(".", "_")
            handler = getattr(self, f"{handler_name}", None)
            if handler:
                handler(data)

    def on_error(self, ws, error):
        # logger.error(f"Error: {error}")
        pass

    def on_close(self, ws, close_status_code, close_msg):
        if close_status_code == 4001:  # Authentication error
            click.echo("Authentication failed", err=True)
        elif close_status_code == 4002:  # Validation error
            click.echo("Validation failed", err=True)
        else:
            # click.echo(
            #     f"Connection closed with code {close_status_code}: {close_msg}",
            #     err=True,
            # )
            typing_print(
                "Finish connection with server", delay=0, color="black", keywords=["Finish connection with server"]
            )
        self.connected.clear()

    def on_open(self, ws):
        typing_print(
            "steev server connected",
            color="black",
            keywords=["steev server connected"],
            delay=0,
        )
        self.connected.set()  # 연결이 완료되면 Event를 set

    def connect(self):
        self.ws = websocket.WebSocketApp(
            self.url,
            header={"Authorization": f"Bearer {self.cred.token['access_token']}"},
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open,
        )
        self.thread = Thread(target=self.ws.run_forever)
        self.thread.daemon = True
        self.thread.start()

        if not self.connected.wait(timeout=10):
            typing_print(
                "steev server connection timeout",
                color="red",
                keywords=["steev server connection timeout"],
                delay=0,
            )
            self.close()
            return False

        return True

    def close(self):
        if self.ws:
            self.ws.close()
        self.connected.clear()

    def send(self, message: str):
        if not self.ws or not self.connected.is_set():
            typing_print(
                "steev server is not connected",
                color="red",
                keywords=["steev server is not connected"],
                delay=0,
            )
            return False
        try:
            self.ws.send(message)
            return True
        except Exception as e:
            typing_print(
                f"Failed to send message: {e}",
                color="red",
                keywords=[str(e)],
                delay=0,
            )
            return False

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connected.is_set():
            typing_print(
                "\nFinishing connection in 3 seconds",
                color="black",
                keywords=["Finishing connection in 3 seconds"],
                delay=0,
            )
            self.wait_for_finish(3)
        self.close()

    def wait_for_finish(self, timeout: int | None = None):
        self.log_finished.wait(timeout)
        self.log_finished.clear()
