from csvmanager.fileHandler import read_file

def nb_of_rows(file_path, filters = None):
    data = read_file(file_path, filters)
    return len(data)

def percentage(part, whole):
    if whole <= 0:
        return 0
    return round((part / whole * 100), 2)