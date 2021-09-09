import csv


def insert_headers_to_csv(csv_path, csv_file_name, headers):
    csv_file = open(csv_path + csv_file_name, 'a', encoding="utf-8", newline='')
    try:
        with csv_file as f:
            for header in headers:
                writer = csv.writer(f)
                writer.writerow(list(header.values()))
    except IOError:
        print("I/O error")


def clear_csv_file(csv_path):
    csv_file = open(csv_path, 'r+')
    csv_file.truncate(0)
    csv_file.close()


def whitespace_remover(dataframe):
    # iterating over the columns
    for i in dataframe.columns:

        # checking datatype of each columns
        if dataframe[i].dtype == 'object':

            # applying strip function on column
            dataframe[i] = dataframe[i].str.strip()
        else:

            # if condn. is False then it will do nothing.
            pass
