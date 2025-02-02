from gai.lib.common.http_utils import http_post_async, http_get_async
from gai.lib.config import GaiClientConfig
from ..dtos import SearchRequest, SearchResponse, ScrapeRequest, ParsedResponse, CrawlRequest, UrlRequest, CrawlJob

from typing import Optional, Union

class SeleniumClient:
    
    def __init__(self, config: Optional[Union[GaiClientConfig|dict]]=None,name:Optional[str]="gai-selenium", file_path:str=None):
        # Load from default config file
        self.config:GaiClientConfig = None
        
        # Convert to ClientLLMConfig
        if isinstance(config, dict):
            # Load default config and patch with provided config
            self.config = GaiClientConfig.from_dict(config)
        elif isinstance(config, GaiClientConfig):
            self.config = config
        elif name:
            # If path is provided, load config from path
            self.config = GaiClientConfig.from_name(name=name,file_path=file_path)
        else:
            raise ValueError(f"__init__: Invalid config or path provided")
        
        if self.config.client_type != "gai":
            raise ValueError(f"__init__: Invalid client type. client_type={self.config.client_type}")
    
    async def search(self, query:str, n_results:int=10, period=None) -> SearchResponse:
        # curl -X POST "http://localhost:12028/api/v1/googler" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"query\":\"python\",\"n_results\":5}"
        
        url = f'{self.config.url}/search'
        params = SearchRequest(query=query, n_results=n_results, period=period).model_dump(exclude_none=True)
        results = await http_post_async(url, data=params)
        return SearchResponse(**results.json())
    
    async def scrape(self, root_url:str, force:bool=False) -> ParsedResponse:
        # curl -X POST "http://localhost:12028/api/v1/scrape" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"url\":\"https://www.bbc.com/news/world-europe-60575619\"}"
        
        url = f'{self.config.url}/scrape'
        params = ScrapeRequest(url=root_url,force=force).model_dump(exclude_none=True)
        results = await http_post_async(url, data=params, timeout=240)
        return ParsedResponse(**results.json())
    
    async def crawl(self, root_url:str, max_depth:int, max_count:int, include_external:bool=False,force:bool=False, parser_type:str=None) -> CrawlJob:
        # curl -X POST "http://localhost:12028/api/v1/crawl" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"root_url\":\"https://www.bbc.com/news/world-europe-60575619\",\"max_depth\":2,\"max_count\":5,\"include_external\":false}"
        
        url = f'{self.config.url}/crawl'
        params = CrawlRequest(root_url=root_url, max_depth=max_depth, max_count=max_count, include_external=include_external,force=force,parser_type=parser_type).model_dump(exclude_none=True)
        results = await http_post_async(url, data=params)
        return CrawlJob(**results.json())
    
    async def get_crawl_job(self, job_id:str) -> CrawlJob:
        # curl -X GET "http://localhost:12028/api/v1/crawl/job/1" -H  "accept: application/json"
        
        url = f'{self.config.url}/crawl/job/{job_id}'
        results = await http_get_async(url)
        return CrawlJob(**results.json())

    async def get_html_text(self, root_url:str):
        # curl -X POST "http://localhost:12028/api/v1/html" -H  "accept: application/json" -d "{\"url\":\"https://www.bbc.com/news/world-europe-60575619\"}"
        
        url = f'{self.config.url}/html'
        params = UrlRequest(url=root_url).model_dump(exclude_none=True)
        results = await http_post_async(url,data=params)
        return results.json()

    async def get_parsed_text(self, root_url:str) -> ParsedResponse:
        # curl -X POST "http://localhost:12028/api/v1/parsed" -H  "accept: application/json" -d "{\"url\":\"https://www.bbc.com/news/world-europe-60575619\"}"
        
        url = f'{self.config.url}/parsed'
        params = UrlRequest(url=root_url).model_dump(exclude_none=True)
        results = await http_post_async(url,data=params)
        return ParsedResponse(**results.json())