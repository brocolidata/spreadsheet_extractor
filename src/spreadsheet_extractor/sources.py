import pathlib

from spreadsheet_extractor import datasets
from spreadsheet_extractor.logger import logger
from spreadsheet_extractor.utils import spreadsheets as sheet_utils


class Source:
    """
    A Source represent an abstraction for spreadsheets.
    
    A source is not bind to one file but rather a sequence of files
    that are created each period (day, week, ...)
    
    It allows to define logic on top of all the files that have
    similar Datasets.

    A Source can have multiple Datasets.
    """

    def __init__(
        self, 
        source_config:,
        data_path: None | pathlib.Path = None,
    ):
        self._source_config = source_config
        self.name = source_config.name
        self.data_path = data_path
        self.periodicity = source_config.periodicity
        self.config = self.get_config()
        self.file_paths = source_config.file_paths
        self.files_dc = {}
        self.load_files()
        self.schema = source_config.schema
        self.datasets_ls = source_config.datasets
        self.datasets = self.process_datasets()

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

    def get_config(self):
        return self._source_config.get('config', {})
    
    def load_files(self):
        for period, file_path in self._source_config.file_paths.items():
            logger.info(f"Loading {file_path}")
            read_write_ls = self._source_config.get('read_and_write', [])
            if read_write_ls and period in read_write_ls:
                msg = f'{period} file loading may take long (read and write)'
                logger.info(msg)
                read_only = False
            else:
                read_only = True
            self.files_dc[period] = sheet_utils.get_spreadsheet_file(
                self.data_path, 
                file_path,
                read_only
            )
            logger.info(f"Successfully loaded {file_path}")

    
    def process_datasets(self):
        datasets_ls = []
        for dataset_dict in self.datasets_ls:
            logger.info(f"processing {dataset_dict.name}")
            dataset = datasets.Dataset(self, dataset_dict)
            datasets_ls.append(dataset)
        return datasets_ls
    
    def load(self):
        for dataset in self.datasets:
            dataset.load()
