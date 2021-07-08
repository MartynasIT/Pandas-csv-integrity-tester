import file_worker as file
import utils as util

DIRECTORY_COMPARE = util.get_current_dir() / 'files_to_compare/'
FILE_TO_READ = util.get_current_dir() / 'sample_file.csv'

if __name__ == '__main__':
    selected_file = input('Select file name to compare: ')
    # selected_file = 'additional_column.csv'
    try:
        data_comp_dir = file.read_csv(DIRECTORY_COMPARE / selected_file)
        data_sample = file.read_csv(FILE_TO_READ)
    except AttributeError as e:
        print('{0} {1}'.format('Program failed due to problem of reading the file. Error:', str(e)))
        exit(1)
    print('{0} {1}'.format('checking file', selected_file))

    if not file.check_if_files_equal(data_sample, data_comp_dir):
        if not data_comp_dir.shape[1] == 1:
            data_comp_dir = file.check_column_count(data_sample, data_comp_dir)
            data_comp_dir = file.check_duplicate_headers(data_comp_dir)
            data_comp_dir = file.check_col_order(data_sample, data_comp_dir)
            data_comp_dir = file.check_if_header_names_correct(data_sample, data_comp_dir)
            file.save_csv(data_comp_dir, selected_file)
            print('all checked')
        else:
            print('Error file has only one column so it is most likely bad')



