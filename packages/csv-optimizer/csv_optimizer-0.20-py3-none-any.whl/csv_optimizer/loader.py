import pandas as pd
import numpy as np

def load_optimized_dataframe(filename, sample_fraction=0.1, chunksize=1000, use_float_for_nan_ints=False,
                             use_float_for_nan_bools=False, encoding='latin1', **kwargs):
    """
    Load a CSV file with optimized memory usage by detecting the best dtype for each column.

    Parameters:
        filename (str): Path to the CSV file.
        sample_fraction (float): Fraction of the dataset to sample for dtype detection (default: 0.1).
        chunksize (int): Number of rows per chunk when reading the CSV file (default: 1000).
        use_float_for_nan_ints (bool): Store integer columns with NaNs as float32 instead of Pandas Int64 (default: False).
        use_float_for_nan_bools (bool): Store boolean columns with NaNs as float32 instead of Pandas BooleanDtype (default: False).
        encoding (str): File encoding (default: 'latin1').
        **kwargs: Additional arguments for pandas.read_csv().

    Returns:
        pandas.DataFrame: Optimized DataFrame.
    """
    sample_list = []
    chunk_iter = pd.read_csv(filename, encoding=encoding, chunksize=chunksize, **kwargs)

    for chunk in chunk_iter:
        sample_list.append(chunk.sample(frac=sample_fraction, random_state=1))

    file_sample = pd.concat(sample_list).sample(frac=sample_fraction, random_state=1)

    dtype_dict = {}
    parse_dates = []

    for col in file_sample.columns:
        col_data = file_sample[col].dropna()

        if col_data.dtype == 'object':
            try:
                pd.to_datetime(col_data)
                parse_dates.append(col)
            except (ValueError, TypeError):
                if col_data.nunique() / len(col_data) < 0.5:
                    dtype_dict[col] = 'category'

        elif col_data.dtype == 'float64':
            if col_data.mod(1).eq(0).all():
                min_val, max_val = col_data.min(), col_data.max()

                if set(col_data.unique()).issubset({0, 1}):
                    dtype_dict[col] = 'float32' if use_float_for_nan_bools else 'boolean' if file_sample[col].isna().any() else 'bool'
                else:
                    for dtype in [np.int8, np.int16, np.int32, np.int64]:
                        if np.iinfo(dtype).min <= min_val <= max_val <= np.iinfo(dtype).max:
                            dtype_dict[col] = dtype
                            break
                    if file_sample[col].isna().any():
                        dtype_dict[col] = 'float32' if use_float_for_nan_ints else 'Int64'
            else:
                dtype_dict[col] = 'float32' if col_data.abs().max() < np.finfo(np.float32).max else 'float64'

        elif col_data.dtype == 'int64':
            min_val, max_val = col_data.min(), col_data.max()

            if set(col_data.unique()).issubset({0, 1}):
                dtype_dict[col] = 'float32' if use_float_for_nan_bools else 'boolean' if file_sample[col].isna().any() else 'bool'
            else:
                for dtype in [np.int8, np.int16, np.int32, np.int64]:
                    if np.iinfo(dtype).min <= min_val <= max_val <= np.iinfo(dtype).max:
                        dtype_dict[col] = dtype
                        break

    df = pd.read_csv(filename, dtype=dtype_dict, parse_dates=parse_dates, encoding=encoding, **kwargs)
    return df