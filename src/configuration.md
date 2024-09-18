# Spreasheet Extractor configuration

* [Source configuration](#source-configuration)
* [`datasets:` configuration](#datasets-configuration)
* [`config:` configuration](#config-configuration)
* [`data_ranges:` configuration](#data_ranges-configuration)
* [Complete config example](#complete-config-example)

## Source configuration

These are the top level settings for configuring sources : 

| **Key**          | **Type** | **Description**                                                             | **Required or Optional** | **Example**                                                           |
|------------------|----------|-----------------------------------------------------------------------------|--------------------------|-----------------------------------------------------------------------|
| `name`           | string   | Name of the Source                                                          | Required                 | `"Indice des Prix"`                                                   |
| `periodicity`    | string   | Periodicity of the Source. One of [`year`].                                 | Required                 | `year`                                                                |
| `schema`         | string   | Name of the database schema where the tables will be stored                 | Required                 | `indice_des_prix`                                                     |
| `config`         | dict     | Config dict. See [`config` configuration](#config-configuration)                                                   | Optional                 |                                                                       |
| `file_paths`     | dict     | Dict of `period:file_path`                                                  | Required                 | `2022: "Annuaire Statistique 2022/17. Indice des prix _AS 2022.xlsx"` |
| `read_and_write` | list     | List of `period` to be loaded with read-and-write mode instead of read-only (required when using `replace_cells`) | Optional                 | `[2019, 2021]`                                                        |
| `datasets`       | list     | List of datasets. See [`datasets` configuration](#datasets-configuration)                                            | Required                 |                                                                       |

## `datasets:` configuration

Each dataset is a YAML list element inside the `datasets:` key. 

They can be configured with the following settings : 

| **Key**       	| **Type** 	| **Description**                               	| **Required or Optional** 	| **Example**                                                            	|
|---------------	|----------	|-----------------------------------------------	|--------------------------	|------------------------------------------------------------------------	|
| `name`        	| string   	| Name of the dataset (descriptive)             	| Required                 	| `Indice des prix à la production industrielle, énergétique et minière` 	|
| `table_name`  	| string   	| Name of the database table                    	| Required                 	| `ipp`                                                                  	|
| `config`      	| dict     	| Config dict. See [`config` configuration](#config-configuration)                    	| Required                 	|                                                                        	|
| `data_ranges` 	| dict     	| Data Ranges of the dataset. See [`data_ranges` configuration](#data_ranges-configuration) 	| Required                 	|                                                                        	|

## `data_ranges:` configuration

Each DataRange is a key:value pair inside the `data_ranges:` key in the config.
The key is the `period` and the value is a YAML dict with the following keys :

| **Key**   	| **Type** 	| **Description**                  	| **Required or Optional** 	| **Example** 	|
|-----------	|----------	|----------------------------------	|--------------------------	|-------------	|
| `version` 	| integer  	| Version number of the data range 	| Required                 	| `1`         	|
| `config`  	| dict     	| Config dict. See [`config` configuration](#config-configuration)        	| Optional                 	|             	|



## `config:` configuration

Configs can be defined at the following level :
- top (source)
    - dataset
        - versions
            - dataranges

The following settings can be defined in top level and overriden in lower level.


| **Key**            | **Type** | **Description**                                     | **Required or Optional** | **Example**                |
|--------------------|----------|-----------------------------------------------------|--------------------------|----------------------------|
| `sheet_name`       | string   | Name of the worksheet where the dataset is located  | Required                 | `ipp`                      |
| `historic_periods` | integer  | Number of historic periods available in the dataset | Required                 | `3`                        |
| `data_cells_range` | string   | Cells range where the data is located               | Required                 | `A9:E42`                   |
| `replace_cells`    | dict     | Mapping of cell ranges and values to be replaced    | Optional                 | `{"D120":8.1, "E120":8.11` |


## Complete config example
See the config used for test : [`indice_des_prix.yaml`](src/tests/assets/sources/indice_des_prix.yaml)