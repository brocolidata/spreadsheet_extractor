from typing import Optional

import typer
from typing_extensions import Annotated

from spreadsheet_extractor import Source, get_config

app = typer.Typer()

source_config_name_param = Annotated[
    str, 
    typer.Argument(
        help="Name of the source setting file (without file extension)"
    )
]

source_config_path_param = Annotated[
    Optional[str], 
    typer.Argument(
        help="Path to the source settings folder",
        envvar="SPREADSHEET_EXTRACTOR_CONFIG_PATH"
    )
]

data_path_option = Annotated[
    Optional[str], 
    typer.Argument(
        help="Path to the data folder",
        envvar="DATA_PATH"
    )
]

@app.command("run")
def run(
    source_config_name: source_config_name_param, 
    source_config_path: source_config_path_param, 
    data_path: data_path_option
):
    
    config = get_config(
        source_config_name,
        source_config_path
    )
    source = Source(config, data_path)
    source.load()


if __name__ == "__main__":
    app()