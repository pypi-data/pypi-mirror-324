from pydantic import BaseModel, Field
from typing import List, Optional, Any


class RiskCategory(BaseModel):
    name: str = Field(description="Name of the risk category")
    score: float = Field(description="Score of the risk category")
    risks: List[str] = Field(description="List of identified risk factors")


class Scorecard(BaseModel):
    categories: List[RiskCategory] = Field(description="Risk categories")
    assessment: str = Field(description="Overall Assessment")
    recommendation: str = Field(description="Mitigation Recommendations")


