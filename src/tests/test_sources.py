from spreadsheet_extractor import Source


def test_sources(source_name, source_config):
    source = Source(source_config)
    assert source.name == source_name


def test_source_load(source):
    source.load()