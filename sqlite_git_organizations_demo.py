import sqlite3
from prettytable import from_db_cursor


def __open_connection():
    conn = sqlite3.connect('github_companies_analysis.db')
    return conn


def create_organizations_table():
    connection = __open_connection()
    c = connection.cursor()
    create_table_query = "CREATE TABLE organizations_stats " \
                         "(id INTEGER PRIMARY KEY, " \
                         "organization TEXT NOT NULL," \
                         "total_number_of_stars REAL NOT NULL," \
                         "total_number_of_forks REAL NOT NULL," \
                         "average_number_of_issues REAL NOT NULL);"
    c.execute(create_table_query)
    connection.commit()
    c.close()
    connection.close()


def __fill_organizations_table(single_company_data):
    connection = __open_connection()
    c = connection.cursor()
    insert_data_query = "INSERT INTO organizations_stats (organization, total_number_of_stars, " \
                        "total_number_of_forks, average_number_of_issues, record_time) VALUES (?, ?, ?, ?, ?)"
    c.execute(insert_data_query, single_company_data)
    connection.commit()

    selection = "SELECT * FROM organizations_stats WHERE organization = ?"
    c.execute(selection, (single_company_data[0],))

    results = c.fetchall()
    c.close()
    connection.close()
    return results


def delete_extra_rows():
    connection = __open_connection()
    c = connection.cursor()
    delete_data_query = "DELETE FROM organizations_stats WHERE id BETWEEN 10 and 11;"
    c.execute(delete_data_query)
    connection.commit()
    c.close()
    connection.close()

# delete_extra_rows()


def add_time_column():
    connection = __open_connection()
    c = connection.cursor()
    add_column_query = "ALTER TABLE organizations_stats ADD COLUMN record_time TEXT;"
    c.execute(add_column_query)
    connection.commit()
    c.close()
    connection.close()

# add_time_column()


# Return pretty table
def __return_single_value_in_pretty_table(company_name):
    connection = __open_connection()
    c = connection.cursor()
    selection = c.execute("SELECT * FROM organizations_stats WHERE organization = ?;", (company_name,))
    actual_table = from_db_cursor(selection)
    c.close()
    connection.close()
    return actual_table


def __update_record(record):
    connection = __open_connection()
    c = connection.cursor()
    update_record_query = "UPDATE organizations_stats SET organization = ?, total_number_of_stars = ?, " \
                          "total_number_of_forks = ?, average_number_of_issues = ?, record_time = ? WHERE organization = ?;"
    data = (record[0], record[1], record[2], record[3], record[4], record[0])
    c.execute(update_record_query, data)
    connection.commit()

    selection = "SELECT * FROM organizations_stats WHERE organization = ?"
    c.execute(selection, (record[0],))
    results = c.fetchall()
    c.close()
    connection.close()
    return results


def __check_if_company_exist_in_table(company):
    connection = __open_connection()
    c = connection.cursor()
    select_query = "SELECT * FROM organizations_stats WHERE organization = ?"
    c.execute(select_query, (company,))
    result = c.fetchall()
    c.close()
    connection.close()
    return result


# Creating an index for the table
def create_index_for_table():
    connection = __open_connection()
    c = connection.cursor()
    create_index_query = "CREATE INDEX organizations_stats_organizations ON organizations_stats(organization);"
    c.execute(create_index_query)
    connection.commit()
    c.close()
    connection.close()


def __return_top_ten():
    connection = __open_connection()
    c = connection.cursor()
    selection = c.execute("SELECT * FROM organizations_stats ORDER BY total_number_of_stars LIMIT 10;")
    actual_table = from_db_cursor(selection)
    c.close()
    connection.close()
    return actual_table


