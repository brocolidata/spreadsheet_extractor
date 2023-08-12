# def dispatch_periodicity(data_range):
#     periodicity = data_range.dataset.source.periodicity
#     match periodicity:
#         case "year":
#             process_year_period(data_range)
            
# def process_year_period(data_range):

def get_cols_to_load(
        version_dict
    ):
    period_ls = list(version_dict["files"].keys())
    period_ls.sort(reverse=True)
    col_period_mapping = {}
    for period in period_ls:
        col_period_mapping.update(
            {
                col:period for col in version_dict["files"][period] \
                if col not in col_period_mapping
            }
        )
    period_col_mapping = {period:[] for period in version_dict["files"]}
    for col, period in col_period_mapping.items():
        period_col_mapping[period].append(col)

    return period_col_mapping