from typing import Annotated, List, Optional

from pydantic import BaseModel, Field

from .common import LLMInput, Source


class ReferenceInput(BaseModel):
    start: Annotated[int, Field(ge=0)]
    end: int
    # TODO: change this to uuids
    evidence_ids: List[str]


class HallucinationDetectionInput(BaseModel):
    # TODO: stronger definitions
    claim: str
    sources: List[Source]
    llm_input: Optional[List[LLMInput]] = None
