import pytest, json, os
from unittest.mock import patch, MagicMock
from gai.ttt.client.ttt_client import TTTClient
from gai.lib.config import GaiClientConfig
from gai.lib.common.utils import get_app_path

from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from openai import OpenAI
import pytest

import sys
mock_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../mock_ttt"))
if mock_dir not in sys.path:
    sys.path.insert(0, mock_dir)
from mock_ttt import chat_completions_generate,chat_completions_stream,chat_completions_toolcall,chat_completions_json_schema


# @pytest.fixture
# def ttt_client():
#     return ttt_client()

mock_config = {
    "version": "1.0",
    "clients": {
        "ttt": {
            "type": "ttt",
            "engine": "exllamav2",
            "model": "dolphin",
            "name": "ttt-exllamav2-dolphin",
            "client_type": "gai",
            "url": "http://localhost:12031/gen/v1/chat/completions"
        },
        "ttt-exllamav2-dolphin": {
            "type": "ttt",
            "engine": "exllamav2",
            "model": "dolphin",
            "name": "ttt-exllamav2-dolphin",
            "client_type": "gai",
            "url": "http://localhost:12031/gen/v1/chat/completions"
        },
        "llama3.1": {
            "type": "ttt",
            "engine": "ollama",
            "model": "llama3.1",
            "name": "llama3.1",
            "client_type": "ollama"
        }
    }
}

"""
TTTClient() should get "ttt" config
"""
@patch("gai.lib.config.GaiClientConfig._get_gai_config", return_value=mock_config)
def test_ttt_client_init_no_params(mock_get_client_config):
    client = TTTClient()
    assert client.config.name == "ttt-exllamav2-dolphin"

"""
TTTClient(name="ttt-exllamav2-dolphin") should get "ttt-exllamav2-dolphin" config
"""
@patch("gai.lib.config.GaiClientConfig._get_gai_config", return_value=mock_config)
def test_ttt_client_init_w_name(mock_get_client_config):
    client = TTTClient(name="ttt-exllamav2-dolphin")
    assert client.config.name == "ttt-exllamav2-dolphin"

"""
TTTClient(config={"name":"llama3.1"}) should fail with client_type error
"""
@patch("gai.lib.config.GaiClientConfig._get_gai_config", return_value=mock_config)
def test_ttt_client_init_w_invalid_client_type(mock_get_client_config):
    try:
        client = TTTClient(name="llama3.1")
    except ValueError as e:
        assert str(e) == "__init__: Invalid client type. client_type=ollama"

    
"""
TTTClient(name="phi4") should fail with config not found error
"""
@patch("gai.lib.config.GaiClientConfig._get_gai_config", return_value=mock_config)
def test_ttt_client_init_w_invalid_config(mock_get_client_config):
    try:
        client = TTTClient(name="phi4")
    except ValueError as e:
        assert str(e) == "GaiClientConfig: Client Config not found. name=phi4"
    
"""
TTTClient(config={"name":"phi4"}) should get "phi4" config
"""
@patch("gai.lib.config.GaiClientConfig._get_gai_config", return_value=mock_config)
def test_ttt_client_init_w_config(mock_get_client_config):
    client = TTTClient(config={"client_type":"gai","name":"ttt-llamacpp-llama3.1"})
    assert client.config.name == "ttt-llamacpp-llama3.1"
    
"""
client.create(messages=[{"role":"user","content":"tell me a one sentence story"},stream=False]) should return a ChatCompletion object
"""
@patch("gai.ttt.client.TTTClient._generate_dict")
@patch("gai.lib.config.GaiClientConfig._get_gai_config", return_value=mock_config)
def test_ttt_client_generate(mock_gent_client_config, mock_generate):
    mock_generate.return_value = chat_completions_generate()

    client = TTTClient()
    response = client(messages=[{"role":"user","content":"tell me a one sentence story"}],stream=False)
    print(response)
    
    assert response.choices[0].message.function_call == None
    assert response.choices[0].message.tool_calls == None
    assert response.choices[0].finish_reason == "stop"

