import os
import pathlib

import pytest

from spreadsheet_extractor import Source, get_config


@pytest.fixture
def source_config_name():
    return "indice_des_prix"

@pytest.fixture
def source_name():
    return "Indice des Prix"


@pytest.fixture
def source_config_path():
    # return pathlib.Path(os.getcwd(), 'assets', 'sources' )
    return pathlib.Path(os.getcwd(),'tests', 'assets', 'sources' )


@pytest.fixture
def source_config(source_config_name, source_config_path):
    return get_config(
        source_config_name,
        source_config_path
    )


@pytest.fixture
def data_path():
    return pathlib.Path(os.getcwd(),'tests', 'assets')


@pytest.fixture
def source(source_config, data_path):
    return Source(source_config, data_path)