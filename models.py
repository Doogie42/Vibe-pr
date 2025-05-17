from pydantic import BaseModel
from typing import List


class PromptResponseIssue(BaseModel):
    description: str
    confidence: float


class PromptResponse(BaseModel):
    summary: str
    suggested_title: str
    issues: List[PromptResponseIssue]
