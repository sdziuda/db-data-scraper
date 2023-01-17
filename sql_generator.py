import numpy as np


def generate_sql_query(table_name, column_names, column_values):
    return "INSERT INTO " + table_name + " (" + ", ".join(column_names) + ") VALUES (" + ", ".join(column_values) + ");"


def generate_sql_queries_from_file(file_name, table_name):
    input_csv = np.loadtxt(file_name, delimiter=",", dtype=str, encoding="utf-8")
    column_names = input_csv[0]
    column_values = input_csv[1:]
    res = []
    lens = []
    lens_names = []
    lens_surnames = []
    for value in column_values:
        if table_name == "wojewodztwo" or table_name == "komitet":
            lens += [len(value[1])]
        elif table_name != "kandydat":
            lens += [len(value[2])]

        if table_name == "kandydat" and value[2] != "":
            lens_names += [len(value[1])]
            lens_names += [len(value[2])]
            lens_surnames += [len(value[3])]
            res += [generate_sql_query(table_name, column_names, value)]
        elif table_name == "kandydat" and value[2] == "":
            lens_names += [len(value[1])]
            lens_surnames += [len(value[3])]
            res += [generate_sql_query(table_name, [column_names[0], column_names[1], column_names[3], column_names[4]],
                                       [value[0], value[1], value[3], value[4]])]
        else:
            res += [generate_sql_query(table_name, column_names, value)]
    if table_name != "kandydat":
        print(table_name + " " + str(max(lens)))
    else:
        print(table_name + " " + str(max(lens_names)) + " " + str(max(lens_surnames)))

    return res


# This function needs to be different because of the way the data about locales is stored in the file
def generate_sql_locales(file_name, table_name):
    input_csv = open(file_name, "r", encoding="utf-8")
    column_names = input_csv.readline().strip().split(",")
    res = []
    lens = []

    for r in input_csv:
        r = r.strip()
        if len(r) > 0:
            res += [generate_sql_query(table_name, column_names,
                                       [r.split(",")[0], r.split(",")[1], "".join(r.split(",")[2:])])]
            lens += [len("".join(r.split(",")[2:]))]
    print(table_name + " " + str(max(lens)))
    return res


def generate_sql_file(queries, file_name):
    output = open(file_name, "w", encoding="utf-8")
    for query in queries:
        output.write(query + "\n")
    output.close()


generate_sql_file(generate_sql_queries_from_file("res/voivodeships.csv", "wojewodztwo"), "sql/voivodeships.sql")
generate_sql_file(generate_sql_queries_from_file("res/districts.csv", "powiat"), "sql/districts.sql")
generate_sql_file(generate_sql_queries_from_file("res/municipalities.csv", "gmina"), "sql/municipalities.sql")
generate_sql_file(generate_sql_queries_from_file("res/committees.csv", "komitet"), "sql/committees.sql")
generate_sql_file(generate_sql_queries_from_file("res/candidates.csv", "kandydat"), "sql/candidates.sql")
generate_sql_file(generate_sql_queries_from_file("res/results_corrected.csv", "wyniki"), "sql/results.sql")
generate_sql_file(generate_sql_locales("res/locales_corrected.csv", "lokal"), "sql/locales.sql")