"""
client.create(messages=[{"role":"user","content":"tell me a one sentence story"},stream=true]) should return stream
"""
@patch("gai.ttt.client.TTTClient._stream_dict")
@patch("gai.lib.config.GaiClientConfig._get_gai_config", return_value=mock_config)
def test_ttt_client_stream(mock_gent_client_config, mock_stream):
    mock_stream.return_value = chat_completions_stream()

    client = TTTClient()
    response = client(messages=[{"role":"user","content":"tell me a one sentence story"}],stream=True)
    chunks = [chunk for chunk in response]

    # first chunk
    first_chunk = chunks[0]
    assert first_chunk.choices[0].finish_reason == None
    assert first_chunk.choices[0].delta.content == ""

    # last chunk
    last_chunk = chunks[-1]
    assert last_chunk.choices[0].finish_reason == "stop"

    # content    
    content = ""
    for chunk in chunks:
        if chunk.choices[0].delta.content:
            content += chunk.choices[0].delta.content
    assert content.strip() == 'An angry old drunk walks through the streets yelling at cars and throwing bottles.'

@patch("gai.ttt.client.TTTClient._generate_dict")
@patch("gai.lib.config.GaiClientConfig._get_gai_config", return_value=mock_config)
def test_ttt_client_toolcall(mock_gent_client_config, mock_generate):
    mock_generate.return_value = chat_completions_toolcall()

    client = TTTClient()
    messages = [
        {"role":"user","content":"What is the current time in Singapore?"},
        {"role":"assistant","content":""}
    ]
    tool_choice="required"
    tools = [
        {
            "type": "function",
            "function": {
                "name": "google",
                "description": "The 'google' function is a powerful tool that allows the AI to gather external information from the internet using Google search. It can be invoked when the AI needs to answer a question or provide information that requires up-to-date, comprehensive, and diverse sources which are not inherently known by the AI. For instance, it can be used to find current date, current news, weather updates, latest sports scores, trending topics, specific facts, or even the current date and time. The usage of this tool should be considered when the user's query implies or explicitly requests recent or wide-ranging data, or when the AI's inherent knowledge base may not have the required or most current information. The 'search_query' parameter should be a concise and accurate representation of the information needed.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "search_query": {
                            "type": "string",
                            "description": "The search query to search google with. For example, to find the current date or time, use 'current date' or 'current time' respectively."
                        }
                    },
                    "required": ["search_query"]
                }
            }
        }
    ]
    response=client(messages=messages,stream=False,tool_choice=tool_choice,tools=tools)

    assert response.choices[0].finish_reason == "tool_calls"    
    assert response.choices[0].message.tool_calls[0].function.arguments == '{"search_query": "current time in Singapore"}'
    assert response.choices[0].message.tool_calls[0].function.name == "google"

@patch("gai.ttt.client.TTTClient._generate_dict")
@patch("gai.lib.config.GaiClientConfig._get_gai_config", return_value=mock_config)
def test_ttt_client_json_schema(mock_gent_client_config, mock_generate):
    mock_generate.return_value = chat_completions_json_schema()

    client = TTTClient()
    from pydantic import BaseModel
    class Book(BaseModel):
        title: str
        summary: str
        author: str
        published_year: int

    response=client(
        messages=[
            {"role":"user","content":"""Foundation is a science fiction novel by American writer 
                Isaac Asimov. It is the first published in his Foundation Trilogy (later 
                expanded into the Foundation series). Foundation is a cycle of five 
                interrelated short stories, first published as a single book by Gnome Press 
                in 1951. Collectively they tell the early story of the Foundation, 
                an institute founded by psychohistorian Hari Seldon to preserve the best 
                of galactic civilization after the collapse of the Galactic Empire.
                """},
            {"role":"assistant","content":""}
            ],
        json_schema=Book.model_json_schema(),
        tool_choice="none",
        timeout=50,
        stream=False
        )    
    response.extract=None
    print(response.json())
    
    assert response.choices[0].finish_reason == "stop"
    assert response.choices[0].message.content == "{\n   \"title\": \"Foundation\",\n   \"summary\": \"Foundation is a science fiction novel by American writer Isaac Asimov. It is the first published in his Foundation Trilogy (later expanded into the Foundation series). Foundation is a cycle of five interrelated short stories, first published as a single book by Gnome Press in 1951. Collectively they tell the early story of the Foundation, an institute founded by psychohistorian Hari Seldon to preserve the best of galactic civilization after the collapse of the Galactic Empire.\",\n   \"author\": \"Isaac Asimov\",\n   \"published_year\": 1951\n }"
    