
import typer
from rich.prompt import Prompt
from typing_extensions import Annotated

from spreadsheet_extractor import Source, get_config

app = typer.Typer()

SOURCE_CONFIG_NAME_HELP = "Name of the source setting file (without file extension)"
SOURCE_CONFIG_PATH_HELP = "Path to the source settings folder"
DATA_PATH_HELP = "Path to the data folder"

source_config_name_param = Annotated[
    str, 
    typer.Option(
        help=SOURCE_CONFIG_NAME_HELP,
        prompt=True
    )
]

source_config_path_param = Annotated[
    str, 
    typer.Option(
        help=SOURCE_CONFIG_PATH_HELP,
        envvar="SPREADSHEET_EXTRACTOR_CONFIG_PATH",
        prompt=True
    )
]

data_path_option = Annotated[
    str, 
    typer.Option(
        help=DATA_PATH_HELP,
        envvar="DATA_PATH",
        prompt=True
    )
]

@app.command("run")
def run(
    source_config_name: source_config_name_param, 
    source_config_path: source_config_path_param, 
    data_path: data_path_option
):
    source_config_name = source_config_name or Prompt.ask(f'{SOURCE_CONFIG_NAME_HELP}')
    source_config_path = source_config_path or Prompt.ask(f'{SOURCE_CONFIG_PATH_HELP}')
    data_path = data_path or Prompt.ask(f'{DATA_PATH_HELP}')
    config = get_config(
        source_config_name,
        source_config_path
    )
    source = Source(config, data_path)
    source.load()


if __name__ == "__main__":
    app()