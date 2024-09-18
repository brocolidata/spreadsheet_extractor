import pathlib

from omegaconf import OmegaConf

from spreadsheet_extractor import data_ranges, settings


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
        self.type_data = self.config.get("type")
        self.versions = {}
        self.data_ranges = {}
        self.version_dfs = {}
        self.process_data_ranges()
        self.process_versions()
        self.process_configs()

    def get_config(self):
        return OmegaConf.merge(self.source.config, self._dataset_dict.get("config", {}))

    def process_data_ranges(self):
        for file_period, drange_dict in self._dataset_dict.data_ranges.items():
            data_range = data_ranges.DataRange(self, file_period, drange_dict)
            self.data_ranges[file_period] = data_range
            self.append_drange_to_versions(file_period, drange_dict)

    def append_drange_to_versions(self, file_period, drange_dict):
        version = drange_dict["version"]
        if version in self.versions:
            self.versions[version]["files"].append(file_period)
        else:
            self.versions[version] = {"files": [file_period]}

    def process_versions(self):
        for version_num, version_dc in self.versions.items():
            version_dc["config"] = (
                self._dataset_dict.get("versions", {})
                .get(version_num, {})
                .get("config", {})
            )

    def process_configs(self):
        for _, data_range in self.data_ranges.items():
            version_config = OmegaConf.merge(
                self.config, self.versions[data_range.version]["config"]
            )
            data_range._add_version_config(version_config)

    def get_data_ranges_by_version(self, version):
        return filter(lambda dr: dr.version == version, self.data_ranges)

    def get_load_path(self, version_num):
        load_path = settings.get_load_path(self.source.data_path)
        return pathlib.Path(
            load_path, self.source.schema, f"{self.table_name}_{version_num}.parquet"
        )
