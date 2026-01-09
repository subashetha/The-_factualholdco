from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ==============================================================================
# DATA MODELS
# ==============================================================================
# Why Pydantic?
# 1. Validation: Automatically ensures our data matches the required types.
# 2. Serialization: Easily converts to JSON for the API response.
# 3. Documentation: Serves as self-documenting code for what the API returns.
# ==============================================================================

class Meta(BaseModel):
    ticker: str
    timestamp: datetime

class MarketData(BaseModel):
    price: float
    change_percent: float
    volume: int

class Reasoning(BaseModel):
    thesis: str
    risk: str

class SnapshotResponse(BaseModel):
    meta: Meta
    data: MarketData
    reasoning: Reasoning
