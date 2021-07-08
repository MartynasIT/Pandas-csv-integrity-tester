import pytest
import file_worker as file
import main
import utils

SAMPLE_DATA = file.read_csv(main.FILE_TO_READ)
COLS_SAMPLE = file.get_column_name_list(SAMPLE_DATA)


def test_read_good():
    data = file.read_csv(main.DIRECTORY_COMPARE / 'additional_column.csv')
    assert data is not None


def test_read_bad():
    with pytest.raises(Exception):
        file.read_csv(main.DIRECTORY_COMPARE / 'fff.csv')


def test_save():
    file.save_csv(SAMPLE_DATA, 'output.csv')
    utils.delete_file(main.DIRECTORY_COMPARE / 'output.csv')


def test_check_column_count_additional():
    original_file = file.read_csv(main.DIRECTORY_COMPARE / 'additional_column.csv')
    after_changes = file.check_column_count(SAMPLE_DATA, original_file)
    count_col_sample = SAMPLE_DATA.shape[1]
    count_col_comp = after_changes.shape[1]
    assert count_col_comp == count_col_sample


def test_check_column_count_missing():
    original_file = file.read_csv(main.DIRECTORY_COMPARE / 'missing_column.csv')
    after_changes = file.check_column_count(SAMPLE_DATA, original_file)
    count_col_sample = SAMPLE_DATA.shape[1]
    count_col_comp = after_changes.shape[1]
    assert count_col_comp == count_col_sample


def test_check_column_count_no_header():
    original_file = file.read_csv(main.DIRECTORY_COMPARE / 'no_headers.csv')
    after_changes = file.check_column_count(SAMPLE_DATA, original_file)
    assert file.check_if_header_exists(after_changes)


def test_col_order():
    original_file = file.read_csv(main.DIRECTORY_COMPARE / 'other_column_order.csv')
    after_changes = file.check_col_order(SAMPLE_DATA, original_file)
    assert SAMPLE_DATA.equals(after_changes)


def test_check_if_header_names_correct():
    original_file = file.read_csv(main.DIRECTORY_COMPARE / 'other_headers.csv')
    after_changes = file.check_if_header_names_correct(SAMPLE_DATA, original_file)
    assert SAMPLE_DATA.equals(after_changes)


def test_check_if_header_exists():
    original_file = file.read_csv(main.DIRECTORY_COMPARE / 'no_headers.csv')
    assert file.check_if_header_exists(original_file) is False
    original_file = file.read_csv(main.DIRECTORY_COMPARE / 'other_headers.csv')
    assert file.check_if_header_exists(original_file)


def test_reorder_columns():
    original_file = file.read_csv(main.DIRECTORY_COMPARE / 'other_headers.csv')
    after_changes = file.override_columns(original_file, SAMPLE_DATA)
    assert list(after_changes.columns) == COLS_SAMPLE


def test_override_columns():
    original_file = file.read_csv(main.DIRECTORY_COMPARE / 'other_column_order.csv')
    after_changes = file.reorder_columns(original_file, SAMPLE_DATA)
    assert list(after_changes.columns) == COLS_SAMPLE


def test_check_row_values_same():
    original_file = file.read_csv(main.DIRECTORY_COMPARE / 'sample_file_diff.csv')
    cols_comp = file.get_column_name_list(original_file)
    assert file.check_row_values_same(SAMPLE_DATA, SAMPLE_DATA, COLS_SAMPLE, COLS_SAMPLE)
    assert file.check_row_values_same(SAMPLE_DATA, original_file, COLS_SAMPLE, cols_comp) is False


def test_is_header_names_equal_true():
    assert file.is_header_names_equal(COLS_SAMPLE, COLS_SAMPLE)


def test_is_header_name_equal_false():
    original_file = file.read_csv(main.DIRECTORY_COMPARE / 'other_headers.csv')
    cols_comp = file.get_column_name_list(original_file)
    assert file.is_header_names_equal(COLS_SAMPLE, cols_comp) is False


def test_remove_col():
    original_file = file.read_csv(main.DIRECTORY_COMPARE / 'additional_column.csv')
    after_changes = file.remove_col(SAMPLE_DATA, original_file)
    assert len(COLS_SAMPLE) == len(file.get_column_name_list(after_changes))
    after_changes = file.remove_col(SAMPLE_DATA, SAMPLE_DATA)
    assert len(COLS_SAMPLE) == len(file.get_column_name_list(after_changes))


def test_add_col():
    original_file = file.read_csv(main.DIRECTORY_COMPARE / 'missing_column.csv')
    after_changes = file.add_col(SAMPLE_DATA, original_file)
    assert len(COLS_SAMPLE) == len(file.get_column_name_list(after_changes))
    after_changes = file.remove_col(SAMPLE_DATA, SAMPLE_DATA)
    assert len(COLS_SAMPLE) == len(file.get_column_name_list(after_changes))


def test_check_duplicate_headers():
    original_file = file.read_csv(main.DIRECTORY_COMPARE / 'repeated_header.csv')
    after_changes = file.check_duplicate_headers(original_file)
    cols_comparison = file.get_column_name_list(after_changes)
    for header in cols_comparison:
        data_comp = after_changes[header].tolist()
        assert header not in data_comp


@pytest.mark.parametrize("test_input, expected", [(main.FILE_TO_READ, True), ('sample_file_diff.csv', False)])
def test_check_if_files_equal(test_input, expected):
    data = file.read_csv(main.DIRECTORY_COMPARE / test_input)
    result = file.check_if_files_equal(SAMPLE_DATA, data)
    assert result == expected


@pytest.mark.parametrize("test_input, expected", [(main.FILE_TO_READ, True), ('replaced_column.csv', False)])
def test_check_if_data_equal_ignoring_col_order(test_input, expected):
    data = file.read_csv(main.DIRECTORY_COMPARE / test_input)
    result = file.check_if_data_equal_ignoring_col_order(SAMPLE_DATA, data)
    assert result == expected

