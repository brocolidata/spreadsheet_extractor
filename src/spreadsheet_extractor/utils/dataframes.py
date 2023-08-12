import pandas as pd

def merge_categories_and_elements(
    df: pd.DataFrame,
    dimension_cols: list
) -> pd.DataFrame:
    col_years=list(df.columns.difference(dimension_cols))
    ls_produits = []
    category = {}
    for i, row in df.iterrows():
        row_dc = row.to_dict()
        actual = {col:row_dc[col] for col in dimension_cols}
        elem = row_dc[col_years[0]]
        if pd.isna(elem):
            category = actual
        else:
            ls_produits.append(
                {
                    col:str(category.get(col)).strip() + " " + str(actual.get(col)).strip() for col in dimension_cols
                }
            )

    df_produits = pd.DataFrame(ls_produits)

    df_values = (
        df[col_years]
        .dropna(
            axis=0,
            how='any',
        )
        .reset_index(drop=True)
    )
    
    return pd.concat([df_produits, df_values], axis=1)


def merge_multiline_labels(
    df: pd.DataFrame,
    dimension_cols: list
) -> pd.DataFrame:
    col_data=list(df.columns.difference(dimension_cols))
    ls_produits = []
    previous = {}
    for i, row in df.iterrows():
        row_dc = row.to_dict()
        actual = {col:row_dc[col] for col in dimension_cols}
        elem = row_dc[col_data[0]]
        if pd.isna(elem):
            previous = actual
        elif previous:
            ls_produits.append(
                {
                    col:str(previous.get(col)).strip() + "" + str(actual.get(col)).strip() for col in dimension_cols
                }
            )
            previous = {}
        else:

            ls_produits.append(
                { 
                    col:str(actual.get(col)).strip() for col in dimension_cols 
                }
            )
            previous = {}

    df_produits = pd.DataFrame(ls_produits)
    
    # clean values
    df_values = (
        df[col_data]
        .dropna(
            axis=0,
            how='any',
        )
        .reset_index(drop=True)
    )
    out_df = pd.concat([df_produits, df_values], axis=1)
    out_df.columns = df.columns
    return out_df


def prepare_df(config, df:pd.DataFrame) -> pd.DataFrame:

    dimension_cols = df.columns[config.dimension_cols_index]

    if config.merge_strategy == 'merge_multiline_labels':
        clean_df = merge_multiline_labels(df, dimension_cols) 
    elif config.merge_strategy == 'merge_categories_and_elements':
        clean_df = merge_categories_and_elements(df, dimension_cols) 
    else:
        clean_df = df
    return clean_df


def save_df(df: pd.DataFrame, path):
    if not path.parent.exists():
        path.parent.mkdir(parents=True)
    
    df.to_parquet(
        path,
        index = None
    )

def replace_values_in_df(df, replace_regex=None):
    coma_df = (
        df
        .replace(r'\,', '.', regex=True)
    )
    if replace_regex:
        df_replaced = (
            coma_df
            .replace(
                replace_regex,
                regex=True
            )
            .apply(pd.to_numeric)
        )
    else:
        df_replaced = coma_df

    return df_replaced