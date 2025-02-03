import pytest
from unittest.mock import patch, mock_open, MagicMock,call, AsyncMock
from gai.selenium.dtos import SearchResponse, SearchResult


mock_config = {
    "version": "1.0",
    "clients": {
        "gai-selenium": {
            "type": "scraper",
            "engine": "selenium",
            "model": "selenium",
            "name": "gai-selenium",
            "client_type": "gai",
            "url": "http://gai-selenium:12028/api/v1"
        },
    }
}

@pytest.fixture
def selenium_config():
    return {
        "type": "scraper",
        "engine": "selenium",
        "model": "selenium",
        "name": "gai-selenium",
        "client_type": "gai",
        "url": "http://localhost:12028/api/v1"
    }

"""
SeleniumClient() should get "gai-selenium" config from ~/.gai/gai.yml
"""
@patch("yaml.load", return_value=mock_config)
@patch("gai.lib.config.GaiClientConfig._get_gai_config", return_value=mock_config)
@patch("builtins.open", new_callable=mock_open)
@patch("gai.lib.common.utils.get_app_path", return_value="~/.gai")
def test_from_path_default(mock_load_yaml,mock_get_config, mock_file, mock_app_path):
    from gai.lib.config import GaiClientConfig
    
    # Load GaiConfig from default path
    config = GaiClientConfig.from_name("gai-selenium")
    
    # Ensure only ~/.gai/gai.yml was opened
    mock_file.assert_called_once_with("~/.gai/gai.yml")
    assert len(mock_file.call_args_list) == 1
    
    # Ensure the config is loaded correctly
    assert config.url == "http://gai-selenium:12028/api/v1"

"""
SeleniumClient() should get "gai-selenium" config from /tmp/gai.yml
"""
@patch("yaml.load", return_value=mock_config)
@patch("gai.lib.config.GaiClientConfig._get_gai_config", return_value=mock_config)
@patch("builtins.open", new_callable=mock_open)
@patch("gai.lib.common.utils.get_app_path", return_value="~/.gai")
def test_from_path_default(mock_load_yaml,mock_get_config, mock_file, mock_app_path):
    from gai.lib.config import GaiClientConfig
    
    # Load GaiConfig from default path
    config = GaiClientConfig.from_path("/tmp/gai.yml")
    
    # Ensure only ~/.gai/gai.yml was opened
    mock_file.assert_called_once_with("/tmp/gai.yml")
    assert len(mock_file.call_args_list) == 1
    
    # Ensure the config is loaded correctly
    assert config.url == "http://gai-selenium:12028/api/v1"

"""
SeleniumClient() should get "gai-selenium" config from constructor
"""
@patch("yaml.load", return_value=mock_config)
@patch("gai.lib.config.GaiClientConfig._get_gai_config", return_value=mock_config)
@patch("builtins.open", new_callable=mock_open)
@patch("gai.lib.common.utils.get_app_path", return_value="~/.gai")
def test_from_constructor_config(mock_load_yaml,mock_get_config, mock_file, mock_app_path):
    from gai.lib.config import GaiClientConfig
    
    # Load GaiConfig from constructor config
    config = GaiClientConfig.from_dict({
        "type": "scraper",
        "engine": "selenium",
        "model": "selenium",
        "name": "gai-selenium",
        "client_type": "gai",
        "url": "http://localhost:12028/api/v1"
    })
    
    # Ensure only ~/.gai/gai.yml was not opened
    assert len(mock_file.call_args_list) == 0
    
    # Ensure the config is loaded from constructor config
    assert config.url == "http://localhost:12028/api/v1"

# """
# SeleniumClient() call search() should call http_post_async("http://gai-selenium:12028/api/v1/search")
# """
@patch('gai.lib.common.http_utils.http_post_async', new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_search(mock_http_post_async, selenium_config):
    
    # Create a SeleniumClient instance with test config
    
    from gai.selenium.client import SeleniumClient
    selenium_client = SeleniumClient(selenium_config)
    
    # Mock the response from the HTTP POST
    
    mock_http_post_async.return_value = MagicMock()
    mock_http_post_async.return_value.json.return_value = {
        "result": [
            {"title": "Python", "link": "https://www.python.org", "snippet": "Python is a programming language"}
        ]
    }

    # Act
    
    search_response = await selenium_client.search(query="python", n_results=5)
    
    # Confirm parameters are passed correctly to HTTP POST
    
    mock_http_post_async.assert_called_once_with("http://localhost:12028/api/v1/search", data={"query": "python", "n_results": 5})

    # Confirm the response is parsed correctly from HTTP POST
    
    assert search_response.result[0].title == "Python"

@patch('gai.lib.common.http_utils.http_post_async', new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_scrape(mock_http_post_async, selenium_config):
    
    # Create a SeleniumClient instance with test config
    
    from gai.selenium.client import SeleniumClient
    client = SeleniumClient(selenium_config)
    
    mock_http_post_async.return_value = MagicMock()
    mock_http_post_async.return_value.json.return_value = {
        "source": "http://www.example.com",
        "title": "Example",
        "text": "Parsed text output",
        "length": 18,
        "created_at": "2022-01-01T00:00:00Z",
    }

    # Act
    
    scrape_response = await client.scrape("https://www.example.com", force=True)
    
    # Confirm parameters are passed correctly to HTTP POST
    mock_http_post_async.assert_called_once_with("http://localhost:12028/api/v1/scrape", data={"url": "https://www.example.com", "force": True}, timeout=240)

    # Confirm the response is parsed correctly from HTTP POST
    assert scrape_response.source == "http://www.example.com"
    assert scrape_response.title == "Example"
    
    from gai.selenium.dtos import ParsedResponse
    assert isinstance(scrape_response, ParsedResponse)


@patch('gai.lib.common.http_utils.http_post_async', new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_crawl(mock_http_post_async, selenium_config):
    
    # Create a SeleniumClient instance with test config
    
    from gai.selenium.client import SeleniumClient
    client = SeleniumClient(selenium_config)

    mock_http_post_async.return_value = MagicMock()
    mock_http_post_async.return_value.json.return_value = {
        "job_id": "123",
        "status": "running",
        "root_url": "https://www.example.com",
        "max_depth": 2,
        "max_count": 5,
        "include_external": False,
        "force": True,
        "parser_type": "html",
        "result": {"progress": "50%", "urls": ["https://www.example.com/page1", "https://www.example.com/page2"]}
    }
    
    # Act
    crawl_response = await client.crawl("https://www.example.com", max_depth=2, max_count=5, include_external=False, force=True, parser_type="html")

    # Confirm parameters are passed correctly to HTTP POST
    mock_http_post_async.assert_called_once_with("http://localhost:12028/api/v1/crawl", data={
        "root_url": "https://www.example.com",
        "max_depth": 2,
        "max_count": 5,
        "include_external": False,
        "force": True,
        "parser_type": "html"
    })

    # Confirm the response is parsed correctly from HTTP POST
    assert crawl_response.job_id == "123"
    assert crawl_response.status == "running"
    assert crawl_response.result["progress"] == "50%"
    
    from gai.selenium.dtos import CrawlJob
    assert isinstance(crawl_response, CrawlJob)

    
