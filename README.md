# Spreadsheet Extractor
Write YAML to extract data from spreadsheet files

## Usage

### Define source configuration
See [Spreasheet Extractor configuration](/src/configuration.md)

### Run Spreadsheet Extractor

#### CLI
```bash
spex source_config /path/to/source/config/folder /path/to/data/folder
```
***Tip** : If you set the `DATA_PATH` & `SPREADSHEET_EXTRACTOR_CONFIG_PATH` environment variables, you will only have to provide the `source_config`*

#### Python
```python
from spreadsheet_extractor import get_config, Source

config = get_config(
    "source_config",
    "/path/to/source/config/folder"
)
source = Source(config, "/path/to/data/folder")
source.load()
```

## Useful links
- [Spreasheet Extractor configuration](/src/configuration.md)
- [Spreasheet Extractor development](/src/development.md)
- [Spreasheet Extractor README](/src/README.md)