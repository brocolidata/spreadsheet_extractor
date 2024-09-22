# Spreadsheet Extractor
Write YAML to extract data from spreadsheet files

## Installation

```
pip install https://github.com/brocolidata/spreadsheet_extractor/releases/download/spreadsheet_extractor_v0.2.0/spreadsheet_extractor-0.2.0-py3-none-any.whl
```
or add this to your `requirements.txt`
```
https://github.com/brocolidata/spreadsheet_extractor/releases/download/spreadsheet_extractor_v0.2.0/spreadsheet_extractor-0.2.0-py3-none-any.whl
```

## Usage

### Define source configuration
See [Spreasheet Extractor configuration](/src/configuration.md)

### Run Spreadsheet Extractor

The example below uses the tests source configuration : [`indice_des_prix.yaml`](src/tests/assets/sources/indice_des_prix.yaml)

#### Python
```python
from spreadsheet_extractor import get_config, Source

DATASET_NAME = "Indice des prix à la production industrielle,énergétique et minière"
DATA_RANGE_YEAR = 2022

config = get_config(
    config_name="source_config",
    config_path="/path/to/source/config/folder"     # Optional if SPREADSHEET_EXTRACTOR_CONFIG_PATH is defined
)

source = Source(
    source_config=config,                           
    data_path="/path/to/data/folder"              # Optional if DATA_PATH is defined
)

ipp_dataset = source.datasets[DATASET_NAME]
ipp_data_range_2022 = ipp_dataset.data_ranges[DATA_RANGE_YEAR]
ipp_data_range_2022.extract()
df_ipp_2022 = ipp_data_range_2022.raw_df
## ...
```

## Useful links
- [Spreasheet Extractor configuration](/src/configuration.md)
- [Spreasheet Extractor development](/src/development.md)
- [Spreasheet Extractor README](/src/README.md)
