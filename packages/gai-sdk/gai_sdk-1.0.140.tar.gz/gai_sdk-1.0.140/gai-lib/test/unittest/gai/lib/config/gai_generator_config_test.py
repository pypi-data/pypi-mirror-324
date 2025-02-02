import pytest
from unittest.mock import patch, mock_open, MagicMock,call
import yaml

mock_yaml_data= {
    "version": "1.0",
    "generators": {
        "ttt-exllamav2-dolphin": {
            "type": "ttt",
            "engine": "exllamav2",
            "model": "dolphin",
            "name": "ttt-exllamav2-dolphin",
            "module":{
                "name": "gai.ttt.server.gai_exllamav2",
                "class": "GaiExllamav2"
            }
        }
    }
}

# GaiGeneratorConfig should load from "~/.gai/gai.yml" by default
@patch("yaml.load", return_value=mock_yaml_data)
@patch("builtins.open", new_callable=mock_open, read_data="version: 1.0\ngai_url: http://localhost")
@patch("gai.lib.common.utils.get_app_path", return_value="~/.gai")
def test_from_path_default(mock_app_path, mock_file, mock_yaml_load):
    from gai.lib.config import GaiGeneratorConfig
    
    # Load GaiConfig from default path
    config = GaiGeneratorConfig.from_name("ttt-exllamav2-dolphin")
    
    # Ensure only ~/.gai/gai.yml was opened
    mock_file.assert_called_once_with("~/.gai/gai.yml", 'r')
    assert len(mock_file.call_args_list) == 1
    
    assert config.module.name == "gai.ttt.server.gai_exllamav2"

# GaiGeneratorConfig should load from custom file path if provided
@patch("yaml.load", return_value=mock_yaml_data)
@patch("builtins.open", new_callable=mock_open, read_data="version: 1.0\ngai_url: http://localhost")
@patch("gai.lib.common.utils.get_app_path", return_value="~/.gai")
def test_from_custom_path(mock_app_path, mock_file, mock_yaml_load):
    from gai.lib.config import GaiGeneratorConfig
    
    # Load GaiConfig from default path
    config = GaiGeneratorConfig.from_name("ttt-exllamav2-dolphin", file_path="/tmp/gai.yml")
    
    # Ensure only ~/.gai/gai.yml was opened
    mock_file.assert_called_once_with("/tmp/gai.yml", 'r')
    assert len(mock_file.call_args_list) == 1
    
    assert config.module.name == "gai.ttt.server.gai_exllamav2"

# GaiGeneratortConfig should not load from any file if the config is provided
@patch("yaml.load", return_value=mock_yaml_data)
@patch("builtins.open", new_callable=mock_open, read_data="version: 1.0\ngai_url: http://localhost")
@patch("gai.lib.common.utils.get_app_path", return_value="~/.gai")
def test_from_dict(mock_app_path, mock_file, mock_yaml_load):
    from gai.lib.config import GaiGeneratorConfig
    
    # Load GaiConfig from default path
    config = GaiGeneratorConfig.from_dict({
        "type": "ttt",
        "engine": "llamacpp",
        "model": "dolphin",
        "name": "ttt-llamacpp-dolphin",
        "module":{
            "name": "gai.ttt.server.gai_llamacpp",
            "class": "GaiLlamaCpp"
        }
    })
    
    assert config.module.name == "gai.ttt.server.gai_llamacpp"
    
    # Ensure only ~/.gai/gai.yml was opened
    assert len(mock_file.call_args_list) == 0


