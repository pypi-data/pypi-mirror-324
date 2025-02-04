import threading
from typing import TYPE_CHECKING

import click

from src.core.runner import get_runner
from src.core.websocket_base import WebSocketClientBase
from src.models import message
from src.utils.credentials import cred

if TYPE_CHECKING:
    from src.utils.credentials import Credential


class WebSocketClient(WebSocketClientBase):
    def __init__(self, url: str, cred: "Credential" = cred):
        super().__init__(url, cred)
        self.code_stack: list[str] | str = []
        self.review_stack: list[str] | str = []
        self.is_code_review_finished = threading.Event()
        self.is_generate_code_finished = threading.Event()
        self.is_start_generate_code = threading.Event()

    def success(self, data: message.SuccessMessage):
        pass

    def error(self, data: message.ErrorMessage):
        print(f"error: {data}")
        pass

    def alert(self, data: message.AlertMessage):
        pass

    def abort(self, data: message.AbortMessage):
        click.echo(click.style("( @_@) : Abort command by user", fg="red"), err=True)
        runner = get_runner()
        if runner:
            runner.terminate()

    def log_finish(self, data: message.FinishLogAnalysis):
        click.echo("Finish log analysis")
        self.log_finished.set()

    def code_chunk(self, data: message.CodeGenerateChunk):
        if not self.is_start_generate_code.is_set():
            self.is_start_generate_code.set()
        self.code_stack.append(data.chunk)  # type: ignore
        click.echo(data.chunk, nl=False)

    def code_finished(self, data: message.CodeGenerateFinished):
        self.is_generate_code_finished.set()

    def code_review_chunk(self, data: message.CodeReviewChunk):
        self.review_stack.append(data.chunk)  # type: ignore
        click.echo(data.chunk, nl=False)

    def code_review_finished(self, data: message.CodeReviewFinished):
        self.is_code_review_finished.set()
