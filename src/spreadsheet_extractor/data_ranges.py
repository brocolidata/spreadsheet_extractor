import pandas as pd
from omegaconf import OmegaConf

from spreadsheet_extractor.logger import logger
from spreadsheet_extractor.utils import dataframes as df_utils
from spreadsheet_extractor.utils import spreadsheets as sheet_utils


class DataRange():
    """
    A DataRange represent a cell range in a worksheet.
    
    A DataRange is bind to one workshet inside a file defined in the Source.
    
    A DataRange can be all data in the worksheet 
    or a cell range within a worksheet.
    It is possible to have multiple datasets in a worksheet.
    
    It allows to define data extraction logic.
    """

    # def __init__(self, dataset_version, year, year_file_dict={}):
    def __init__(self, dataset, file_period: str, drange_dc: dict):
        self._drange_dc = drange_dc
        self.dataset = dataset
        self.period = file_period
        self.version = drange_dc.version
        self._version_config = {}
        self.config = {}
        self.file_name = dataset.source.file_paths[file_period]
        self.worksheet = None
        self.columns = None
        self.data_columns = None
        self.dimensions_cols = None
        self.raw_df = None
        self.dimensions_df = None
        self.prepared_df = None
        self.df = None

    @property
    def fqtn(self):
        return f"{self.dataset.table_name}_{self.period}"


    def _set_config(self):
        self.config = OmegaConf.merge(
            self._version_config,
            self._drange_dc.get('config', {})
        )
        self.worksheet = self.get_worksheet()
        self.columns = self.get_columns()
        self.dimensions_cols = self.dimensions_cols or self.get_dimensions_cols()
    

    def _add_version_config(self, version_config):
        self._version_config = version_config
        self._set_config()
        

    def extract(self):
        self.load_data_as_df()
        self.df = pd.concat([self.dimensions_df, self.prepared_df],  axis=1)        

    
    def get_worksheet(self):
        wb = self.dataset.source.files_dc[self.period]
        return wb[self.config.sheet_name]
            
    def get_columns(self):
        return sheet_utils.get_ls_columns(
            self.worksheet, 
            self.config.columns_cells_range
        )
    

    def get_data_columns(self) -> list:
        return [
            col for i, col in enumerate(self.columns) \
            if i not in self.config.dimension_cols_index
        ]
    

    def get_dimensions_cols(self):
        return [self.columns[i] for i in self.config.dimension_cols_index]
    
    @property
    def cols_to_load(self):
        return self.dataset.versions[self.version]['cols'][self.period]


    def load_data_as_df(self):
        ws = self.worksheet
        ls_columns = self.get_columns()
        
        if self.period in self.config.get('replace_cells', {}):
            logger.info('apply replace map')
            ws = sheet_utils.apply_cell_replacement(
                ws, 
                self.config.replace_cells[self.period]
            )
        self.raw_df = sheet_utils.get_df_from_cells_range(
            ws,
            cell_ranges = self.config.data_cells_range,
            ls_columns=ls_columns
        )
        self.prepared_df = (
            df_utils.prepare_df(self.config, self.raw_df)
            [self.cols_to_load]
            .pipe(
                df_utils.replace_values_in_df, 
                self.config.get('replace_regex')
            )
        )  
        self.dimensions_df = self.dimensions_df or self.get_dimensions_df()


    def get_dimensions_df(self):
        return (
            self.raw_df
            [self.dimensions_cols]
        )