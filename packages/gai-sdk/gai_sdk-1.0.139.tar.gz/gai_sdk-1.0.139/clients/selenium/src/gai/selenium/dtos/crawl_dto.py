from pydantic import BaseModel
from typing import Optional
    
class CrawlJob(BaseModel):
    job_id: str
    root_url: str
    max_depth: int
    max_count: int
    include_external: bool
    status: str
    result: Optional[dict]

class CrawlTreeNode(BaseModel):
    title: str
    url: str
    depth: int
    parent: Optional[str]=None
    children: Optional[list]=[]
    
class CrawlRequest(BaseModel):
    root_url: str
    max_depth: int
    max_count: int
    include_external: bool
    force: Optional[bool] = False
    parser_type: Optional[str] = None

class UrlRequest(BaseModel):
    url: str
