import json
from typing import Literal

from pydantic import BaseModel, RootModel

from .log import LogModel


class SuccessMessage(BaseModel):
    type: Literal["success"] = "success"
    message: str


class ErrorMessage(BaseModel):
    type: Literal["error"] = "error"
    message: str


class AlertMessage(BaseModel):
    type: Literal["alert"] = "alert"
    message: str


class AbortMessage(BaseModel):
    type: Literal["abort"] = "abort"


class FinishLogAnalysis(BaseModel):
    type: Literal["log.finish"] = "log.finish"


class CodeGenerateChunk(BaseModel):
    type: Literal["code.chunk"] = "code.chunk"
    chunk: str


class CodeGenerateFinished(BaseModel):
    type: Literal["code.finished"] = "code.finished"
    code: str


class CodeReviewFinished(BaseModel):
    type: Literal["code.review.finished"] = "code.review.finished"
    review: str


class CodeReviewChunk(BaseModel):
    type: Literal["code.review.chunk"] = "code.review.chunk"
    chunk: str


class CodeReviewRequest(BaseModel):
    type: Literal["code.review"] = "code.review"
    experiment_id: str


ReceiveMessageUnion = (
    SuccessMessage
    | ErrorMessage
    | AlertMessage
    | AbortMessage
    | FinishLogAnalysis
    | CodeGenerateChunk
    | CodeGenerateFinished
    | CodeReviewFinished
    | CodeReviewRequest
    | CodeReviewChunk
)


class ReceiveMessage(RootModel[ReceiveMessageUnion]):
    pass


def parse_model(data: dict | str | bytes) -> ReceiveMessageUnion:
    if isinstance(data, str):
        data = json.loads(data)
    elif isinstance(data, bytes):
        data = json.loads(data.decode("utf-8"))
    return ReceiveMessage.model_validate(data).root


# --------------------------------------------------------------
# send
# --------------------------------------------------------------


class LogMessage(BaseModel):
    type: Literal["log"] = "log"
    experiment_id: str
    log: LogModel


class ExperimentEnded(BaseModel):
    type: Literal["exp.ended"] = "exp.ended"
    experiment_id: str


class CodeGenerateRequest(BaseModel):
    type: Literal["code.generate"] = "code.generate"
    experiment_id: str
