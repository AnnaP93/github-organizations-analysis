import requests
import os
from dotenv import load_dotenv
import sys
from sqlite_git_organizations_demo import __fill_organizations_table
from sqlite_git_organizations_demo import __return_pretty_table
from sqlite_git_organizations_demo import __return_all_data
from sqlite_git_organizations_demo import __update_record
from sqlite_git_organizations_demo import __check_if_company_exist_in_table
import datetime
from datetime import timedelta


def get_all_repositories_data(organization):
    all_info = []
    url = 'https://api.github.com/search/repositories'
    is_final_page = False
    while not is_final_page:
        response = __get_api_response(url, organization)
        convert_to_json = response.json()['items']
        for item in convert_to_json:
            all_info.append(item)
        if 'next' in response.links:
            next_url = response.links['next']['url']
            url = next_url
            is_final_page = False
        else:
            is_final_page = True

    stars_in_all_repositories = sum(map(lambda repository: repository['stargazers_count'], all_info))
    forks_in_all_repositories = sum(map(lambda repository: repository['forks_count'], all_info))
    average_issues_in_all_repositories = round(sum((map(lambda repository: repository['open_issues_count'],
                                                        all_info)))/len(all_info), 1)
    time_of_record = datetime.datetime.now()
    all_repository_stats = [organization, stars_in_all_repositories, forks_in_all_repositories,
                            average_issues_in_all_repositories, time_of_record]
    return all_repository_stats


def __get_api_response(url, company):
    headers = {'Accept': 'application/vnd.github.v3+json', "Authorization": "token " + os.environ.get('GITHUB_API_TOKEN')}
    repositories_in_organization = requests.get(url=url, headers=headers,
                                                params={'q': 'org:' + company})
    return repositories_in_organization


def __check_time_when_added(company):
    # complete_table = __return_all_data()
    check_company_existence = __check_if_company_exist_in_table(company)
    if check_company_existence != []:
        for record in check_company_existence:
            date_time_obj = datetime.datetime.strptime(record[5], '%Y-%m-%d %H:%M:%S.%f')
            if datetime.datetime.now() - date_time_obj >= timedelta(weeks=1):
                new_stats = get_all_repositories_data(company)
                updated_tuple = __update_record(tuple(new_stats))
                return updated_tuple
            else:
                return record
    else:
        company_stats = get_all_repositories_data(company)
        inserting_data_into_database = __fill_organizations_table(tuple(company_stats))
        return inserting_data_into_database


if __name__ == "__main__":
    # Credentials
    load_dotenv('token.env')

    organizations = sys.argv[1:]
    for single_company in organizations:
        single_company_stats = __check_time_when_added(single_company)
        return_single_company_stats = __return_pretty_table(single_company)
        print(return_single_company_stats)


