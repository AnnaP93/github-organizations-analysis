import sqlite3
from prettytable import from_db_cursor


conn = sqlite3.connect('/Users/annapopovych/PycharmProjects/github-resumes/github-organizations-analysis/github_companies_analysis.db')
c = conn.cursor()


def create_organizations_table():
    create_table_query = "CREATE TABLE organizations_stats " \
                         "(id INTEGER PRIMARY KEY, " \
                         "organization TEXT NOT NULL," \
                         "total_number_of_stars REAL NOT NULL," \
                         "total_number_of_forks REAL NOT NULL," \
                         "average_number_of_issues REAL NOT NULL);"
    c.execute(create_table_query)
    conn.commit()
    c.close()


# create_organizations_table()


def __fill_organizations_table(single_company_data):
    insert_data_query = "INSERT INTO organizations_stats (organization, total_number_of_stars, " \
                        "total_number_of_forks, average_number_of_issues, record_time) VALUES (?, ?, ?, ?, ?)"
    c.execute(insert_data_query, single_company_data)
    conn.commit()


def delete_extra_rows():
    delete_data_query = "DELETE FROM organizations_stats WHERE id >= 1;"
    c.execute(delete_data_query)
#   conn.commit()

# delete_extra_rows()


def add_time_column():
    add_column_query = "ALTER TABLE organizations_stats ADD COLUMN record_time TEXT;"
    c.execute(add_column_query)
    # conn.commit()
    # c.close()

# add_time_column()


def __return_complete_table():
    selection = c.execute("SELECT * FROM organizations_stats;")
    return from_db_cursor(selection)



