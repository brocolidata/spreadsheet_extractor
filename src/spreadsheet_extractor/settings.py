import os
import pathlib


def get_data_path() -> pathlib.Path:
    if path_str := os.getenv("DATA_PATH"):
        return pathlib.Path(path_str)
    else:
        raise RuntimeError("'DATA_PATH' env var must be set or use the 'data_path' arg")

def get_config_path() -> pathlib.Path:
    if path_str := os.getenv("SPREADSHEET_EXTRACTOR_CONFIG_PATH"):
        return pathlib.Path(path_str)
    else:
        raise RuntimeError("'SPREADSHEET_EXTRACTOR_CONFIG_PATH' env var must be set or use the 'config_path' arg")
    

EXTRACTS_FOLDER = 'extracts'
LOAD_FOLDER = 'raw'


def get_load_path(data_path=None) -> pathlib.Path:
    data_path = data_path or get_data_path()
    return pathlib.Path(
        data_path,
        LOAD_FOLDER
    )
