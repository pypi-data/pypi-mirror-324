import pytest
from unittest.mock import patch, mock_open, MagicMock,call
import yaml

mock_yaml_data= {
    "version": "1.0",
    "gai_url": "http://localhost:8080",
    "logging": {
        "level": "DEBUG",
        "format": "%(levelname)s - %(message)s"
    },
    "clients": {
        "ttt": {
            "type": "ttt",
            "engine": "ollama",
            "model": "llama3.1",
            "name": "llama3.1",
            "client_type": "ollama"
        }
    }
}

# GaiClientConfig should load from "~/.gai/gai.yml" by default
@patch("yaml.load", return_value=mock_yaml_data)
@patch("builtins.open", new_callable=mock_open, read_data="version: 1.0\ngai_url: http://localhost")
@patch("gai.lib.common.utils.get_app_path", return_value="~/.gai")
def test_from_path_default(mock_yaml_load, mock_file, mock_app_path):
    from gai.lib.config import GaiClientConfig
    
    # Load GaiConfig from default path
    config = GaiClientConfig.from_name("ttt")
    
    # Ensure only ~/.gai/gai.yml was opened
    mock_file.assert_called_once_with("~/.gai/gai.yml", 'r')
    assert len(mock_file.call_args_list) == 1

# GaiClientConfig should load from custom file path if provided
@patch("yaml.load", return_value=mock_yaml_data)
@patch("builtins.open", new_callable=mock_open, read_data="version: 1.0\ngai_url: http://localhost")
@patch("gai.lib.common.utils.get_app_path", return_value="~/.gai")
def test_from_custom_path(mock_yaml_load, mock_file, mock_app_path):
    from gai.lib.config import GaiClientConfig
    
    # Load GaiConfig from default path
    config = GaiClientConfig.from_name("ttt", file_path="/tmp/gai.yml")
    
    # Ensure only ~/.gai/gai.yml was opened
    mock_file.assert_called_once_with("/tmp/gai.yml", 'r')
    assert len(mock_file.call_args_list) == 1

# GaiClientConfig should not load from any file if the config is provided
@patch("yaml.load", return_value=mock_yaml_data)
@patch("builtins.open", new_callable=mock_open, read_data="version: 1.0\ngai_url: http://localhost")
@patch("gai.lib.common.utils.get_app_path", return_value="~/.gai")
def test_from_dict(mock_yaml_load, mock_file, mock_app_path):
    from gai.lib.config import GaiClientConfig
    
    # Load GaiConfig from default path
    config = GaiClientConfig.from_dict({
        "type": "ttt",
        "engine": "ollama",
        "model": "llama3.1",
        "name": "llama3.1",
        "client_type": "ollama"
    })
    
    # Ensure only ~/.gai/gai.yml was opened
    assert len(mock_file.call_args_list) == 0


