from spreadsheet_extractor import get_config


def test_get_source(
    source_config_name,
    source_config_path,
    source_name
):
    config = get_config(
        source_config_name,
        source_config_path
    )

    assert config.name == source_name