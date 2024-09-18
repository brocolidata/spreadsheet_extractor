import pathlib

import pandas as pd
import pytest

from spreadsheet_extractor import Source, get_config
from spreadsheet_extractor.utils.columns import process_arabic_str


@pytest.fixture
def source_config_name():
    return "indice_des_prix"


@pytest.fixture
def source_name():
    return "Indice des Prix"


@pytest.fixture
def source_config(source_config_name):
    return get_config(source_config_name)


@pytest.fixture
def source(source_config):
    return Source(source_config)


@pytest.fixture
def ipp_fixture():
    file_path = pathlib.Path(
        "/spreadsheet_extractor/src/tests/assets", "fixtures", "ipp.parquet"
    )
    # fmt: off
    df = (
        pd.read_parquet(file_path)
        .assign(
            libelle_ar=lambda df_: df_.libelle_ar.apply(process_arabic_str)
        )
    )
    # fmt: on
    return df
