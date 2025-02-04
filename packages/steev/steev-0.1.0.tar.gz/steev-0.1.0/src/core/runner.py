import subprocess
import sys
import threading
from datetime import datetime
from typing import TYPE_CHECKING

import click

from src.models.log import LogLevel, LogModel
from src.models.message import CodeGenerateRequest, CodeReviewRequest, ExperimentEnded, LogMessage
from src.utils.path import TempFile

if TYPE_CHECKING:
    from src.core.http_client import Client
    from src.core.websocket_client import WebSocketClient
    from src.utils.path import Path

runner = None


class Runner:
    def __init__(
        self,
        base_dir: "Path",
        client: "Client",
        ws: "WebSocketClient",
        experiment_id: str,
    ):
        self.base_dir = base_dir
        self.client: "Client" = client
        self.experiment_id: str = experiment_id
        self.ws: "WebSocketClient" = ws
        self.process: subprocess.Popen | None = None
        self.threads: list[threading.Thread] = []
        set_runner(self)

    def request_generate_code(self) -> str:
        self.ws.send(
            CodeGenerateRequest(
                experiment_id=self.experiment_id,
            ).model_dump_json()
        )
        if not self.ws.is_start_generate_code.wait(timeout=100):
            raise Exception("Failed to generate code")
        elif not self.ws.is_generate_code_finished.wait(timeout=100):
            raise Exception("Failed to generate code")
        return "".join(self.ws.code_stack)

    def request_code_review(self) -> str:
        self.ws.send(
            CodeReviewRequest(
                experiment_id=self.experiment_id,
            ).model_dump_json()
        )
        if not self.ws.is_code_review_finished.wait(timeout=100):
            raise Exception("Failed to review code")
        return "".join(self.ws.review_stack)

    def execute_train(self, code: str):
        def read_output(pipe, level: LogLevel = LogLevel.INFO):
            with pipe:
                for line in iter(pipe.readline, ""):
                    try:
                        # 터미널에 출력
                        if level:
                            click.echo(
                                f"[{level}] {line}",
                                nl=False,
                            )
                        # 웹소켓으로 전송
                        data = LogMessage(
                            experiment_id=self.experiment_id,
                            log=LogModel(
                                message=line,
                                timestamp=datetime.now().isoformat(),
                                level=level.value,
                            ),
                        )
                        self.ws.send(data.model_dump_json())
                    except Exception:
                        pass

        def run_subprocess(command):
            return subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                shell=False,
                encoding="utf-8",
                errors="replace",
            )

        def start_thread(target, args):
            thread = threading.Thread(target=target, args=args)
            thread.start()
            return thread

        with TempFile(dir=self.base_dir) as temp_file:
            temp_file.write(code)
            temp_file.flush()
            self.process = run_subprocess([sys.executable, "-u", str(temp_file.file_path)])

            if self.process is None:
                raise Exception("Failed to start process")

            self.threads = [
                start_thread(read_output, args=(self.process.stdout, LogLevel.INFO)),
                start_thread(read_output, args=(self.process.stderr, LogLevel.INFO)),
            ]
            self.process.wait()
            for thread in self.threads:
                thread.join()

        # Experiment ended
        self.ws.send(
            ExperimentEnded(
                experiment_id=self.experiment_id,
            ).model_dump_json()
        )

    def terminate(self):
        if self.process is not None:
            self.process.terminate()


def set_runner(r: "Runner"):
    global runner
    runner = r


def get_runner():
    return runner
