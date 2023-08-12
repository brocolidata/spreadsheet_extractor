from spreadsheet_extractor.logger import logger
import pathlib

from omegaconf import OmegaConf, dictconfig

from spreadsheet_extractor import settings

def get_config(
    config_name: str, 
    config_path: pathlib.Path | None = None
) -> dictconfig.DictConfig:
    config_path = config_path or settings.get_config_path()
    config_file_path = pathlib.Path(config_path, f"{config_name}.yaml").as_posix()
    logger.info(f'config_path : {config_file_path}')
    return OmegaConf.load(config_file_path)


def get_available_year(historic_years, year):
    return list(range(year-1, year-(historic_years+1), -1))


def get_years_to_load(historic_years, years):
    years.sort(reverse=True)
    dc_available_years = {
        y:get_available_year(historic_years, y) for y in years
    }
    dc_years = {}
    for year in years:
        dc = {
            ay:year for ay in dc_available_years[year] if ay not in dc_years
        }
        dc_years.update(dc)
    return dc_years


