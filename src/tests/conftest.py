
import pytest

from spreadsheet_extractor import Source, get_config


@pytest.fixture
def source_config_name():
    return "indice_des_prix"

@pytest.fixture
def source_name():
    return "Indice des Prix"


@pytest.fixture
def source_config(source_config_name):
    return get_config(
        source_config_name
    )


@pytest.fixture
def source(source_config):
    return Source(source_config)