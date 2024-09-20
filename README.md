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

#### Python
```python
from spreadsheet_extractor import get_config, Source

config = get_config(
    config_name="source_config",
    config_path="/path/to/source/config/folder"     # Optional if SPREADSHEET_EXTRACTOR_CONFIG_PATH is defined
)
source = Source(
    source_config=config,                           
    data_path="/path/to/data/folder"              # Optional if DATA_PATH is defined
)
source.load()
```

## Useful links
- [Spreasheet Extractor configuration](/src/configuration.md)
- [Spreasheet Extractor development](/src/development.md)
- [Spreasheet Extractor README](/src/README.md)
