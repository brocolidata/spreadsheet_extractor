# Spreadsheet Extractor Development 

## Manage project using uv
We are using [uv](https://docs.astral.sh/uv/) to package the libaries and manage their dependencies.
All settings are defined in a `pyproject.toml` and all dependencies locked in a `uv.lock`.

## Manage dependencies

### Add a new dependency
```
uv add a_pip_installable_package
```

### Update dependencies
```
uv sync
```
### Remove a dependency
```
uv remove a_pip_installable_package
```