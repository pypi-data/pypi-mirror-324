from pydantic import BaseModel
from typing import Optional

class SearchRequest(BaseModel):
    query: str
    n_results: int = 10
    period: Optional[str]=None

class SearchResult(BaseModel):
    title: str
    link: str
    snippet: Optional[str]=""
    html_text: Optional[str]=None
    parsed_text: Optional[str]=None
    score: Optional[float]=None

class SearchResponse(BaseModel):
    query: str
    result: list[SearchResult]
