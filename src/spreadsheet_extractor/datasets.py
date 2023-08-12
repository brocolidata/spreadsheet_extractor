import pathlib
from omegaconf import OmegaConf
import pandas as pd

from spreadsheet_extractor import (
    data_ranges, settings
)

from spreadsheet_extractor.logger import logger
from spreadsheet_extractor.utils import columns as column_utils
from spreadsheet_extractor.utils import dataframes as df_utils


class Dataset:
    """
    A Dataset represent a table/dataframe in worksheets.
    
    A Dataset is not bind to one file/worksheet but rather
    multiple worksheets within all the files defined in the Source.
    
    A Dataset can be all data in a worksheet 
    or a range within a worksheet.
    It is possible to have multiple datasets in a worksheet.
    
    It allows to define logic on top of all the worksheets 
    of the Source that have similar data.

    A Dataset can have multiple versions, each version contains
    one or multiple couple file-worksheet.
    """

    def __init__(self, source, dataset_dict):
        self._dataset_dict = dataset_dict
        self.source = source
        self.name = dataset_dict.name
        self.table_name = dataset_dict.table_name
        self.config = self.get_config()
        self.type_data = self.config.get('type')
        self.versions = {}
        self.data_ranges = []
        self.data_ranges = []
        self.version_dfs = {}
        self.process_data_ranges()
        self.process_versions()
        self.process_configs()
        self.process_columns()


    def get_config(self):
        return OmegaConf.merge(
            self.source.config,
            self._dataset_dict.get('config', {})
        )
    
    def process_data_ranges(self):
        for file_period, drange_dict in self._dataset_dict.data_ranges.items():
            data_range = data_ranges.DataRange(self, file_period, drange_dict)
            self.data_ranges.append(data_range)
            version = drange_dict["version"]
            if version in self.versions:
                self.versions[version]["files"].append(file_period)
            else:
                self.versions[version] = {"files" : [file_period]}


    def process_versions(self):
        for version_num, version_dc in self.versions.items():
            version_dc["config"] = self._dataset_dict.get(
                "versions", {}
            ).get(
                version_num, {}
            ).get(
                "config", {}
            )

    def process_configs(self):
        for data_range in self.data_ranges:
            version_config = OmegaConf.merge(
                self.config,
                self.versions[data_range.version]["config"]
            )
            data_range._add_version_config(version_config)

    def process_columns(self):
        for version_num, version_dict in self.versions.items():
            data_ranges = self.get_data_ranges_by_version(version_num)
            version_dict['files'] = {
                dr.period:dr.get_data_columns() for dr in data_ranges
            }
            version_dict["cols"] = column_utils.get_cols_to_load(self, version_dict)


    def get_data_ranges_by_version(self, version):
        return filter(lambda dr: dr.version == version, self.data_ranges)


    def load(self):
        for drange in self.data_ranges:
            logger.info(f"Extracting {drange.fqtn}")
            drange.extract()
            logger.info(f"Successfully extracted {drange.fqtn}")
        for version_num in self.versions:
            version_dranges = self.get_data_ranges_by_version(
                version_num
            )
            logger.info(f"Merging {self.name}_v{version_num}..")
            dimensions_df = list(version_dranges)[0].dimensions_df
            ls_dfs = [
                dimensions_df,
                *[y.prepared_df for y in version_dranges]
            ]
            self.version_dfs[version_num] = pd.concat(ls_dfs,  axis=1)

            load_path = self.get_load_path(version_num)
            logger.info(f'Loading data to {load_path}..')
            df_utils.save_df(self.version_dfs[version_num], load_path) 


    def get_load_path(self, version_num):
        load_path = settings.get_load_path(self.source.data_path)
        return pathlib.Path(
            load_path,
            self.source.schema,
            f"{self.table_name}_{version_num}.parquet"
        )