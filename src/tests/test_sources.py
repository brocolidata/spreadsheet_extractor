from spreadsheet_extractor import Source


def test_sources(source_name, source_config):
    source = Source(source_config)
    assert source.name == source_name


def test_data_range_extraction(source, ipp_fixture):
    test_dataset_name = (
        "Indice des prix à la production industrielle,énergétique et minière"
    )
    test_data_range = 2019
    test_data_range = source.datasets[test_dataset_name].data_ranges[test_data_range]
    test_data_range.extract()
    ## Dropping arabic label because it's too complicated to standardize the format
    # fmt: off
    valid_df = (
        ipp_fixture
        .drop(columns=["libelle_ar"])
    )
    tested_df = (
        test_data_range.raw_df
        .drop(columns=["libelle_ar"])
    )
    # fmt: on
    assert tested_df.equals(valid_df)


# def test_source_load(source):
#     source.load()
