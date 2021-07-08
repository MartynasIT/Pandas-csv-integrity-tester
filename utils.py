import pathlib


def get_current_dir():
    return pathlib.Path.cwd()


def get_filename(path):
    path_obj = pathlib.Path(path)
    return path_obj.name


def delete_file(path):
    rem_file = pathlib.Path(path)
    rem_file.unlink()
