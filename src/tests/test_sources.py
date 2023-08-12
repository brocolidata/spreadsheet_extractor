from spreadsheet_extractor import Source


def test_sources(data_path, source_name, source_config):
    source = Source(source_config, data_path)
    assert source.name == source_name


def test_source_load(source):
    source.load()