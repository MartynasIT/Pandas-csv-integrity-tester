import pandas as pd
import main
import utils as util


def read_csv(file):
    data = None
    try:
        data = pd.read_csv(file, error_bad_lines=False, warn_bad_lines=True, header=None)
        print(util.get_filename(file) + ' red')
    except Exception as e:
        print(util.get_filename(file) + ' error due to' + str(e))
    if check_if_header_exists(data):
        data.columns = list(data.iloc[0])
        data.drop(index=data.index[0], inplace=True)
    return data


def save_csv(data, filename):
    try:
        data.to_csv(main.DIRECTORY_COMPARE / filename, index=False)
        print('File fixed and  saved as ' + filename)
    except Exception as e:
        print(util.get_filename(filename) + ' error due to' + str(e))


def check_column_count(sample_data, comparison_data):
    count_col_sample = sample_data.shape[1]
    count_col_comp = comparison_data.shape[1]
    has_header_sample = check_if_header_exists(sample_data)
    has_header_comp = check_if_header_exists(comparison_data)
    if not has_header_comp and has_header_sample:
        print('This file has no header')
        comparison_data = override_columns(comparison_data, sample_data)
    else:
        if count_col_comp > count_col_sample:
            print('This file has more columns than sample')
            comparison_data = remove_col(sample_data, comparison_data)
        elif count_col_comp < count_col_sample:
            print('This file has missing columns compared to sample')
            comparison_data = add_col(sample_data, comparison_data)

    return comparison_data


def check_col_order(sample_data, comparison_data):
    cols_sample = list(sample_data.columns)
    cols_comparison = list(comparison_data.columns)
    is_header_number_same = len(cols_sample) == len(cols_comparison)
    if not is_header_number_same:
        print('Files are different even after column removal')
        return comparison_data
    is_header_names_same = is_header_names_equal(cols_sample, cols_comparison)
    is_data_same = check_row_values_same(sample_data, comparison_data, cols_sample, cols_comparison)
    is_data_same_any_row = check_if_data_equal_ignoring_col_order(sample_data, comparison_data)
    if is_data_same_any_row is not True:
        raise ValueError('Files do not have same values')
    elif is_header_names_same and not is_data_same or (
            is_data_same is False and is_data_same_any_row):
        print('This file has different column order')
        comparison_data = reorder_columns(comparison_data, sample_data)
    return comparison_data


def check_if_header_names_correct(sample_data, comparison_data):
    cols_sample = list(sample_data.columns)
    cols_comparison = list(comparison_data.columns)
    is_header_names_same = is_header_names_equal(cols_sample, cols_comparison)
    is_data_same = check_row_values_same(sample_data, comparison_data, cols_sample, cols_comparison)
    if not is_header_names_same and is_data_same:
        print('This file has different header values')
        comparison_data = override_columns(comparison_data, sample_data)
    elif not is_header_names_same and not is_data_same:
        print('Files do not have same data')
    return comparison_data


def check_if_header_exists(data):
    first_row = list(data.columns)
    for i, value in enumerate(first_row):
        row = list(data.iloc[:, i])
        k = 0
        size_row = len(row)
        type_header = type(value)
        for row_val in row:
            if type(row_val) == type_header and len(str(first_row[i])) <= len(str(row_val)):
                k += 1
        if k == size_row:
            return False
    return True


def reorder_columns(comparison_data, sample_data):
    correct_order = []
    for i, value in enumerate(comparison_data):
        col_comp = comparison_data.iloc[:, i].values.tolist()
        for j, val in enumerate(sample_data):
            if sample_data.iloc[:, j].values.tolist() == col_comp:
                correct_order.append(j)
    comparison_data = comparison_data[[comparison_data.columns[q] for q in correct_order]]
    comparison_data.columns = get_column_name_list(sample_data)
    return comparison_data


def override_columns(comparison_data, sample_data):
    cols_sample = get_column_name_list(sample_data)
    comparison_data.columns = cols_sample
    return comparison_data


def check_row_values_same(sample_data, comparison_data, cols_sample, cols_comparison):
    eq_cal = 0
    for i, j in zip(cols_sample, cols_comparison):
        data_sample = sample_data[i].tolist()
        date_comp = comparison_data[j].tolist()
        number_cols = len(cols_sample)
        if len(data_sample) == len(date_comp):
            if set(data_sample) == set(date_comp):
                eq_cal += 1
        else:
            return False
    return eq_cal == number_cols


def is_header_names_equal(headers_sample, headers_comparison):
    headers_sample = sorted(headers_sample)
    headers_comparison = sorted(headers_comparison)
    return headers_sample == headers_comparison


def get_column_name_list(data):
    return list(data.columns)


def remove_col(sample_data, comparison_data):
    cols_sample = get_column_name_list(sample_data)
    cols_comparison = get_column_name_list(comparison_data)
    to_remove = [x for x in cols_comparison if x not in cols_sample]
    comparison_data.drop(columns=to_remove, inplace=True)
    return comparison_data


def add_col(sample_data, comparison_data):
    cols_sample = get_column_name_list(sample_data)
    cols_comparison = get_column_name_list(comparison_data)
    to_add = [x for x in cols_sample if x not in cols_comparison]
    selected_cols = sample_data[to_add].copy()
    return comparison_data.join(selected_cols)


def check_duplicate_headers(comparison_data):
    cols_comparison = get_column_name_list(comparison_data)
    for header in cols_comparison:
        data_comp = comparison_data[header].tolist()
        if header in data_comp:
            print('Duplicate header found')
            comparison_data = comparison_data[comparison_data[header] != header]
    return comparison_data


def check_if_files_equal(data_sample, data_comp_dir):
    if data_sample.columns.equals(data_comp_dir.columns):
        if data_sample.head(3).equals(data_comp_dir.head(3)):
            print('Files are equal')
            return True
    return False


def check_if_data_equal_ignoring_col_order(sample_data, comparison_data):
    count = 0
    for i, val in enumerate(comparison_data):
        col_comp = list(comparison_data.iloc[:, i])
        for j, value in enumerate(sample_data):
            col_sample = list(sample_data.iloc[:, j])
            if col_comp == col_sample:
                count += 1
    if count == len(get_column_name_list(sample_data)):
        return True
    return False
