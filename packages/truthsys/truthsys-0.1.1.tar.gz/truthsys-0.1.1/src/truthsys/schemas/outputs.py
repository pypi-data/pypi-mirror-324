from typing import Annotated, List, NamedTuple, Tuple

from pydantic import BaseModel, Field

from .common import Top5Sentences
from .enums import PredictionEnum, PredictionNumEnum


class PredictionVector(NamedTuple):
    refutes: Annotated[float, Field(ge=0, le=1)]
    not_enough_info: Annotated[float, Field(ge=0, le=1)]
    supports: Annotated[float, Field(ge=0, le=1)]


class HallucinationDetectionResponse(BaseModel):
    prediction_vector: PredictionVector
    prediction: PredictionEnum
    prediction_num: PredictionNumEnum
    atomic: str
    top5_sentences: Top5Sentences
    span: Tuple[int, int]


class EvidenceResponse(BaseModel):
    source_spans: List[Tuple[int, int]]
    ids: List[str]
    scores: List[List[float]]


class SentenceMergeResponse(BaseModel):
    verdict: PredictionNumEnum
    evidence: EvidenceResponse
    span: Tuple[int, int]
