from omegaconf import OmegaConf

from spreadsheet_extractor.logger import logger
from spreadsheet_extractor.utils import spreadsheets as sheet_utils


class DataRange:
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
        self.raw_df = None

    @property
    def fqtn(self):
        return f"{self.dataset.table_name}_{self.period}"

    def _set_config(self):
        self.config = OmegaConf.merge(
            self._version_config, self._drange_dc.get("config", {})
        )
        self.worksheet = self.get_worksheet()

    def _add_version_config(self, version_config):
        self._version_config = version_config
        self._set_config()

    def extract(self):
        self.raw_df = self.load_raw_data_as_df()

    def get_worksheet(self):
        wb = self.dataset.source.files_dc[self.period]
        return wb[self.config.sheet_name]

    def get_columns(self):
        return self.config.columns

    def get_data_columns(self) -> list:
        return [
            col
            for i, col in enumerate(self.columns)
            if i not in self.config.dimension_cols_index
        ]

    def get_dimensions_cols(self):
        return [self.columns[i] for i in self.config.dimension_cols_index]

    @property
    def cols_to_load(self):
        return self.dataset.versions[self.version]["cols"][self.period]

    def load_raw_data_as_df(self):
        ws = self.worksheet
        # if self.period in self.config.get('replace_cells', {}):
        if self.config.get("replace_cells"):
            logger.info("apply replace map")
            ws = sheet_utils.apply_cell_replacement(ws, self.config.replace_cells)
        raw_df = sheet_utils.get_df_from_cells_range(
            ws, cell_ranges=self.config.data_cells_range, ls_columns=self.config.columns
        )
        return raw_df
